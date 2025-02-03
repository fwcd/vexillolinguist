from pathlib import Path
from vexillolinguist.color import parse_color

import argparse
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
LANGUAGES_PATH = ROOT_DIR / 'resources' / 'languages.yml'

def main():
    parser = argparse.ArgumentParser(description='Flag-directed, language-aware Git repo initialization tool')
    parser.add_argument('--languages', type=Path, default=LANGUAGES_PATH, help="Path to the languages.yml used by GitHub's Linguist")
    parser.add_argument('colors', type=str, nargs=argparse.ONE_OR_MORE, help='The color codes or names of the flag')

    args = parser.parse_args()

    with open(args.languages, 'r') as f:
        langs = yaml.safe_load(f)
    
    colors = [parse_color(c) for c in args.colors]

    print(langs)
    print(colors)
