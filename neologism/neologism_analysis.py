import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict


def load_neologisms_data(csv_file: str = "harry_potter_neologisms.csv"):
    """Load neologisms data from CSV file"""
    try:
        df = pd.read_csv(csv_file)
        print(f"Loaded {len(df)} neologisms from {csv_file}")
        return df
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please run the main analysis first.")
        return None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def analyze_first_chapters(df):
    """Analyze neologisms introduced in first chapters only"""
    if df is None:
        return None

    # Filter for first chapters only
    first_chapters = df[df['first_chapter'] == 1].copy()

    print(f"Found {len(first_chapters)} neologisms introduced in first chapters")

    # Group by book
    books_data = defaultdict(list)

    for _, row in first_chapters.iterrows():
        book = row['first_book']
        neologism = row['neologism']
        frequency = row['total_frequency']
        books_data[book].append({
            'neologism': neologism,
            'frequency': frequency
        })

    # Create summary data
    summary = {}
    for book, neologisms in books_data.items():
        summary[book] = {
            'count': len(neologisms),
            'total_frequency': sum(n['frequency'] for n in neologisms),
            'neologisms': sorted(neologisms, key=lambda x: x['frequency'], reverse=True)
        }

    return summary


def find_most_creative_chapters(df):
    """Find the most creative chapter (most new neologisms) in each book"""
    if df is None:
        return None

    # Group by book and chapter
    chapter_stats = defaultdict(lambda: defaultdict(list))

    for _, row in df.iterrows():
        book = row['first_book']
        chapter = row['first_chapter']
        neologism = row['neologism']
        frequency = row['total_frequency']

        chapter_stats[book][chapter].append({
            'neologism': neologism,
            'frequency': frequency
        })

    # Find most creative chapter per book
    most_creative = {}

    for book, chapters in chapter_stats.items():
        max_count = 0
        best_chapter = None

        for chapter_num, neologisms in chapters.items():
            count = len(neologisms)
            if count > max_count:
                max_count = count
                best_chapter = {
                    'chapter': chapter_num,
                    'count': count,
                    'total_frequency': sum(n['frequency'] for n in neologisms),
                    'neologisms': sorted(neologisms, key=lambda x: x['frequency'], reverse=True)
                }

        if best_chapter:
            most_creative[book] = best_chapter

    return most_creative

