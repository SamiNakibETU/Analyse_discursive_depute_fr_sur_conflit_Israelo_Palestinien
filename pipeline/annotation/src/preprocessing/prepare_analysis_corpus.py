"""
Prepare clean analysis datasets (tweets + interventions).
Fix author names, groups, and context BEFORE analysis.
"""
import glob
import pandas as pd


def clean_name(name: str) -> str:
    if not isinstance(name, str):
        return "UNKNOWN"
    cleaned = " ".join(name.replace("\u00a0", " ").split())
    if cleaned == "":
        return "UNKNOWN"
    if cleaned.upper() == cleaned:
        particles = {"de", "du", "des", "la", "le", "les", "d'", "l'"}
        parts = []
        for part in cleaned.lower().split():
            if part in particles:
                parts.append(part)
            else:
                parts.append(part.capitalize())
        return " ".join(parts)
    return cleaned


def build_an_context(row: pd.Series) -> str:
    parts = ["AN"]
    if "sitting_label" in row and pd.notna(row["sitting_label"]):
        parts.append(str(row["sitting_label"]))
    if "matched_role" in row and pd.notna(row["matched_role"]):
        parts.append(f"role={row['matched_role']}")
    if "EXCERPT_INFO" in row and pd.notna(row["EXCERPT_INFO"]):
        parts.append(f"excerpt={row['EXCERPT_INFO']}")
    return " | ".join(parts)


def build_tweet_context(row: pd.Series) -> str:
    parts = ["Twitter"]
    if row.get("is_retweet") is True:
        parts.append("RETWEET")
    if row.get("is_reply") is True:
        parts.append("REPLY")
    if pd.notna(row.get("retweets")) or pd.notna(row.get("likes")):
        parts.append(f"rt={row.get('retweets', 0)}")
        parts.append(f"likes={row.get('likes', 0)}")
    if pd.notna(row.get("url")):
        parts.append(f"url={row['url']}")
    return " | ".join(parts)


def prepare_interventions() -> pd.DataFrame:
    interv = pd.read_parquet("data/annotated/predictions/interventions_v3_full.parquet")

    # Author normalization
    if "AUTEUR" in interv.columns:
        interv["AUTEUR"] = interv["AUTEUR"].apply(clean_name)
    elif "speaker_name" in interv.columns:
        interv["AUTEUR"] = interv["speaker_name"].apply(clean_name)
    else:
        interv["AUTEUR"] = "UNKNOWN"

    # Group fix
    if "GROUPE" not in interv.columns:
        interv["GROUPE"] = "UNKNOWN"
    mask_unknown = interv["GROUPE"].astype(str).str.strip().str.upper() == "UNKNOWN"
    if "matched_group" in interv.columns:
        interv.loc[mask_unknown, "GROUPE"] = interv.loc[mask_unknown, "matched_group"]
        mask_unknown = interv["GROUPE"].astype(str).str.strip().str.upper() == "UNKNOWN"
    if "matched_group_long" in interv.columns:
        interv.loc[mask_unknown, "GROUPE"] = interv.loc[mask_unknown, "matched_group_long"]

    # Context
    interv["CONTEXTE"] = interv.apply(build_an_context, axis=1)

    return interv


def prepare_tweets() -> pd.DataFrame:
    files = sorted(glob.glob("data/annotated/predictions/tweets_v3_chunk_*.parquet"))
    tweets = pd.concat([pd.read_parquet(p) for p in files], ignore_index=True)

    # Fill missing depute_name / group from username majority
    name_map = (
        tweets.groupby("username")["depute_name"]
        .agg(lambda x: x.dropna().mode().iloc[0] if len(x.dropna().mode()) else None)
    )
    group_map = (
        tweets.groupby("username")["groupe_politique"]
        .agg(lambda x: x.dropna().mode().iloc[0] if len(x.dropna().mode()) else None)
    )

    tweets["depute_name"] = tweets.apply(
        lambda r: name_map.get(r["username"]) if pd.isna(r["depute_name"]) else r["depute_name"],
        axis=1,
    )
    tweets["groupe_politique"] = tweets.apply(
        lambda r: group_map.get(r["username"]) if pd.isna(r["groupe_politique"]) else r["groupe_politique"],
        axis=1,
    )

    # Context
    tweets["CONTEXTE"] = tweets.apply(build_tweet_context, axis=1)

    return tweets


def main():
    tweets = prepare_tweets()
    tweets.to_parquet("data/annotated/predictions/tweets_v3_full_clean.parquet", index=False)

    interv = prepare_interventions()
    interv.to_parquet("data/annotated/predictions/interventions_v3_full_clean.parquet", index=False)

    print("Saved clean datasets:")
    print(" - data/annotated/predictions/tweets_v3_full_clean.parquet")
    print(" - data/annotated/predictions/interventions_v3_full_clean.parquet")


if __name__ == "__main__":
    main()
