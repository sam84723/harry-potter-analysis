import re
import requests
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple
import pandas as pd


def create_robust_english_dictionary() -> Set[str]:
    """Creates a comprehensive English dictionary using multiple sources"""
    print("Creating comprehensive English dictionary...")

    english_words = set()

    # Source 1: Complete online dictionary
    try:
        url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            online_words = set(response.text.strip().split('\n'))
            english_words.update(word.lower().strip() for word in online_words if word.strip())
            print(f"Main dictionary: {len(online_words)} words")
    except Exception as e:
        print(f"Main dictionary error: {e}")

    # Source 2: Top 10K most frequent English words
    try:
        url = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            frequent_words = set(response.text.strip().split())
            english_words.update(word.lower().strip() for word in frequent_words if word.strip())
            print(f"Frequent words: +{len(frequent_words)} words")
    except Exception as e:
        print(f"Frequent words error: {e}")

    # Essential words that MUST be in the dictionary
    essential_words = {
        # Body parts
        'eyes', 'eye', 'hands', 'hand', 'feet', 'foot', 'head', 'face', 'hair', 'arms', 'arm',
        'legs', 'leg', 'mouth', 'nose', 'ears', 'ear', 'back', 'chest', 'shoulder', 'shoulders',
        'fingers', 'finger', 'toes', 'toe', 'neck', 'throat', 'stomach', 'heart', 'brain',

        # Very common verbs - ALL forms
        'seem', 'seemed', 'seems', 'seeming', 'ask', 'asked', 'asks', 'asking',
        'hear', 'heard', 'hears', 'hearing', 'pull', 'pulled', 'pulls', 'pulling',
        'want', 'wanted', 'wants', 'wanting', 'happen', 'happened', 'happens', 'happening',
        'look', 'looked', 'looks', 'looking', 'talk', 'talked', 'talks', 'talking',
        'walk', 'walked', 'walks', 'walking', 'turn', 'turned', 'turns', 'turning',
        'move', 'moved', 'moves', 'moving', 'help', 'helped', 'helps', 'helping',

        # Time words
        'years', 'year', 'days', 'day', 'weeks', 'week', 'months', 'month',
        'hours', 'hour', 'minutes', 'minute', 'seconds', 'second', 'times', 'time',

        # Contractions
        'didn', 'doesn', 'wasn', 'weren', 'haven', 'hasn', 'hadn', 'wouldn',
        'couldn', 'shouldn', 'mustn', 'needn', 'daren', 'won', 'can', 'don',

        # Common adjectives
        'good', 'bad', 'great', 'small', 'big', 'large', 'little', 'old', 'new',
        'long', 'short', 'high', 'low', 'hot', 'cold', 'warm', 'cool', 'fast', 'slow',

        # Errors
        'wouldumbledore', 'isirius', 'nah', 'hmm', 'doin', 'vos', 'zis', 'zey', 'urgh', 'amr', 'igor',
        'ogwarts', 'mmm', 'hmmm', 'orrible', 'dyin', 'ryone', 'isit', 'inee', 'wiv', 'bilius', 'iful', 'teh', "eez"
        'lyin', 'eet', 'highpitched', 'aremember', 'vot', 'isurely', 'jokin', 'noooooo', 'shoulda', 'waitin',
        'readin', 'shhhh','yerselves','agrippa','studyin','pposed','isaid','isix','isays','streetlamp',
        'amad','aroun','woulda','aaargh','umbledore','makin','askin','eez','bleedin','nuthin','aaaah',
        'ced','musta','hidin','sittin','watchin','sorta','isomeone','istill','istop','havin','yerself',
        'killin', 'everythin', 'knowin', 'lyin', 'ishall', 'isomething', 'amolly', 'feelin', 'keepin',
        'ooooh', 'wandless', 'talkin', 'aaah', 'olympe', 'noticeboard', 'mornin', 'sayin', 'meself', 'isee',
        'amum', 'tryin', 'somethin',
        'ishut', 'gabrielle', 'oooh', 'nothin', 'lookin', 'comin', 'erm', 'gettin', 'amaybe', 'hannah',
        'goin', 'outta', 'morfin', 'ishe', 'wouldo', 'goodlooking', 'grimfaced', 'redfaced', 'twentyfour',
        'madeye', 'facetoface', 'lightningshaped',
        'nonmagical', 'upsidedown', 'longfingered', 'ginnys', 'visitin', 'sneakin', 'sleepin', 'amind', 'istudents',
        'enquiringly', 'ameaning', 'isince', 'iscourgify', 'ishh', 'unmistakeably', 'seein', 'ispect', 'happenin',
        'appened', 'choo', 'spellman', 'woodlice',
        'istand', 'unplottable', 'lettin', 'gotcha', 'oughta', 'innit', 'euan',
        'amorning', 'iind', 'sacrafice', 'theenk', 'brutalfaced', 'ihe', 'oldfashioned', 'lemme', 'halfbrother',
        'mudlike', 'unopoo', 'iind', 'lamplike', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
        '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
    }

    english_words.update(essential_words)

    # Generate conjugated forms
    print("Generating conjugated forms...")
    base_words = list(english_words)

    for word in base_words:
        if len(word) > 2:
            forms_to_add = generate_word_forms(word)
            english_words.update(forms_to_add)

    print(f"Final dictionary: {len(english_words)} English words")
    return english_words


