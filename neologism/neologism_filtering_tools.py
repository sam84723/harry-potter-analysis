import re
import requests
from collections import Counter
from typing import Dict, List, Set

from neologism.file_manager import FileManager


class WordFusionManager:
    """Manages word fusions before text processing"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.fusions = self._load_word_fusions()

    def _load_word_fusions(self) -> Dict[str, str]:
        """Load word fusion rules"""
        fusions = self.file_manager.load_json('word_fusions_json', default={})

        # Default Harry Potter fusions
        defaults = {
            # Multi-word names/places
            # "you-know-who": "youknowwho",
            # "he-who-must-not-be-named": "hewhomustnotbenamed",
            "diagon alley": "diagon_alley",
            "knockturn alley": "knocktur_nalley",
            "privet drive": "privet_drive",
            "platform nine and three quarters": "platform_nine_and_three_quarters",
            "minister of magic": "minister_of_magic",

            # Hyphenated spells/concepts
            "anti-apparition": "anti_apparition",
            "anti-muggle": "anti_muggle",
            "half-blood": "half_blood",
            "pure-blood": "pure_blood",
            "mud-blood": "mud_blood",

            'death eaters': 'death_eaters',

            # Titles with spacing issues
            # "professor mcgonagall": "professormcgonagall",
            # "professor dumbledore": "professordumbledore",
            # "professor snape": "professorsnape",
        }

        # Add defaults if not present
        updated = False
        for pattern, replacement in defaults.items():
            if pattern not in fusions:
                fusions[pattern] = replacement
                updated = True

        if updated:
            self._save_word_fusions(fusions)

        return fusions

    def _save_word_fusions(self, fusions: Dict[str, str]):
        """Save word fusion rules"""
        path = self.file_manager.get_path('json', 'word_fusions.json')
        self.file_manager.save_json(fusions, 'json', 'word_fusions.json')
        print(f"Saved word fusions: {path}")

    def add_fusion_interactive(self):
        """Interactive fusion creation"""
        print("Current word fusions:")
        for pattern, replacement in self.fusions.items():
            print(f"  '{pattern}' → '{replacement}'")

        while True:
            pattern = input("\nEnter pattern to fuse (or 'done'): ").strip().lower()
            if pattern == 'done':
                break

            replacement = input(f"Replace '{pattern}' with: ").strip().lower()
            if replacement:
                self.fusions[pattern] = replacement
                print(f"Added: '{pattern}' → '{replacement}'")

        self._save_word_fusions(self.fusions)

    def get_fusions(self) -> Dict[str, str]:
        """Get current fusion rules"""
        return self.fusions.copy()

def clean_and_extract_words(text: str, word_fusions: Dict[str, str] = None) -> List[str]:
    """Cleans text and extracts words with pre-fusion and contraction handling"""
    text = text.lower()

    if word_fusions:
        for pattern, replacement in word_fusions.items():
            text = text.replace(pattern, replacement)

    contractions = {
        "don't": "do not", "won't": "will not", "can't": "cannot",
    }

    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)

    text = re.sub(r"\w+n't", lambda m: m.group()[:-3] + " not", text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = [word.strip() for word in text.split() if len(word.strip()) > 2]

    return words


class EnglishDictionary:
    """Handles English dictionary creation and word validation"""

    def __init__(self):
        self.words = set()
        self.exclusions = set()
        self._load_dictionary()
        self._load_exclusions()

    def _load_dictionary(self):
        """Creates comprehensive English dictionary"""
        print("Creating English dictionary...")

        # Try online sources
        self._load_online_dictionary()
        self._load_frequent_words()
        self._add_essential_words()
        self._generate_word_forms()

        print(f"Dictionary loaded: {len(self.words)} words")

    def _load_online_dictionary(self):
        """Load main online dictionary"""
        try:
            url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                words = set(response.text.strip().split('\n'))
                self.words.update(word.lower().strip() for word in words if word.strip())
                print(f"Main dictionary: {len(words)} words")
        except Exception as e:
            print(f"Main dictionary error: {e}")

    def _load_frequent_words(self):
        """Load frequent words"""
        try:
            url = "https://www.mit.edu/~ecprice/wordlist.10000"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                words = set(response.text.strip().split())
                self.words.update(word.lower().strip() for word in words if word.strip())
                print(f"Frequent words: +{len(words)} words")
        except Exception as e:
            print(f"Frequent words error: {e}")

    def _add_essential_words(self):
        """Add words that MUST be in dictionary"""
        essential = {
            # Body parts
            'eyes', 'eye', 'hands', 'hand', 'feet', 'foot', 'head', 'face', 'hair',
            'arms', 'arm', 'legs', 'leg', 'mouth', 'nose', 'ears', 'ear', 'back',
            'chest', 'shoulder', 'shoulders', 'fingers', 'finger', 'neck', 'throat',

            # Common verbs
            'seem', 'seemed', 'seems', 'ask', 'asked', 'asks', 'hear', 'heard',
            'pull', 'pulled', 'want', 'wanted', 'happen', 'happened', 'look', 'looked',
            'talk', 'talked', 'walk', 'walked', 'turn', 'turned', 'move', 'moved',

            # Time words
            'years', 'year', 'days', 'day', 'weeks', 'week', 'months', 'month',
            'hours', 'hour', 'minutes', 'minute', 'seconds', 'second', 'times', 'time',

            # Contractions
            'didn', 'doesn', 'wasn', 'weren', 'haven', 'hasn', 'hadn', 'wouldn',
            'couldn', 'shouldn', 'mustn', 'needn', 'won', 'can', 'don',

            # Common adjectives
            'good', 'bad', 'great', 'small', 'big', 'large', 'little', 'old', 'new',
            'long', 'short', 'high', 'low', 'hot', 'cold', 'warm', 'cool', 'fast', 'slow',

            # Parsing errors to exclude
            'wouldumbledore', 'isirius', 'nah', 'hmm', 'doin', 'vos', 'zis', 'zey',
            'urgh', 'ogwarts', 'mmm', 'hmmm', 'orrible', 'dyin', 'ryone', 'isit',
            'killin', 'everythin', 'knowin', 'lyin', 'feelin', 'keepin', 'talkin',
            'lookin', 'comin', 'gettin', 'goin', 'seein', 'happenin', 'tryin'
        }
        self.words.update(essential)

    def _generate_word_forms(self):
        """Generate conjugated forms for base words"""
        print("Generating word forms...")
        base_words = list(self.words)

        for word in base_words:
            if len(word) > 2:
                self.words.update(self._get_word_forms(word))

    def _get_word_forms(self, word: str) -> Set[str]:
        """Generate all forms of a word"""
        forms = {word}

        # Plurals
        if word.endswith('y') and len(word) > 2 and word[-2] not in 'aeiou':
            forms.add(word[:-1] + 'ies')
        elif word.endswith(('s', 'sh', 'ch', 'x', 'z')):
            forms.add(word + 'es')
        else:
            forms.add(word + 's')

        # Past tense
        if word.endswith('e'):
            forms.add(word + 'd')
        elif word.endswith('y') and len(word) > 2 and word[-2] not in 'aeiou':
            forms.add(word[:-1] + 'ied')
        else:
            forms.add(word + 'ed')

        # Present participle
        if word.endswith('e') and len(word) > 2 and not word.endswith('ee'):
            forms.add(word[:-1] + 'ing')
        else:
            forms.add(word + 'ing')

        return forms

    def _load_exclusions(self):
        """Load exclusion list"""
        self.exclusions = {
            'london', 'england', 'britain', 'scotland', 'ireland', 'wales',
            'america', 'australia', 'canada', 'france', 'germany', 'spain',
            'smith', 'johnson', 'williams', 'jones', 'brown', 'davis',
            'christmas', 'easter', 'halloween', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday', 'january', 'february',
            'march', 'april', 'june', 'july', 'august', 'september', 'october',
            'november', 'december', 'mr', 'mrs', 'ms', 'dr', 'prof'
        }

    def is_neologism_candidate(self, word: str) -> bool:
        """Check if word could be a neologism"""
        word = word.lower()

        # Known HP neologisms - always accept
        hp_words = {
            'avada', 'kedavra', 'crucio', 'imperio', 'expelliarmus', 'expecto', 'patronum',
            'alohomora', 'lumos', 'nox', 'wingardium', 'leviosa', 'stupefy', 'protego',
            'riddikulus', 'accio', 'reparo', 'obliviate', 'voldemort', 'hogwarts',
            'gryffindor', 'slytherin', 'ravenclaw', 'hufflepuff', 'quidditch', 'muggle',
            'animagus', 'auror', 'pensieve', 'horcrux', 'dementor', 'azkaban', 'harry'
        }

        if word in hp_words:
            return True

        # Check exclusions
        if word in self.exclusions:
            return False

        # Check if in English dictionary
        if word in self.words:
            return False

        # HP patterns
        hp_patterns = ['wart', 'gryf', 'slyth', 'raven', 'huff', 'volde', 'dumble', 'mcgon']
        if any(pattern in word for pattern in hp_patterns):
            return True

        return True


class NeologismDetector:
    """Main neologism detection logic with word fusion"""

    def __init__(self, file_manager: FileManager = None):
        self.dictionary = EnglishDictionary()
        if file_manager:
            self.word_fusion_manager = WordFusionManager(file_manager)
        else:
            self.word_fusion_manager = None

    def detect_neologisms(self, books: Dict[str, str], min_frequency: int = 2) -> Dict:
        """Detect neologisms with pre-fusion"""
        print("Detecting neologisms with word fusion...")

        # Get fusion rules
        word_fusions = None
        if self.word_fusion_manager:
            word_fusions = self.word_fusion_manager.get_fusions()
            if word_fusions:
                print(f"Applying {len(word_fusions)} word fusion rules...")

        # Extract all words with fusion
        all_words = []
        book_words = {}

        for book_file, book_text in books.items():
            book_name = book_file.replace('.txt', '').replace('_', ' ').title()
            # USE fusion here
            words = clean_and_extract_words(book_text, word_fusions)
            book_words[book_name] = words
            all_words.extend(words)

        # Count words
        word_counts = Counter(all_words)
        print(f"Total unique words: {len(word_counts)}")

        # Filter neologisms
        neologisms = {}
        for word, count in word_counts.items():
            if (count >= min_frequency and
                    len(word) > 2 and
                    self.dictionary.is_neologism_candidate(word)):
                neologisms[word] = count

        print(f"Neologisms detected: {len(neologisms)}")

        # Analyze by book
        book_analysis = {}
        for book_name, words in book_words.items():
            book_counts = Counter(words)
            book_neologisms = {word: count for word, count in book_counts.items()
                               if word in neologisms}

            book_analysis[book_name] = {
                'total_words': len(words),
                'total_neologisms': sum(book_neologisms.values()),
                'unique_neologisms': len(book_neologisms),
                'neologism_counts': book_neologisms
            }

        return {
            'all_neologisms': neologisms,
            'book_analysis': book_analysis,
            'total_unique_neologisms': len(neologisms)
        }