import re
from collections import Counter
from typing import Dict, List, Tuple
import pandas as pd
from nltk.corpus import stopwords

from frequency_analysis_constants import ALIASES, HARRY_POTTER_COMPOUNDS, STOP_WORDS_HP, STOP_WORDS_GENERIC, STOP_NAMES


# Harry Potter-specific multi-word expressions to treat as a single token


def clean_and_tokenize(text: str) -> List[str]:
    """
    Clean the text and tokenize into words, handling compound expressions
    """
    # Convert to lowercase
    text = text.lower()

    # Replace compound expressions with their unified versions
    for original, replacement in HARRY_POTTER_COMPOUNDS:
        text = text.replace(original, replacement)

    # Remove punctuation, keep only letters and underscores
    text = re.sub(r'[^a-zA-Z_\s]', ' ', text)

    # Split into words
    words = text.split()

    STOP_WORDS = STOP_WORDS_GENERIC.union(STOP_WORDS_HP)

    # Filter stopwords and very short words (except compounds with _)
    filtered_words = []
    for word in words:
        if '_' in word:  # It's a compound word; keep it
            filtered_words.append(word)
        elif (word not in STOP_WORDS
              and word not in STOP_NAMES
              and len(word) > 2):
            filtered_words.append(word)

    return filtered_words


def analyze_book_words(book_text: str, book_name: str, top_n: int = 50) -> Dict:
    """
    Analyze the most frequent words in a single book
    """
    # Clean and tokenize
    words = clean_and_tokenize(book_text)

    # Count occurrences
    word_counts = Counter(words)

    # Get the most frequent words
    most_common = word_counts.most_common(top_n)

    return {
        'book_name': book_name,
        'total_words': len(words),
        'unique_words': len(word_counts),
        'most_common_words': most_common,
        'word_counts': dict(word_counts)
    }


def analyze_all_books(books: Dict[str, str], top_n: int = 50) -> Dict[str, Dict]:
    """
    Analyze all books and return a dictionary of results
    """
    results = {}

    for book_file, book_text in books.items():
        # print(f"Analyzing {book_file}...")

        # Clean the book name
        book_name = book_file.replace('.txt', '').replace('_', ' ').title()

        # Analyze the book
        analysis = analyze_book_words(book_text, book_name, top_n)
        results[book_name] = analysis

        # print(f"✅ {book_name}: {analysis['total_words']} words, "
        #       f"{analysis['unique_words']} unique words")

    return results


def display_top_words(results: Dict[str, Dict], top_n: int = 20):
    """
    Display the most frequent words for each book
    """
    for book_name, analysis in results.items():
        print(f"\n{'=' * 60}")
        print(f"📚 {book_name}")
        print(f"{'=' * 60}")
        print(f"Total words analyzed: {analysis['total_words']:,}")
        print(f"Unique words: {analysis['unique_words']:,}")
        print(f"\nTop {top_n} most frequent words:")
        print("-" * 40)

        for i, (word, count) in enumerate(analysis['most_common_words'][:top_n], 1):
            percentage = (count / analysis['total_words']) * 100
            # Format display of compound words
            display_word = word.replace('_', ' ').title() if '_' in word else word
            print(f"{i:2d}. {display_word:<20} : {count:4d} ({percentage:.2f}%)")


def create_comparison_dataframe(results: Dict[str, Dict], top_n: int = 20) -> pd.DataFrame:
    """
    Create a DataFrame to compare the most frequent words across books
    """
    all_data = []

    for book_name, analysis in results.items():
        for rank, (word, count) in enumerate(analysis['most_common_words'][:top_n], 1):
            percentage = (count / analysis['total_words']) * 100
            # Create a human-readable version of the word for the DataFrame
            display_word = word.replace('_', ' ').title() if '_' in word else word
            all_data.append({
                'book': book_name,
                'rank': rank,
                'word': word,  # Technical token for analysis
                'display_word': display_word,  # Readable version
                'count': count,
                'percentage': percentage,
                'total_words_in_book': analysis['total_words']
            })

    return pd.DataFrame(all_data)