def generate_word_forms(word: str) -> Set[str]:
    """Generates all possible forms of a word"""
    forms = set()
    word = word.lower().strip()

    if len(word) <= 2:
        return forms

    forms.add(word)

    # Plurals and 3rd person singular
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

    # Comparative and superlative
    if len(word) <= 6 and not word.endswith(('ing', 'ed', 'ly')):
        if word.endswith('y'):
            forms.add(word[:-1] + 'ier')
            forms.add(word[:-1] + 'iest')
        else:
            forms.add(word + 'er')
            forms.add(word + 'est')

    # Adverbs
    if not word.endswith(('ly', 'ing', 'ed')):
        if word.endswith('y'):
            forms.add(word[:-1] + 'ily')
        else:
            forms.add(word + 'ly')

    return forms


def create_exclusion_list() -> Set[str]:
    """Creates an exclusion list for obvious non-neologisms"""
    return {
        'london', 'england', 'britain', 'scotland', 'ireland', 'wales', 'europe',
        'america', 'australia', 'canada', 'france', 'germany', 'spain', 'italy',
        'smith', 'johnson', 'williams', 'jones', 'brown', 'davis', 'miller',
        'wilson', 'moore', 'taylor', 'anderson', 'thomas', 'jackson', 'white',
        'christmas', 'easter', 'halloween', 'monday', 'tuesday', 'wednesday',
        'thursday', 'friday', 'saturday', 'sunday', 'january', 'february',
        'march', 'april', 'june', 'july', 'august', 'september', 'october',
        'november', 'december', 'mr', 'mrs', 'ms', 'dr', 'prof',
        # Parsing errors
        'wouldumbledore', 'youknowwho', 'hewhomustnotbenamed', 'isirius'
    }


def clean_and_extract_words(text: str) -> List[str]:
    """Cleans text and extracts words with contraction handling"""
    text = text.lower()

    # Handle contractions
    contractions = {
        "don't": "do not", "won't": "will not", "can't": "cannot",
        "isn't": "is not", "wasn't": "was not", "weren't": "were not",
        "haven't": "have not", "hasn't": "has not", "hadn't": "had not",
        "wouldn't": "would not", "couldn't": "could not", "shouldn't": "should not",
        "'re": " are", "'ve": " have", "'ll": " will", "'d": " would",
        "'m": " am", "'s": " is", "it's": "it is", "he's": "he is"
    }

    for contraction, expansion in contractions.items():
        text = text.replace(contraction, expansion)

    text = re.sub(r"\w+n't", lambda m: m.group()[:-3] + " not", text)
    text = re.sub(r'[^a-z\s]', ' ', text)
    words = [word.strip() for word in text.split() if len(word.strip()) > 2]

    return words


