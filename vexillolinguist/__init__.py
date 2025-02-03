from pathlib import Path
from send2trash import send2trash
from vexillolinguist.color import parse_color

import argparse
import subprocess
import yaml

from vexillolinguist.utils import closest_matches

ROOT_DIR = Path(__file__).resolve().parent.parent
LANGUAGES_PATH = ROOT_DIR / 'resources' / 'languages.yml'

def main():
    parser = argparse.ArgumentParser(description='Flag-directed, language-aware Git repo initialization tool')
    parser.add_argument('--languages', type=Path, default=LANGUAGES_PATH, help="Path to the languages.yml used by GitHub's Linguist")
    parser.add_argument('-f', '--force', action='store_true', help='Force-overwrites the target directory. Use with care.')
    parser.add_argument('-o', '--output', type=Path, help='The path to the output directory for the Git repo to be created. Treated as a dry-run if left unspecified.')
    parser.add_argument('colors', type=str, nargs=argparse.ONE_OR_MORE, help='The color codes or names of the flag')

    args = parser.parse_args()

    print('==> Reading languages...')
    with open(args.languages, 'r') as f:
        langs = yaml.safe_load(f)
        lang_colors = {name: parse_color(lang['color']) for name, lang in langs.items() if 'color' in lang and 'extensions' in lang}
    
    print('==> Parsing colors...')
    flag_raw_colors = args.colors
    flag_size = len(flag_raw_colors)
    flag_colors = [parse_color(c) for c in flag_raw_colors]

    print('==> Matching colors...')
    flag_lang_names, _ = zip(*closest_matches(flag_colors, lang_colors.items(), dist=lambda c, entry: c.distance_to(entry[1])))
    flag_lang_exts = [langs[name]['extensions'][0] for name in flag_lang_names]
    print('\n'.join(f'    {color:>9} -> {lang:<16} ({ext})' for color, lang, ext in zip(flag_raw_colors, flag_lang_names, flag_lang_exts)))

    if args.output:
        output: Path = args.output

        if args.force and output.exists():
            print(f'==> Trashing directory at {output}...')
            send2trash(output)

        print('==> Creating Git repo...')
        output.mkdir(parents=True)
        subprocess.run(['git', 'init'], cwd=output, check=True)

        print('==> Creating files...')
        flag_lang_weights = [500 + flag_size - 1 - i for i in range(flag_size)]
        dummy_paths = [output / f'{i:04}{ext}' for i, ext in enumerate(flag_lang_exts)]

        for dummy_path, weight in zip(dummy_paths, flag_lang_weights):
            with open(dummy_path, 'w') as f:
                f.write('\n'.join(['# Probably not valid syntax'] * weight))

        with open(output / '.gitattributes', 'w') as f:
            f.write('\n'.join(f'*{ext} linguist-detectable' for ext in sorted(set(flag_lang_exts))))
        
        print('==> Committing files...')
        subprocess.run(['git', 'add', '.'], cwd=output, check=True)
        subprocess.run(['git', 'commit', '-m', 'Create a neat flag'], cwd=output, check=True)

        print(f'==> Done, created your repo at {output}. Try pushing it to GitHub!')
