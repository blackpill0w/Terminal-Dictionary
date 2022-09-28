#!/usr/bin/env python3

import argparse, requests, sys
try:
    from rich import print as rprint
    HIGHLIGHT: str = '[green]'
    END_HIGHLIGHT: str = '[/green]'
except ModuleNotFoundError:
    sys.stderr.write("WARNING: the rich library is not installed, output will be printed with no color.\n\n")
    HIGHLIGHT: str = '-> '
    END_HIGHLIGHT: str = '-> '
    rprint = print

# URL used to fetch word's data
# Usage: URL/word
DICTIONARY_URL = 'https://api.dictionaryapi.dev/api/v2/entries/en'

def get_word_data(word: str) -> list | None:
    '''
    Get word's data using freeDictionaryAPI.
    The data is a list containing json data.
    None is return if it is not a valid word.
    '''
    resp = requests.get(f'{DICTIONARY_URL}/{word}')
    if not resp.ok:
        return None
    else:
        return resp.json()

def format_word_data(word_data: list) -> str:
    '''
    Takes json data and returns a string to be displayed.
    '''
    res = ''
    for meaning in word_data[0]['meanings']:
        res += f'{HIGHLIGHT}{meaning["partOfSpeech"]}{END_HIGHLIGHT}\n'
        for definition in meaning['definitions']:
            res += f'{definition["definition"]}\n'
    return res

def main():
    parser = argparse.ArgumentParser(prog='dct', description='Look up english words definition from the terminal')
    parser.add_argument('word', help='word to be defined')
    parser.add_argument('-s', '--synonym', help='display synonyms', action='store_true')
    parser.add_argument('-a', '--antonym', help='display antonyms', action='store_true')
    parser.add_argument('-n', '--no-def',  help="don't display definition", action='store_true')
    args = parser.parse_args()

    if args.no_def and not (args.synonym or args.antonym):
        print('Error: using --no-def/-n requires --synonym/-s or --antonym/-a')
        exit(1)
    word_data = get_word_data(args.word)
    if word_data is None:
        print("Sorry, I couldn't find the word you are looking for.")
    else:
        rprint(format_word_data(word_data), end='')


if __name__ == '__main__':
    main()
