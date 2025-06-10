import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import seaborn as sns
from retrieval_and_cleaning import get_books_dataset, get_dialogues_dataset, get_characters_datasets
import os
import nltk
from nltk.corpus import stopwords
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
    
    # Save the plot
    plt.savefig('word_counts.png')
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
            max_words=100
        ).generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title)
        plt.tight_layout(pad=0)
        plt.savefig(filename)
        plt.close()
    
    # Create wordclouds
    create_wordcloud(first_book, 'Word Cloud - First Book', 'wordcloud_first_book.png')
    create_wordcloud(last_book, 'Word Cloud - Last Book', 'wordcloud_last_book.png')

def analyze_dialogues():
    """
    Analyze the dialogue dataset to show:
    1. Top 10 characters by number of dialogues
    2. Average dialogue length per character (for top 10)
    """
    dialogue_path = get_dialogues_dataset()
    
    # Read the dialogues CSV file
    dialogues_file = os.path.join(dialogue_path, 'Characters_Dialogue.csv')
    df = pd.read_csv(dialogues_file)
    
    # Count dialogues per character
    dialogue_counts = df['Character'].value_counts().head(10)
    
    # Calculate average dialogue length
    df['dialogue_length'] = df['Dialogue'].str.len()
    avg_length = df.groupby('Character')['dialogue_length'].mean()
    avg_length_top10 = avg_length[dialogue_counts.index]
    
    # Plot number of dialogues
    plt.figure(figsize=(12, 6))
    dialogue_counts.plot(kind='bar')
    plt.title('Top 10 Characters by Number of Dialogues')
    plt.xlabel('Character')
    plt.ylabel('Number of Dialogues')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('dialogue_counts.png')
    plt.close()
    
    # Plot average dialogue length
    plt.figure(figsize=(12, 6))
    avg_length_top10.plot(kind='bar')
    plt.title('Average Dialogue Length per Character (Top 10)')
    plt.xlabel('Character')
    plt.ylabel('Average Length (characters)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('avg_dialogue_length.png')
    plt.close()

def analyze_characters():
    """
    Analyze the characters dataset to show:
    1. Distribution of characters by house
    2. Blood status distribution
    """
    characters_path = get_characters_datasets()
    
    # Read the characters CSV file
    characters_file = os.path.join(characters_path, 'Characters.csv')
    df = pd.read_csv(characters_file)
    
    # Plot house distribution
    plt.figure(figsize=(10, 6))
    df['House'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Distribution of Characters by House')
    plt.axis('equal')
    plt.savefig('house_distribution.png')
    plt.close()
    
    # Plot blood status distribution
    plt.figure(figsize=(10, 6))
    df['Blood status'].value_counts().plot(kind='bar')
    plt.title('Distribution of Blood Status')
    plt.xlabel('Blood Status')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('blood_status_distribution.png')
    plt.close()

if __name__ == "__main__":
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
    
    print("\nAll sanity checks completed! Check the generated PNG files for visualizations.") 