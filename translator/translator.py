import requests
import sys
from bs4 import BeautifulSoup


class Translator:

    def __init__(self):
        self.LANGUAGES = {
            '0': 'all',
            '1': 'arabic',
            '2': 'german',
            '3': 'english',
            '4': 'spanish',
            '5': 'french',
            '6': 'hebrew',
            '7': 'japanese',
            '8': 'dutch',
            '9': 'polish',
            '10': 'portuguese',
            '11': 'romanian',
            '12': 'russian',
            '13': 'turkish',
        }
        self.base_url = 'https://context.reverso.net/translation'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.translations = None
        self.examples = None
        self.context = None

    """Main application loop."""
    def menu(self):
        # Grab input from console and initializes variables.
        context = {
            'source_lang': sys.argv[1],
            'dest_lang': sys.argv[2],
            'word': sys.argv[3],
        }

        # Makes sure selected languages are supported.
        if context['source_lang'] not in self.LANGUAGES.values():
            print(f"Sorry, the program doesn't support {context['source_lang']}")
            sys.exit()
        if context['dest_lang'] not in self.LANGUAGES.values():
            print(f"Sorry, the program doesn't support {context['dest_lang']}")
            sys.exit()

        self.context = context
        # Initialize read/write functions
        self.write_file()
        self.read_file()

        return None

    """Builds url and makes API request."""
    def context_translate(self, context):
        url = f'{self.base_url}/{context["source_lang"].lower()}-{context["dest_lang"].lower()}/{context["word"]}'
        r = requests.get(url, headers=self.headers)
        # Handles server errors.
        if r.status_code == 404:
            # Catches 'jabberwocky'.
            print(f'Sorry, unable to find {context["word"]}')
            sys.exit()
        elif r.status_code != 200:
            # Catches bad connection.
            print('Something wrong with your internet connection')
            sys.exit()

        self.clean_data(r)
        return None

    """Retrieves & formats data with bs4."""
    def clean_data(self, r):
        # Retrieves data from website HTML.
        soup = BeautifulSoup(r.content, 'html.parser')
        self.translations = soup.find('div', {'id': 'translations-content'}).text.split()
        raw_examples = soup.find('section', {'id': 'examples-content'}).text.split('\n')
        self.examples = [i.strip() + '\n' for i in raw_examples if i][:10]

        # Formats data.
        for i in range(len(self.examples)):
            if i % 2 == 0:
                self.examples[i] = self.examples[i].replace('\n', ':\n')
            else:
                self.examples[i] = self.examples[i].replace('\n', '\n\n')
        return None

    """Writes results to file."""
    def write_file(self):
        lang_list = [self.context['dest_lang']]
        if self.context['dest_lang'] == 'all':
            lang_list = [i for i in self.LANGUAGES.values() if i.lower() not in ['all', self.context['source_lang']]]
        with open(f'{self.context["word"]}.txt', 'w') as f:
            for i in lang_list:
                self.context['dest_lang'] = i
                self.context_translate(context=self.context)
                f.writelines(f'{i.title()} Translations:' + '\n' + '\n'.join(self.translations[:5]) + '\n\n' +
                             f'{i.capitalize()} Examples:' + '\n' + ''.join(self.examples))
            f.close()

    """Reads results from file."""
    def read_file(self):
        with open(f'{self.context["word"]}.txt', 'r') as f:
            print(f.read())


if __name__ == "__main__":
    tr = Translator()
    tr.menu()
