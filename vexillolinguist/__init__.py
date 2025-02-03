from pathlib import Path
from vexillolinguist.color import parse_color

import argparse
import subprocess
import yaml

ROOT_DIR = Path(__file__).resolve().parent.parent
LANGUAGES_PATH = ROOT_DIR / 'resources' / 'languages.yml'

def main():
    parser = argparse.ArgumentParser(description='Flag-directed, language-aware Git repo initialization tool')
    parser.add_argument('--languages', type=Path, default=LANGUAGES_PATH, help="Path to the languages.yml used by GitHub's Linguist")
    parser.add_argument('-o', '--output', type=Path, help='The path to the output directory for the Git repo to be created. Treated as a dry-run if left unspecified.')
    parser.add_argument('colors', type=str, nargs=argparse.ONE_OR_MORE, help='The color codes or names of the flag')

    args = parser.parse_args()

    print('==> Reading languages...')
    with open(args.languages, 'r') as f:
        langs = yaml.safe_load(f)
        lang_colors = {name: parse_color(lang['color']) for name, lang in langs.items() if 'color' in lang and 'extensions' in lang}
    
    print('==> Parsing colors...')
    flag_raw_colors = args.colors
    flag_colors = [parse_color(c) for c in flag_raw_colors]

    print('==> Matching colors...')
    flag_lang_names = [min(lang_colors.items(), key=lambda entry: c.distance_to(entry[1]))[0] for c in flag_colors]
    flag_extensions = [langs[lang]['extensions'][0] for lang in flag_lang_names]
    print('\n'.join(f'    {color:>9} -> {lang:<16} ({ext})' for color, lang, ext in zip(flag_raw_colors, flag_lang_names, flag_extensions)))

    if args.output:
        print('==> Creating Git repo...')
        output: Path = args.output
        output.mkdir(parents=True)
        subprocess.run(['git', 'init'], cwd=output)
