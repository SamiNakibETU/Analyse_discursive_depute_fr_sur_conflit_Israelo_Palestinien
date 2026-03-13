#!/usr/bin/env python3
"""Extract Twitter accounts from deputé_2023_tweeter.html file."""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

# Fix UTF-8 encoding on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = Path("deputé_2023_tweeter.html")
EXISTING_MAPPING = Path("FINAL/config/twitter_handles.json")
OUTPUT_FILE = Path("FINAL/config/twitter_handles_2023.json")


class TwitterExtractor(HTMLParser):
    """Extrait les comptes Twitter depuis le HTML."""

    def __init__(self):
        super().__init__()
        self.twitter_accounts = {}
        self.current_depute = None
        self.in_name_cell = False
        self.name_parts = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        # Detect name cells - they contain député links
        if tag == 'a' and 'href' in attrs_dict:
            href = attrs_dict['href']

            # Pattern: /deputes/fiche/OMC_PAXXXX or similar
            if '/deputes/' in href or 'assemblee-nationale.fr' in href:
                self.in_name_cell = True
                self.name_parts = []

            # Twitter link
            elif 'twitter.com' in href:
                # Extract username from URL like:
                # https://web.archive.org/web/20230128023635/https://twitter.com/@username/
                # or https://twitter.com/@username/
                match = re.search(r'twitter\.com/@?([a-zA-Z0-9_]+)', href)
                if match:
                    username = match.group(1)
                    # Save with the most recent député name we saw
                    if self.current_depute and username:
                        self.twitter_accounts[self.current_depute] = username

    def handle_data(self, data):
        # Collect name parts when in a name cell
        if self.in_name_cell:
            text = data.strip()
            if text:
                self.name_parts.append(text)

    def handle_endtag(self, tag):
        # When we close a link in name cell, join the parts
        if tag == 'a' and self.in_name_cell:
            if self.name_parts:
                # Join parts and clean
                full_name = ' '.join(self.name_parts).strip()
                # Clean up extra spaces
                full_name = re.sub(r'\s+', ' ', full_name)
                if full_name and len(full_name) > 2:
                    self.current_depute = full_name
            self.in_name_cell = False
            self.name_parts = []


def normalize_name(name):
    """Normalize name for matching (remove accents, lowercase)."""
    replacements = {
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'à': 'a', 'â': 'a', 'ä': 'a',
        'ô': 'o', 'ö': 'o',
        'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'î': 'i', 'ï': 'i',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A', 'Ä': 'A',
        'Ô': 'O', 'Ö': 'O',
        'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C', 'Î': 'I', 'Ï': 'I'
    }
    normalized = name
    for old, new in replacements.items():
        normalized = normalized.replace(old, new)
    return normalized.lower().strip()


def load_existing_mapping():
    """Load existing Twitter handles mapping."""
    if EXISTING_MAPPING.exists():
        with open(EXISTING_MAPPING, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def extract_accounts_from_html():
    """Extract Twitter accounts from HTML file."""
    print(f"📖 Lecture de {HTML_FILE}...")

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse HTML
    parser = TwitterExtractor()
    parser.feed(html_content)

    accounts = parser.twitter_accounts
    print(f"✅ {len(accounts)} comptes Twitter extraits du fichier 2023")

    return accounts


def merge_with_existing(new_accounts):
    """Merge new accounts with existing mapping."""
    existing = load_existing_mapping()
    print(f"📋 {len(existing)} comptes existants")

    # Create normalized lookup
    normalized_existing = {}
    for name in existing.keys():
        norm = normalize_name(name)
        normalized_existing[norm] = name

    added = 0
    updated = 0

    for name, twitter in new_accounts.items():
        norm_name = normalize_name(name)

        # Check if we already have this name (normalized)
        if norm_name in normalized_existing:
            existing_name = normalized_existing[norm_name]
            if existing[existing_name] != twitter:
                print(f"⚠️  Mise à jour: {existing_name} → @{twitter} (était @{existing[existing_name]})")
                existing[existing_name] = twitter
                updated += 1
        else:
            # New entry
            existing[name] = twitter
            added += 1

    print(f"\n✨ {added} nouveaux comptes ajoutés")
    print(f"🔄 {updated} comptes mis à jour")
    print(f"📊 Total: {len(existing)} comptes")

    return existing


def save_mapping(mapping):
    """Save Twitter mapping to file."""
    # Save 2023-specific file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Sauvegardé dans {OUTPUT_FILE}")

    # Update main mapping file
    with open(EXISTING_MAPPING, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)
    print(f"💾 Mapping principal mis à jour: {EXISTING_MAPPING}")


def main():
    print("=" * 70)
    print("EXTRACTION COMPTES TWITTER - Fichier 2023")
    print("=" * 70)
    print()

    # Extract from HTML
    new_accounts = extract_accounts_from_html()

    # Show some examples
    print("\n📝 Exemples extraits:")
    for i, (name, twitter) in enumerate(list(new_accounts.items())[:5]):
        print(f"   {name} → @{twitter}")

    # Merge with existing
    print("\n" + "=" * 70)
    print("FUSION AVEC MAPPING EXISTANT")
    print("=" * 70)
    print()

    merged = merge_with_existing(new_accounts)

    # Save
    save_mapping(merged)

    print("\n" + "=" * 70)
    print("✅ EXTRACTION TERMINÉE")
    print("=" * 70)


if __name__ == '__main__':
    main()
