import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import seaborn as sns
from retrieval_and_cleaning import get_books_dataset, get_dialogues_dataset, get_characters_datasets
import os
import nltk
from nltk.corpus import stopwords


# 1. Define the name of the folder where plots will be saved.
PLOTS_DIR = "Plots"

# 2. Create the directory if it doesn't already exist.
os.makedirs(PLOTS_DIR, exist_ok=True)

# Download necessary NLTK data
nltk.download('stopwords')


def count_words_per_book():
    """
    Count and visualize the number of words in each Harry Potter book
    """
    books, names = get_books_dataset()
    word_counts = {}

    for book_name, text in books.items():
        # Clean book name for display
        clean_name = book_name.replace('.txt', '').replace('_', ' ')
        words = text.split()
        word_counts[clean_name] = len(words)

    # Create bar plot
    plt.figure(figsize=(12, 6))
    plt.bar(word_counts.keys(), word_counts.values())
    plt.xticks(rotation=45, ha='right')
    plt.title('Word Count per Harry Potter Book')
    plt.ylabel('Number of Words')
    plt.tight_layout()

    # Save the plot to the 'Plots' directory
    plt.savefig(os.path.join(PLOTS_DIR, 'word_counts.png'))
    plt.close()

    return word_counts


def generate_wordclouds():
    """
    Generate word clouds for the first and last Harry Potter books
    """
    books, names = get_books_dataset()
    sorted_names = sorted(names)
    first_book = books[sorted_names[0]]
    last_book = books[sorted_names[-1]]

    # Get stopwords
    stop_words = set(stopwords.words('english'))

    # Function to create and save wordcloud
    def create_wordcloud(text, title, filename):
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white',
            stopwords=stop_words,
            max_words=100,
        ).generate(text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.tight_layout(pad=0)
        # Save the plot to the 'Plots' directory
        plt.savefig(os.path.join(PLOTS_DIR, filename))
        plt.close()

    # Create wordclouds
    create_wordcloud(first_book, 'Word Cloud - First Book', 'wordcloud_first_book.png')
    create_wordcloud(last_book, 'Word Cloud - Last Book', 'wordcloud_last_book.png')


def analyze_dialogues():
    """
    Analyzes the dialogue dataset to find and plot the top 10 characters
    by their total number of words spoken.
    """
    dialogue_path = get_dialogues_dataset()
    dialogues_file = os.path.join(dialogue_path, 'harry_potter_characters_with_dialogues.csv')

    try:
        df = pd.read_csv(dialogues_file)
    except FileNotFoundError:
        print(f"Error: The file was not found at {dialogues_file}")
        return

    df['Number of Words'] = pd.to_numeric(df['Number of Words'], errors='coerce').fillna(0)
    total_word_counts = df.groupby('Character Name')['Number of Words'].sum()
    top_10_by_words = total_word_counts.sort_values(ascending=False).head(10)

    print("Top 10 Characters by Word Count:")
    print(top_10_by_words)

    plt.figure(figsize=(12, 7))
    top_10_by_words.plot(kind='bar', color='#4A6B8A')
    plt.title('Top 10 Characters by Total Number of Words Spoken')
    plt.xlabel('Character')
    plt.ylabel('Total Number of Words')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_filename = 'top_10_characters_by_words.png'
    # Save the plot to the 'Plots' directory
    plt.savefig(os.path.join(PLOTS_DIR, output_filename))
    plt.close()

    print(f"\nPlot saved as '{os.path.join(PLOTS_DIR, output_filename)}'")


def analyze_characters():
    """
    Analyze the characters dataset to show:
    1. Distribution of characters by house
    2. Blood status distribution
    """
    characters_path = get_characters_datasets()
    characters_file = os.path.join(characters_path, 'Characters.csv')
    df = pd.read_csv(characters_file, sep=';')

    # Plot house distribution
    plt.figure(figsize=(10, 6))
    df['House'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Characters by House')
    plt.axis('equal')
    # Save the plot to the 'Plots' directory
    plt.savefig(os.path.join(PLOTS_DIR, 'house_distribution.png'))
    plt.close()

    # Plot blood status distribution
    plt.figure(figsize=(10, 6))
    df['Blood status'].value_counts().plot(kind='bar')
    plt.title('Distribution of Blood Status')
    plt.xlabel('Blood Status')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the plot to the 'Plots' directory
    plt.savefig(os.path.join(PLOTS_DIR, 'blood_status_distribution.png'))
    plt.close()


def run_all_sanity_checks():
    # Run all sanity checks
    print("Running word count analysis...")
    word_counts = count_words_per_book()
    for book, count in word_counts.items():
        print(f"{book}: {count} words")

    print("\nGenerating word clouds...")
    generate_wordclouds()

    print("\nAnalyzing dialogues...")
    analyze_dialogues()

    print("\nAnalyzing characters...")
    analyze_characters()

    print(f"\nAll sanity checks completed! Check the generated PNG files in the '{PLOTS_DIR}/' folder.")