def is_likely_neologism(word: str, english_dict: Set[str]) -> bool:
    """Determines if a word is likely a real neologism"""
    word = word.lower()

    # Common surnames to avoid
    common_surnames = {'smith', 'johnson', 'williams', 'jones', 'brown'}
    if word in common_surnames:
        return False

    # Known Harry Potter neologisms - ALWAYS accept
    known_hp_words = {
        'avada', 'kedavra', 'crucio', 'imperio', 'expelliarmus', 'expecto', 'patronum',
        'alohomora', 'lumos', 'nox', 'wingardium', 'leviosa', 'stupefy', 'protego',
        'riddikulus', 'accio', 'reparo', 'obliviate', 'voldemort', 'hogwarts',
        'gryffindor', 'slytherin', 'ravenclaw', 'hufflepuff', 'quidditch', 'muggle',
        'animagus', 'auror', 'pensieve', 'horcrux', 'dementor', 'azkaban'
    }

    if word in known_hp_words:
        return True

    # Check for Harry Potter patterns
    hp_patterns = ['wart', 'gryf', 'slyth', 'raven', 'huff', 'volde', 'dumble', 'mcgon']
    if any(pattern in word for pattern in hp_patterns):
        return True

    return True


def detect_neologisms(books: Dict[str, str], min_frequency: int = 2) -> Dict:
    """Detects neologisms using the improved system"""
    print("Enhanced neologism detection...")

    english_dict = create_robust_english_dictionary()
    exclusions = create_exclusion_list()

    # Force inclusion of Harry Potter spells
    hp_spells_override = {
        'avada', 'kedavra', 'crucio', 'imperio', 'patronum', 'lumos', 'nox',
        'expelliarmus', 'expecto', 'wingardium', 'leviosa', 'stupefy', 'protego',
        'riddikulus', 'accio', 'reparo', 'obliviate', 'sectusempra', 'confundus'
    }

    all_words = []
    book_words = {}

    for book_file, book_text in books.items():
        book_name = book_file.replace('.txt', '').replace('_', ' ').title()
        words = clean_and_extract_words(book_text)
        book_words[book_name] = words
        all_words.extend(words)

    all_word_counts = Counter(all_words)
    print(f"Total unique words: {len(all_word_counts)}")

    neologisms = {}
    false_positives = 0

    for word, count in all_word_counts.items():
        if count >= min_frequency and len(word) > 2:
            # Force inclusion of HP spells
            if word in hp_spells_override:
                neologisms[word] = count
            elif (word not in english_dict and
                  word not in exclusions and
                  is_likely_neologism(word, english_dict)):
                neologisms[word] = count
            else:
                false_positives += 1

    print(f"True neologisms detected: {len(neologisms)}")
    print(f"False positives avoided: {false_positives}")

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
            'neologism_counts': book_neologisms,
            'most_common_neologisms': Counter(book_neologisms).most_common(200)
        }

    return {
        'all_neologisms': neologisms,
        'book_analysis': book_analysis,
        'total_unique_neologisms': len(neologisms)
    }


def analyze_introduction_timeline(books: Dict[str, str], get_chapters_func,
                                  detected_neologisms: Set[str]) -> Dict:
    """Analyzes when neologisms are first introduced"""
    print("Analyzing neologism introduction timeline...")

    timeline_data = {
        'first_appearances': {},
        'chapter_analysis': {},
        'evolution_timeline': []
    }

    globally_seen = set()
    book_order = list(books.keys())

    for book_file in book_order:
        book_text = books[book_file]
        book_name = book_file.replace('.txt', '').replace('_', ' ').title()

        try:
            chapters = get_chapters_func(book_text)
            timeline_data['chapter_analysis'][book_name] = {}

            for chapter_idx, (title, subtitle, content) in enumerate(chapters, 1):
                if not content:
                    continue

                chapter_words = clean_and_extract_words(content)
                chapter_neologisms = [word for word in chapter_words if word in detected_neologisms]

                new_neologisms = []
                for neologism in set(chapter_neologisms):
                    if neologism not in globally_seen:
                        globally_seen.add(neologism)
                        new_neologisms.append(neologism)
                        timeline_data['first_appearances'][neologism] = (
                            book_name, chapter_idx, title or subtitle or f"Chapter {chapter_idx}"
                        )

                timeline_data['chapter_analysis'][book_name][chapter_idx] = {
                    'title': title or subtitle or f"Chapter {chapter_idx}",
                    'new_neologisms': new_neologisms,
                    'total_neologisms': len(chapter_neologisms)
                }

                if new_neologisms:
                    timeline_data['evolution_timeline'].append({
                        'book': book_name,
                        'chapter': chapter_idx,
                        'chapter_title': title or subtitle or f"Chapter {chapter_idx}",
                        'new_neologisms': new_neologisms,
                        'count': len(new_neologisms)
                    })

        except Exception as e:
            print(f"Error analyzing book {book_name}: {e}")
            continue

    print(f"Unique neologisms introduced: {len(globally_seen)}")
    return timeline_data