def create_first_chapters_plot(summary_data, save_path: str = "first_chapters_neologisms.png"):
    """Create visualization for first chapters neologisms"""
    if not summary_data:
        print("No data to plot")
        return False

    # Prepare data for plotting
    book_names = []
    neologism_counts = []

    # Sort books chronologically
    book_order = [
        '01 Harry Potter And The Sorcerers Stone',
        '02 Harry Potter And The Chamber Of Secrets',
        '03 Harry Potter And The Prisoner Of Azkaban',
        '04 Harry Potter And The Goblet Of Fire',
        '05 Harry Potter And The Order Of The Phoenix',
        '06 Harry Potter And The Half-Blood Prince',
        '07 Harry Potter And The Deathly Hallows'
    ]

    for book in book_order:
        if book in summary_data:
            # Simplify book name
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                                 '').replace(
                '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
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
            neologism_counts.append(summary_data[book]['count'])
        else:
            # Handle missing books (no neologisms in first chapter)
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                                 '').replace(
                '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
            book_names.append(short_name)
            neologism_counts.append(0)

    # Create plot
    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(book_names)), neologism_counts,
                   color=['#722F37', '#D3A625', '#2A52BE', '#0F4B0F', '#B22222', '#4B0082', '#DC143C'])

    plt.title('New Neologisms Introduced in First Chapters\n(Harry Potter Series)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Books', fontsize=12, fontweight='bold')
    plt.ylabel('Number of New Neologisms in Chapter 1', fontsize=12, fontweight='bold')

    # Add values on bars
    for i, (bar, count) in enumerate(zip(bars, neologism_counts)):
        if count > 0:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                     str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.xticks(range(len(book_names)), book_names, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')

    # Set y-axis limits
    max_count = max(neologism_counts) if neologism_counts else 1
    plt.ylim(0, max_count * 1.15)

    plt.tight_layout()
    plt.tight_layout()
    plt.show()

    return True


def display_first_chapters_analysis(summary_data):
    """Display detailed analysis of first chapters"""
    if not summary_data:
        print("No data to display")
        return

    print("\n" + "=" * 70)
    print("FIRST CHAPTERS NEOLOGISMS ANALYSIS")
    print("=" * 70)

    total_first_chapter_neologisms = sum(data['count'] for data in summary_data.values())
    print(f"Total neologisms introduced in first chapters: {total_first_chapter_neologisms}")

    print(f"\nBreakdown by book:")
    for book, data in summary_data.items():
        book_short = book.replace('Harry Potter And The ', '')
        print(f"\n{book_short}:")
        print(f"  • {data['count']} new neologisms")
        print(f"  • Total frequency: {data['total_frequency']} occurrences")

        if data['neologisms']:
            print(f"  • Top neologisms: {', '.join([n['neologism'] for n in data['neologisms'][:5]])}")

            # Show detailed list
            print(f"  • All neologisms:")
            for neo in data['neologisms']:
                print(f"    - {neo['neologism']} ({neo['frequency']} occurrences)")


def create_frequency_comparison_plot(summary_data, save_path: str = "first_chapters_frequency.png"):
    """Create a plot comparing total frequency of neologisms introduced in first chapters"""
    if not summary_data:
        return False

    book_names = []
    total_frequencies = []

    # Sort books chronologically
    book_order = [
        '01 Harry Potter And The Sorcerers Stone',
        '02 Harry Potter And The Chamber Of Secrets',
        '03 Harry Potter And The Prisoner Of Azkaban',
        '04 Harry Potter And The Goblet Of Fire',
        '05 Harry Potter And The Order Of The Phoenix',
        '06 Harry Potter And The Half-Blood Prince',
        '07 Harry Potter And The Deathly Hallows'
    ]

    for book in book_order:
        if book in summary_data:
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                                 '').replace(
                '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
            book_names.append(short_name)
            total_frequencies.append(summary_data[book]['total_frequency'])
        else:
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                                 '').replace(
                '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
            book_names.append(short_name)
            total_frequencies.append(0)

    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(book_names)), total_frequencies,
                   color=['#8B4513', '#FFD700', '#4169E1', '#228B22', '#FF6347', '#8A2BE2', '#FF1493'])

    plt.title('Total Frequency of Neologisms Introduced in First Chapters\n(Harry Potter Series)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Books', fontsize=12, fontweight='bold')
    plt.ylabel('Total Frequency (All Occurrences)', fontsize=12, fontweight='bold')

    # Add values on bars
    for i, (bar, freq) in enumerate(zip(bars, total_frequencies)):
        if freq > 0:
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(total_frequencies) * 0.01,
                     str(freq), ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.xticks(range(len(book_names)), book_names, rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()

    return True


def create_creative_chapters_plot(creative_chapters):
    """Create visualization for most creative chapters"""
    book_names = []
    chapter_numbers = []
    neologism_counts = []

    book_order = [
        '01 Harry Potter And The Sorcerers Stone',
        '02 Harry Potter And The Chamber Of Secrets',
        '03 Harry Potter And The Prisoner Of Azkaban',
        '04 Harry Potter And The Goblet Of Fire',
        '05 Harry Potter And The Order Of The Phoenix',
        '06 Harry Potter And The Half-Blood Prince',
        '07 Harry Potter And The Deathly Hallows'
    ]

    for book in book_order:
        if book in creative_chapters:
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace('03 ',
                                                                                                                 '').replace(
                '04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
            book_names.append(f"{short_name}\n(Ch. {creative_chapters[book]['chapter']})")
            chapter_numbers.append(creative_chapters[book]['chapter'])
            neologism_counts.append(creative_chapters[book]['count'])

    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(book_names)), neologism_counts,
                   color=['#722F37', '#D3A625', '#2A52BE', '#0F4B0F', '#B22222', '#4B0082', '#DC143C'])

    plt.title('Most Creative Chapter per Book\n(Highest Number of New Neologisms)',
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Books', fontsize=12, fontweight='bold')
    plt.ylabel('Number of New Neologisms', fontsize=12, fontweight='bold')

    # Add values on bars
    for i, (bar, count) in enumerate(zip(bars, neologism_counts)):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                 str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)

    plt.xticks(range(len(book_names)), book_names, rotation=0, ha='center')
    plt.grid(axis='y', alpha=0.3, linestyle='--')
    plt.tight_layout()
    plt.show()