def find_common_words_across_books(results: Dict[str, Dict], min_books: int = 3) -> List[Tuple[str, int]]:
    """
    Find words that frequently appear across multiple books
    """
    word_book_count = Counter()

    # Count in how many books each word appears in the top-N
    for book_name, analysis in results.items():
        top_words = [word for word, count in analysis['most_common_words']]
        for word in top_words:
            word_book_count[word] += 1

    # Keep words that appear in at least min_books
    common_words = [(word, count) for word, count in word_book_count.items()
                    if count >= min_books]

    return sorted(common_words, key=lambda x: x[1], reverse=True)


def run_word_analysis(books: Dict[str, str], top_n: int = 50):
    """
    Run the complete word analysis pipeline
    """
    print("🔍 Starting analysis of the most frequent words...")
    print(f"📝 Recognized compound expressions: {len(HARRY_POTTER_COMPOUNDS)}")

    # Analyze all books
    results = analyze_all_books(books, top_n)

    # Display results
    display_top_words(results, top_n)

    # Create a DataFrame for deeper analysis
    df_comparison = create_comparison_dataframe(results, top_n)

    # Find common words
    common_words = find_common_words_across_books(results, min_books=3)

    print(f"\n{'=' * 60}")
    print("🔗 Frequent words common to multiple books:")
    print(f"{'=' * 60}")
    for word, book_count in common_words[:15]:
        # Format display of compound words
        display_word = word.replace('_', ' ').title() if '_' in word else word
        print(f"{display_word:<20} : present in {book_count} books")

    return results, df_comparison


import re
import matplotlib.pyplot as plt
from collections import defaultdict


def find_frequency_of_the_word(search_term: str, books):
    """
    Count the frequency of a target word (including its aliases) in each book
    and display a graph of its occurrences across the series.

    :param target_word: the main word ("voldemort", "harry", etc.)
    :param books: dict {filename: text}

    Note If you are looking for a group of words, update the alias list
    e.g : Search = lord voldemort -> ("lord voldemort", "lord_voldemort"),
    """

    temp = search_term.split()
    if len(temp) > 1:
        target_word = search_term.replace(' ', '_')
    else:
        target_word = search_term

    results = {}

    for book_file, book_text in books.items():
        # Clean the book name
        book_name = book_file.replace('.txt', '').replace('_', ' ').title()

        text = book_text.lower()

        # Replace all aliases with the main target word
        for original, replacement in ALIASES:
            # if (replacement == target_word and target_word != original): # if the word we are looking shouldnt be changed
            if target_word == original: continue

            if target_word == replacement:
                text = text.replace(original, replacement)

        # Remove punctuation (keep only letters and underscores)
        text = re.sub(r'[^a-zA-Z_\s]', ' ', text)

        # Split into words
        words = text.split()

        # Count target word occurrences
        results[book_name] = sum(1 for word in words if word == target_word)

    # Print results
    for name, count in results.items():
        print(f"The word '{target_word}' was found {count} times in {name}")

    # Plot results
    book_names = list(results.keys())
    counts = list(results.values())

    plt.figure(figsize=(10, 6))
    plt.plot(book_names, counts, marker="o", linestyle="-", linewidth=2)
    plt.title(f"Frequency of '{search_term}' across the books", fontsize=14)
    plt.xlabel("Book", fontsize=12)
    plt.ylabel("Occurrences", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

    return results


# Example usage with your existing code
if __name__ == "__main__":

    from retrieval_and_cleaning import get_books_dataset
    books, names = get_books_dataset()

    # ------------------------ Dataset cleaning and frequency retrieval --------------------------------

    # results, df_comparison = run_word_analysis(books, 50)

    # # Optional: save the results
    # df_comparison.to_csv('harry_potter_word_analysis.csv', index=False)
    # print("\n💾 Results saved in 'harry_potter_word_analysis.csv'")

    # ----------------------- Finding frequency per words --------------------------------------

    find_frequency_of_the_word("harry", books)
    find_frequency_of_the_word("voldemort", books)
    # find_frequency_of_the_word("lord voldemort", books)