def categorize_neologisms(neologisms: Dict[str, int]) -> Dict[str, List[str]]:
    """Categorizes neologisms into different types"""
    categories = {
        'spells': [],
        'people': [],
        'places': [],
        'creatures': [],
        'objects': [],
        'concepts': [],
        'others': []
    }

    for word, count in neologisms.items():
        word_lower = word.lower()

        # Spells
        if word_lower in ['avada', 'kedavra', 'crucio', 'imperio', 'expelliarmus',
                          'patronum', 'alohomora', 'lumos', 'stupefy', 'protego']:
            categories['spells'].append(word)
        # People
        elif word_lower in ['voldemort', 'mcgonagall', 'umbridge', 'quirrell',
                            'longbottom', 'xenophilius', 'karkaroff']:
            categories['people'].append(word)
        # Places
        elif word_lower in ['hogwarts', 'gryffindor', 'slytherin', 'azkaban', 'hogsmeade']:
            categories['places'].append(word)
        # Creatures
        elif word_lower in ['crookshanks', 'fawkes', 'kreacher', 'dementor']:
            categories['creatures'].append(word)
        # Objects
        elif word_lower in ['horcrux', 'quidditch', 'pensieve', 'portkey']:
            categories['objects'].append(word)
        # Concepts
        elif word_lower in ['muggle', 'auror', 'animagus', 'parseltongue']:
            categories['concepts'].append(word)
        else:
            categories['others'].append(word)

    return {k: v for k, v in categories.items() if v}


