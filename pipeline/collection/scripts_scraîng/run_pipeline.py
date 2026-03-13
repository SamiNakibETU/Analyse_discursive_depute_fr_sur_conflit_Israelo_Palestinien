import argparse
import json

from final_pipeline.pipeline import FinalDataPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Exécute les étapes 1 et 2 du pipeline FINAL")
    parser.add_argument("--metadata", help="Chemin vers un fichier où stocker le récapitulatif", default=None)
    args = parser.parse_args()

    pipeline = FinalDataPipeline()
    metadata = pipeline.run()
    if args.metadata:
        Path(args.metadata).write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    from pathlib import Path
    main()
