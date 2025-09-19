import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from typing import Dict, Any
import pandas as pd
from pathlib import Path


class NeologismVisualizer:
    """Creates essential neologism visualizations with organized file management"""

    def __init__(self, file_manager):
        self.file_manager = file_manager
        # Harry Potter book colors
        self.book_colors = [
            '#722F37',  # Gryffindor red
            '#D3A625',  # Hufflepuff yellow
            '#2A52BE',  # Ravenclaw blue
            '#0F4B0F',  # Slytherin green
            '#B22222',  # Dark red
            '#4B0082',  # Indigo
            '#DC143C'  # Crimson
        ]

    def create_all_plots(self, comprehensive_df: pd.DataFrame, analysis_data: Dict[str, Any]):
        """Create all 4 essential plots"""
        print("Creating essential neologism visualizations...")

        # Extract data needed for plots
        unique_counts, total_counts, book_names = self._extract_plot_data(comprehensive_df, analysis_data)

        # Create the 4 plots
        self.plot_unique_neologisms_by_book(unique_counts, book_names)
        self.plot_total_neologisms_by_book(total_counts, book_names)
        self.create_unique_wordclouds_by_book(comprehensive_df)
        self.create_total_wordclouds_by_book(comprehensive_df, analysis_data)

        print("All visualizations created successfully!")

    def _extract_plot_data(self, comprehensive_df: pd.DataFrame, analysis_data: Dict[str, Any]):
        """Extract data needed for plotting"""
        # Count unique neologisms (first appearances) by book
        unique_counts = comprehensive_df['first_book'].value_counts().to_dict()

        # Count total neologism usage by book
        total_counts = {}
        for book_name, book_data in analysis_data['book_analysis'].items():
            total_counts[book_name] = book_data['total_neologisms']

        # Get ordered book names
        book_order = [
            '01 Harry Potter And The Sorcerers Stone',
            '02 Harry Potter And The Chamber Of Secrets',
            '03 Harry Potter And The Prisoner Of Azkaban',
            '04 Harry Potter And The Goblet Of Fire',
            '05 Harry Potter And The Order Of The Phoenix',
            '06 Harry Potter And The Half-Blood Prince',
            '07 Harry Potter And The Deathly Hallows'
        ]

        # Clean book names for display
        clean_names = []
        for book in book_order:
            short_name = book.replace('Harry Potter And The ', '').replace('0', '').replace('1 ', '').replace('2 ',
                                                                                                              '').replace(
                '3 ', '').replace('4 ', '').replace('5 ', '').replace('6 ', '').replace('7 ', '')
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
            clean_names.append(short_name)

        return unique_counts, total_counts, clean_names

    def plot_unique_neologisms_by_book(self, unique_counts: Dict, book_names: list):
        """Plot 1: Number of unique neologisms created per book (first appearances)"""

        # Order data by book sequence
        book_order = [
            '01 Harry Potter And The Sorcerers Stone',
            '02 Harry Potter And The Chamber Of Secrets',
            '03 Harry Potter And The Prisoner Of Azkaban',
            '04 Harry Potter And The Goblet Of Fire',
            '05 Harry Potter And The Order Of The Phoenix',
            '06 Harry Potter And The Half-Blood Prince',
            '07 Harry Potter And The Deathly Hallows'
        ]

        counts = [unique_counts.get(book, 0) for book in book_order]

        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(book_names)), counts, color=self.book_colors)

        plt.title('Unique Neologisms Created per Book\n(First Appearances Only)',
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Books', fontsize=12, fontweight='bold')
        plt.ylabel('Number of New Neologisms Created', fontsize=12, fontweight='bold')

        # Add values on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            if count > 0:
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.01,
                         str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)

        plt.xticks(range(len(book_names)), book_names, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()

        # Save plot
        plot_path = self.file_manager.get_path('plot', 'unique_neologisms_by_book.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {plot_path}")
        plt.show()

    def plot_total_neologisms_by_book(self, total_counts: Dict, book_names: list):
        """Plot 2: Total neologism usage per book (all occurrences)"""

        book_order = [
            '01 Harry Potter And The Sorcerers Stone',
            '02 Harry Potter And The Chamber Of Secrets',
            '03 Harry Potter And The Prisoner Of Azkaban',
            '04 Harry Potter And The Goblet Of Fire',
            '05 Harry Potter And The Order Of The Phoenix',
            '06 Harry Potter And The Half-Blood Prince',
            '07 Harry Potter And The Deathly Hallows'
        ]

        counts = [total_counts.get(book, 0) for book in book_order]

        plt.figure(figsize=(14, 8))
        bars = plt.bar(range(len(book_names)), counts, color=self.book_colors)

        plt.title('Total Neologism Usage per Book\n(All Occurrences)',
                  fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Books', fontsize=12, fontweight='bold')
        plt.ylabel('Total Neologism Occurrences', fontsize=12, fontweight='bold')

        # Add values on bars
        for i, (bar, count) in enumerate(zip(bars, counts)):
            if count > 0:
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(counts) * 0.01,
                         f'{count:,}', ha='center', va='bottom', fontweight='bold', fontsize=10)

        plt.xticks(range(len(book_names)), book_names, rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.tight_layout()

        # Save plot
        plot_path = self.file_manager.get_path('plot', 'total_neologisms_by_book.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"Saved: {plot_path}")
        plt.show()

    def create_unique_wordclouds_by_book(self, comprehensive_df: pd.DataFrame):
        """WordCloud 1: Unique neologisms by book (first appearances only)"""
        try:
            from wordcloud import WordCloud

            # Group unique neologisms by first book
            unique_by_book = {}
            for _, row in comprehensive_df.iterrows():
                book = row['first_book']
                neologism = row['neologism']
                frequency = row['total_frequency']

                if book not in unique_by_book:
                    unique_by_book[book] = {}
                unique_by_book[book][neologism] = frequency

            # Create combined wordcloud plot
            fig, axes = plt.subplots(3, 3, figsize=(18, 16))
            fig.suptitle('Unique Neologisms by Book - Word Clouds\n(First Appearances Only)',
                         fontsize=20, fontweight='bold')
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
                if book in unique_by_book and unique_by_book[book]:
                    # Create color function for this book
                    book_color = self.book_colors[i]

                    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                        return book_color

                    wordcloud = WordCloud(
                        width=400, height=300, background_color='white',
                        color_func=color_func, max_words=50, relative_scaling=0.5,
                        random_state=42
                    ).generate_from_frequencies(unique_by_book[book])

                    axes_flat[i].imshow(wordcloud, interpolation='bilinear')
                    axes_flat[i].axis('off')

                    # Clean book name
                    book_short = book.replace('Harry Potter And The ', '').replace('0', '').replace('1 ', '').replace(
                        '2 ', '').replace('3 ', '').replace('4 ', '').replace('5 ', '').replace('6 ', '').replace('7 ',
                                                                                                                  '')
                    axes_flat[i].set_title(f'{book_short}\n({len(unique_by_book[book])} unique)',
                                           fontsize=12, fontweight='bold', pad=10)
                else:
                    axes_flat[i].text(0.5, 0.5, 'No unique\nneologisms', ha='center', va='center',
                                      fontsize=14, transform=axes_flat[i].transAxes)
                    axes_flat[i].axis('off')

            # Hide remaining subplots
            for j in range(len(book_order), len(axes_flat)):
                axes_flat[j].axis('off')

            plt.tight_layout()

            # Save wordcloud
            wc_path = self.file_manager.get_path('wordcloud', 'unique_neologisms_wordclouds.png')
            plt.savefig(wc_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {wc_path}")
            plt.show()

        except ImportError:
            print("WordCloud library not installed. Install with: pip install wordcloud")

    def create_total_wordclouds_by_book(self, comprehensive_df: pd.DataFrame, analysis_data: Dict):
        """WordCloud 2: Total neologism usage by book (all occurrences)"""
        try:
            from wordcloud import WordCloud

            # Use analysis_data for total usage per book
            total_by_book = {}
            for book_name, book_data in analysis_data['book_analysis'].items():
                total_by_book[book_name] = book_data['neologism_counts']

            # Create combined wordcloud plot
            fig, axes = plt.subplots(3, 3, figsize=(18, 16))
            fig.suptitle('Total Neologism Usage by Book - Word Clouds\n(All Occurrences)',
                         fontsize=20, fontweight='bold')
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
                if book in total_by_book and total_by_book[book]:
                    # Create color function for this book
                    book_color = self.book_colors[i]

                    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
                        return book_color

                    wordcloud = WordCloud(
                        width=400, height=300, background_color='white',
                        color_func=color_func, max_words=50, relative_scaling=0.5,
                        random_state=42
                    ).generate_from_frequencies(total_by_book[book])

                    axes_flat[i].imshow(wordcloud, interpolation='bilinear')
                    axes_flat[i].axis('off')

                    # Clean book name
                    book_short = book.replace('Harry Potter And The ', '').replace('0', '').replace('1 ', '').replace(
                        '2 ', '').replace('3 ', '').replace('4 ', '').replace('5 ', '').replace('6 ', '').replace('7 ',
                                                                                                                  '')
                    total_usage = sum(total_by_book[book].values())
                    axes_flat[i].set_title(f'{book_short}\n({total_usage:,} total uses)',
                                           fontsize=12, fontweight='bold', pad=10)
                else:
                    axes_flat[i].text(0.5, 0.5, 'No data', ha='center', va='center',
                                      fontsize=14, transform=axes_flat[i].transAxes)
                    axes_flat[i].axis('off')

            # Hide remaining subplots
            for j in range(len(book_order), len(axes_flat)):
                axes_flat[j].axis('off')

            plt.tight_layout()

            # Save wordcloud
            wc_path = self.file_manager.get_path('wordcloud', 'total_neologisms_wordclouds.png')
            plt.savefig(wc_path, dpi=300, bbox_inches='tight')
            print(f"Saved: {wc_path}")
            plt.show()

        except ImportError:
            print("WordCloud library not installed. Install with: pip install wordcloud")


# Fonction à ajouter dans run_comprehensive_analysis
def create_essential_visualizations(comprehensive_df, analysis_data, file_manager):
    """Create the 4 essential visualizations"""
    print("here")
    visualizer = NeologismVisualizer(file_manager)
    visualizer.create_all_plots(comprehensive_df, analysis_data)