def create_visualization(timeline_data: Dict, save_path: str = "neologisms_by_book.png"):
    """Creates a visualization of neologism introduction by book"""
    try:
        import matplotlib.pyplot as plt

        # Extract data
        books_stats = defaultdict(int)
        for word, (book, chapter, title) in timeline_data['first_appearances'].items():
            books_stats[book] += 1

        # Prepare data
        book_names = []
        new_words_count = []

        for book, count in books_stats.items():
            short_name = book.replace('Harry Potter And The ', '').replace('0', '')
            if 'Sorcerers Stone' in short_name:
                short_name = 'Sorcerer\'s Stone'
            elif 'Chamber Of Secrets' in short_name:
                short_name = 'Chamber of Secrets'
            elif 'Prisoner Of Azkaban' in short_name:
                short_name = 'Prisoner of Azkaban'
            elif 'Goblet Of Fire' in short_name:
                short_name = 'Goblet of Fire'
            elif 'Order Of The Phoenix' in short_name:
                short_name = 'Order of Phoenix'
            elif 'Half-Blood Prince' in short_name:
                short_name = 'Half-Blood Prince'
            elif 'Deathly Hallows' in short_name:
                short_name = 'Deathly Hallows'

            book_names.append(short_name)
            new_words_count.append(count)

        # Create plot
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(book_names)), new_words_count,
                       color=['#8B0000', '#FFD700', '#4169E1', '#228B22', '#FF6347', '#8A2BE2', '#FF1493'])

        plt.title('New Neologisms Introduced by Book\n(Harry Potter)',
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Books', fontsize=12, fontweight='bold')
        plt.ylabel('Number of New Neologisms', fontsize=12, fontweight='bold')

        # Add values on bars
        for i, (bar, count) in enumerate(zip(bars, new_words_count)):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                     str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)

        plt.xticks(range(len(book_names)), book_names, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()

        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Graph saved: {save_path}")

        return True

    except ImportError:
        print("Matplotlib not installed - cannot create graph")
        return False
    except Exception as e:
        print(f"Error creating graph: {e}")
        return False


def display_results(neologism_results: Dict, timeline_data: Dict):
    """Displays analysis results"""
    print(f"\n{'=' * 70}")
    print("HARRY POTTER NEOLOGISMS - COMPLETE ANALYSIS")
    print(f"{'=' * 70}")

    print(f"Total unique neologisms: {neologism_results['total_unique_neologisms']}")

    # Top neologisms
    print(f"\nTop 200 neologisms with first appearance:")
    sorted_neologisms = sorted(neologism_results['all_neologisms'].items(),
                               key=lambda x: x[1], reverse=True)

    for i, (word, count) in enumerate(sorted_neologisms[:500], 1):
        first_info = timeline_data['first_appearances'].get(word, ("Unknown", 0, ""))
        book, chapter, title = first_info
        book_short = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                             '').replace(
            '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
        print(f"  {i:2d}. {word:<15}: {count:4d} occurrences (1st: {book_short}, Ch.{chapter})")

    # Summary by book
    print(f"\nSummary by book:")
    for book_name, analysis in neologism_results['book_analysis'].items():
        ratio = (analysis['total_neologisms'] / analysis['total_words']) * 100
        book_short = book_name.replace('Harry Potter And The ', '')
        print(
            f"• {book_short}: {analysis['unique_neologisms']} unique, {analysis['total_neologisms']:,} total ({ratio:.1f}%)")

    # Timeline summary
    books_stats = defaultdict(int)
    for word, (book, chapter, title) in timeline_data['first_appearances'].items():
        books_stats[book] += 1

    print(f"\nNeologisms introduced by book:")
    for book, count in books_stats.items():
        print(f"  • {book}: {count} new neologisms")

    # Top creative chapters
    print(f"\nTop 5 most creative chapters:")
    sorted_timeline = sorted(timeline_data['evolution_timeline'],
                             key=lambda x: x['count'], reverse=True)

    for i, entry in enumerate(sorted_timeline[:5], 1):
        print(f"{i}. {entry['book']} - Ch.{entry['chapter']}: {entry['count']} new words")
        top_words = sorted(entry['new_neologisms'],
                           key=lambda x: neologism_results['all_neologisms'].get(x, 0),
                           reverse=True)
        print(f"   Top words: {', '.join(top_words[:6])}")


def run_complete_analysis(books: Dict[str, str], get_chapters_func,
                          min_frequency: int = 3, save_results: bool = True):
    """Runs the complete neologism analysis"""
    print("Complete Harry Potter neologism detection")

    # Detect neologisms
    neologism_results = detect_neologisms(books, min_frequency)

    # Analyze introduction timeline
    timeline_data = analyze_introduction_timeline(
        books, get_chapters_func, set(neologism_results['all_neologisms'].keys())
    )

    # Display results
    display_results(neologism_results, timeline_data)

    # Create visualization
    create_visualization(timeline_data)

    # # Categorize neologisms
    # categories = categorize_neologisms(neologism_results['all_neologisms'])
    # print(f"\nTop neologisms by category:")
    # for category, words in categories.items():
    #     if words:
    #         print(f"\n{category.upper()} ({len(words)} words):")
    #         sorted_words = sorted(words,
    #                               key=lambda x: neologism_results['all_neologisms'].get(x, 0),
    #                               reverse=True)
    #         print(f"  Top 5: {', '.join(sorted_words[:5])}")
    #
    # # Create DataFrames for export
    # if save_results:
    #     frequency_data = []
    #     for word, count in neologism_results['all_neologisms'].items():
    #         category = "others"
    #         for cat, words in categories.items():
    #             if word in words:
    #                 category = cat
    #                 break
    #
    #         first_book, first_chapter, chapter_title = timeline_data['first_appearances'].get(
    #             word, ("Unknown", 0, "Unknown")
    #         )
    #
    #         frequency_data.append({
    #             'neologism': word,
    #             'total_frequency': count,
    #             'category': category,
    #             'first_book': first_book,
    #             'first_chapter': first_chapter,
    #             'chapter_title': chapter_title
    #         })
    #
    #     df = pd.DataFrame(frequency_data)
    #     df.to_csv('harry_potter_neologisms.csv', index=False)
    #
    #     print(f"\nFiles saved:")
    #     print(f"  • harry_potter_neologisms.csv")
    #     print(f"  • neologisms_by_book.png")

    return neologism_results, timeline_data


# Usage
if __name__ == "__main__":
    from retrieval_and_cleaning import get_books_dataset, get_chapters

    books, names = get_books_dataset()

    neologism_results, timeline_data = run_complete_analysis(
        books, get_chapters, min_frequency=3, save_results=True
    )

    print(f"\nFINAL STATISTICS:")
    print(f"Unique neologisms detected: {len(neologism_results['all_neologisms'])}")
    print(f"Chapters with new neologisms: {len(timeline_data['evolution_timeline'])}")