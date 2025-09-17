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

def main():
    """Main function to run first chapters analysis"""
    print("Harry Potter First Chapters Neologisms Analysis")
    print("=" * 50)

    # Load data
    df = load_neologisms_data()
    if df is None:
        return

    # Analyze first chapters
    summary_data = analyze_first_chapters(df)
    if not summary_data:
        print("No first chapter data found")
        return

    # Display analysis
    display_first_chapters_analysis(summary_data)

    # Create visualizations
    create_first_chapters_plot(summary_data)
    create_frequency_comparison_plot(summary_data)

    # Find most creative chapters
    creative_chapters = find_most_creative_chapters(df)
    if not creative_chapters:
        print("No chapter data found")
        return

    # Display analysis
    print("\nMost Creative Chapter per Book:")
    print("=" * 40)

    for book, data in creative_chapters.items():
        book_short = book.replace('Harry Potter And The ', '')
        print(f"\n{book_short}:")
        print(f"  • Chapter {data['chapter']}: {data['count']} new neologisms")
        print(f"  • Total frequency: {data['total_frequency']} occurrences")
        print(f"  • Top neologisms: {', '.join([n['neologism'] for n in data['neologisms'][:5]])}")

    # Create visualization
    create_creative_chapters_plot(creative_chapters)

if __name__ == "__main__":
    main()