def create_wordclouds_by_book(df, save_images=False):
    """Create word clouds for neologisms by book with fixed colors"""
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        # Define fixed colors for each book
        book_colors = {
            '01 Harry Potter And The Sorcerers Stone': '#8B0000',  # Dark red
            '02 Harry Potter And The Chamber Of Secrets': '#228B22',  # Forest green
            '03 Harry Potter And The Prisoner Of Azkaban': '#4169E1',  # Royal blue
            '04 Harry Potter And The Goblet Of Fire': '#FF4500',  # Orange red
            '05 Harry Potter And The Order Of The Phoenix': '#8A2BE2',  # Blue violet
            '06 Harry Potter And The Half-Blood Prince': '#2F4F4F',  # Dark slate gray
            '07 Harry Potter And The Deathly Hallows': '#800080'  # Purple
        }

        # Group neologisms by book
        book_neologisms = {}

        for _, row in df.iterrows():
            book = row['first_book']
            neologism = row['neologism']
            frequency = row['total_frequency']

            if book not in book_neologisms:
                book_neologisms[book] = {}
            book_neologisms[book][neologism] = frequency

        # Create subplots for all word clouds
        fig, axes = plt.subplots(3, 3, figsize=(18, 16))
        fig.suptitle('Neologisms Word Clouds by Book', fontsize=20, fontweight='bold')

        # Flatten axes for easier indexing
        axes_flat = axes.flatten()

        book_order = [
            '01 Harry Potter And The Sorcerers Stone',
            '02 Harry Potter And The Chamber Of Secrets',
            '03 Harry Potter And The Prisoner Of Azkaban',
            '04 Harry Potter And The Goblet Of Fire',
            '05 Harry Potter And The Order Of The Phoenix',
            '06 Harry Potter And The Half-Blood Prince',
            '07 Harry Potter And The Deathly Hallows'
        ]

        for i, book in enumerate(book_order):
            if book in book_neologisms and book_neologisms[book]:
                # Create word cloud with fixed color
                base_color = book_colors[book]

                def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    return base_color

                wordcloud = WordCloud(
                    width=400,
                    height=300,
                    background_color='white',
                    color_func=color_func,
                    max_words=50,
                    relative_scaling=0.5,
                    random_state=42
                ).generate_from_frequencies(book_neologisms[book])

                # Plot word cloud
                axes_flat[i].imshow(wordcloud, interpolation='bilinear')
                axes_flat[i].axis('off')

                # Add title
                book_short = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace(
                    '03 ', '').replace('04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
                axes_flat[i].set_title(f'{book_short}\n({len(book_neologisms[book])} neologisms)',
                                       fontsize=12, fontweight='bold', pad=10)
            else:
                # Empty plot for missing data
                axes_flat[i].text(0.5, 0.5, 'No data', ha='center', va='center',
                                  fontsize=16, transform=axes_flat[i].transAxes)
                axes_flat[i].axis('off')

        # Hide remaining subplots
        for j in range(len(book_order), len(axes_flat)):
            axes_flat[j].axis('off')

        plt.tight_layout()

        if save_images:
            plt.savefig('neologisms_wordclouds_by_book.png', dpi=300, bbox_inches='tight')
            print("Word clouds saved as: neologisms_wordclouds_by_book.png")
        else:
            plt.show()

        return True

    except ImportError:
        print("WordCloud library not installed. Install with: pip install wordcloud")
        return False
    except Exception as e:
        print(f"Error creating word clouds: {e}")
        return False


def create_individual_wordclouds(df, save_images=False):
    """Create individual word cloud for each book in separate windows"""
    try:
        from wordcloud import WordCloud
        import matplotlib.pyplot as plt

        # Define fixed colors for each book
        book_colors = {
            '01 Harry Potter And The Sorcerers Stone': '#8B0000',
            '02 Harry Potter And The Chamber Of Secrets': '#228B22',
            '03 Harry Potter And The Prisoner Of Azkaban': '#4169E1',
            '04 Harry Potter And The Goblet Of Fire': '#FF4500',
            '05 Harry Potter And The Order Of The Phoenix': '#8A2BE2',
            '06 Harry Potter And The Half-Blood Prince': '#2F4F4F',
            '07 Harry Potter And The Deathly Hallows': '#800080'
        }

        # Group neologisms by book
        book_neologisms = {}

        for _, row in df.iterrows():
            book = row['first_book']
            neologism = row['neologism']
            frequency = row['total_frequency']

            if book not in book_neologisms:
                book_neologisms[book] = {}
            book_neologisms[book][neologism] = frequency

        book_order = [
            '01 Harry Potter And The Sorcerers Stone',
            '02 Harry Potter And The Chamber Of Secrets',
            '03 Harry Potter And The Prisoner Of Azkaban',
            '04 Harry Potter And The Goblet Of Fire',
            '05 Harry Potter And The Order Of The Phoenix',
            '06 Harry Potter And The Half-Blood Prince',
            '07 Harry Potter And The Deathly Hallows'
        ]

        for book in book_order:
            if book in book_neologisms and book_neologisms[book]:
                # Create individual word cloud
                base_color = book_colors[book]

                def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                    return base_color

                wordcloud = WordCloud(
                    width=800,
                    height=600,
                    background_color='white',
                    color_func=color_func,
                    max_words=100,
                    relative_scaling=0.5,
                    random_state=42
                ).generate_from_frequencies(book_neologisms[book])

                # Create individual plot
                plt.figure(figsize=(12, 8))
                plt.imshow(wordcloud, interpolation='bilinear')
                plt.axis('off')

                book_short = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '').replace(
                    '03 ', '').replace('04 ', '').replace('05 ', '').replace('06 ', '').replace('07 ', '')
                plt.title(f'{book_short} - Neologisms Word Cloud\n({len(book_neologisms[book])} unique neologisms)',
                          fontsize=16, fontweight='bold', pad=20)

                if save_images:
                    filename = f'wordcloud_{book_short.replace(" ", "_").replace("\'", "").lower()}.png'
                    plt.savefig(filename, dpi=300, bbox_inches='tight')
                    print(f"Saved: {filename}")
                else:
                    plt.show()

        return True

    except ImportError:
        print("WordCloud library not installed. Install with: pip install wordcloud")
        return False
    except Exception as e:
        print(f"Error creating word clouds: {e}")
        return False


def main():
    """Main function to run analysis"""
    print("Harry Potter Neologisms Analysis")
    print("=" * 40)

    # Load data
    df = load_neologisms_data()
    if df is None:
        return

    print("\nChoose analysis type:")
    print("1. Most creative chapters")
    print("2. Word clouds (combined view)")
    print("3. Word clouds (individual)")

    choice = input("Enter choice (1/2/3): ").strip()

    if choice == '1':
        # Your existing creative chapters code
        creative_chapters = find_most_creative_chapters(df)
        # ... rest of creative chapters analysis

    elif choice == '2':
        create_wordclouds_by_book(df, save_images=False)

    elif choice == '3':
        create_individual_wordclouds(df, save_images=False)

    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
