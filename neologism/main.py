#!/usr/bin/env python3
"""
Harry Potter Neologisms Analysis
Main entry point with organized file management
"""

import sys
import argparse
from pathlib import Path

from neologism.neologism_visualization import create_essential_visualizations

# Add project root to path if needed
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from retrieval_and_cleaning import get_books_dataset, get_chapters
from file_manager import FileManager
import pandas as pd


class OrganizedNeologismAnalyzer:
    """Main analyzer with organized file structure"""

    def __init__(self, base_dir: str = None):
        self.file_manager = FileManager(base_dir)
        self.books = None
        self.book_names = None
        self._setup()

    def _setup(self):
        """Setup analyzer with organized structure"""
        # Migrate any existing files
        migrated_count = self.file_manager.migrate_old_files()
        if migrated_count > 0:
            print(f"Migrated {migrated_count} files to organized structure")

        # Create documentation
        self.file_manager.create_readme()

        # Load data
        self._load_data()

    def _load_data(self):
        """Load Harry Potter books data"""
        print("Loading Harry Potter books...")
        try:
            self.books, self.book_names = get_books_dataset()
            print(f"Loaded {len(self.books)} books")
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)

    def run_timeline_analysis(self, min_frequency: int = 2, save_results: bool = True):
        """Run timeline analysis with organized file output"""
        print("\n" + "=" * 60)
        print("TIMELINE ANALYSIS")
        print("=" * 60)

        # Import here to avoid circular imports
        from neologism_hunt import run_timeline_analysis

        # Run analysis
        neologisms, timeline_data = run_timeline_analysis(
            self.books, get_chapters, min_frequency, save_results=False
        )

        if save_results:
            self._save_timeline_results(neologisms, timeline_data)

        self._display_timeline_results(neologisms, timeline_data)
        return neologisms, timeline_data

    def run_comprehensive_analysis(self, min_frequency: int = 2, save_results: bool = True):
        """Run comprehensive analysis with organized file output"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE BY-BOOK ANALYSIS")
        print("=" * 60)

        # Import here to avoid circular imports
        from neologism_hunt import run_comprehensive_analysis

        # Run analysis
        comprehensive_df, analysis_data = run_comprehensive_analysis(
            self.books, get_chapters, min_frequency, save_results=save_results
        )

        if save_results:
            self._save_comprehensive_results(comprehensive_df, analysis_data)


        self._display_comprehensive_results(comprehensive_df, analysis_data)
        return comprehensive_df, analysis_data

    def _save_timeline_results(self, neologisms, timeline_data):
        """Save timeline results to organized location"""
        data = []
        for word, count in neologisms.items():
            first_info = timeline_data['first_appearances'].get(word, ("Unknown", 0, ""))
            data.append({
                'neologism': word,
                'total_frequency': count,
                'first_book': first_info[0],
                'first_chapter': first_info[1],
                'chapter_title': first_info[2]
            })

        df = pd.DataFrame(data)
        csv_path = self.file_manager.get_path('neologisms_csv')
        df.to_csv(csv_path, index=False)

        print(f"Saved timeline results: {csv_path}")

    def _save_comprehensive_results(self, comprehensive_df, analysis_data):
        """Save comprehensive results to organized locations"""
        # Main comprehensive data
        csv_path = self.file_manager.get_path('comprehensive_csv')
        comprehensive_df.to_csv(csv_path, index=False)

        # Books summary
        summary_data = []
        for book, data in analysis_data['book_analysis'].items():
            summary_data.append({
                'book': book,
                'total_neologisms': data['total_neologisms'],
                'unique_neologisms': data['unique_neologisms'],
                'top_neologism': data['most_common'][0][0] if data['most_common'] else '',
                'top_frequency': data['most_common'][0][1] if data['most_common'] else 0
            })

        summary_df = pd.DataFrame(summary_data)
        summary_path = self.file_manager.get_path('books_summary_csv')
        summary_df.to_csv(summary_path, index=False)

        print(f"Saved comprehensive results: {csv_path}")
        print(f"Saved books summary: {summary_path}")

    def _display_timeline_results(self, neologisms, timeline_data):
        """Display timeline analysis results"""
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"Total unique neologisms: {len(neologisms)}")

        # Timeline summary
        books_stats = {}
        for word, (book, chapter, title) in timeline_data['first_appearances'].items():
            books_stats[book] = books_stats.get(book, 0) + 1

        print(f"\nNeologisms introduced by book:")
        for book, count in books_stats.items():
            short_name = book.replace('Harry Potter And The ', '').replace('01 ', '').replace('02 ', '')
            print(f"  • {short_name}: {count} new neologisms")

        # Top neologisms
        print(f"\nTop 10 most frequent neologisms:")
        sorted_neologisms = sorted(neologisms.items(), key=lambda x: x[1], reverse=True)
        for i, (word, count) in enumerate(sorted_neologisms[:10], 1):
            first_info = timeline_data['first_appearances'].get(word, ("Unknown", 0))
            book_short = first_info[0].replace('Harry Potter And The ', '')[:15]
            print(f"  {i:2d}. {word:<15}: {count:4d} occurrences (1st: {book_short})")

    def _display_comprehensive_results(self, comprehensive_df, analysis_data):
        """Display comprehensive analysis results"""
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"Total unique neologisms: {len(comprehensive_df)}")

        print(f"\nTop 10 most frequent neologisms:")
        for idx, row in comprehensive_df.head(10).iterrows():
            first_book_short = row['first_book'].replace('Harry Potter And The ', '')[:15]
            print(f"  {idx + 1:2d}. {row['neologism']:<15}: {row['total_frequency']:4d} total "
                  f"(in {row['books_present_in']} books, 1st: {first_book_short})")

        print(f"\nSummary by book:")
        for book_name, book_data in analysis_data['book_analysis'].items():
            book_short = book_name.replace('Harry Potter And The ', '')
            ratio = (book_data['total_neologisms'] / book_data.get('total_words', 1)) * 100
            print(f"  • {book_short}: {book_data['unique_neologisms']} unique, "
                  f"{book_data['total_neologisms']:,} total ({ratio:.1f}%)")

    def show_file_structure(self):
        """Display the organized file structure"""
        self.file_manager.print_structure()

        print("\n📄 Generated Files:")

        # CSV files
        csv_files = self.file_manager.get_all_csv_files()
        for name, path in csv_files.items():
            status = "✓ Exists" if path.exists() else "✗ Not generated yet"
            print(f"  {name}: {path.relative_to(self.file_manager.base_dir)} ({status})")

        # JSON config files
        print("\n⚙️ Configuration Files:")
        json_files = self.file_manager.get_all_json_files()
        for name, path in json_files.items():
            status = "✓ Exists" if path.exists() else "✗ Not created yet"
            print(f"  {name}: {path.relative_to(self.file_manager.base_dir)} ({status})")


def interactive_menu():
    """Interactive menu with file management"""
    analyzer = OrganizedNeologismAnalyzer()

    frequency = input("Minimum frequency (default 2): ").strip()
    min_freq = int(frequency) if frequency.isdigit() else 2


    print("\n" + "=" * 50)
    print("HARRY POTTER NEOLOGISMS ANALYSIS")
    print("=" * 50)
    print("Choose analysis type:")
    print("1. Timeline Analysis")
    print("2. Comprehensive By-Book Analysis")
    print("3. Both analyses")
    print("4. Show file structure")
    print("5. Clean old logs")

    choice = input("\nEnter your choice (1-6): ").strip()

    if choice == "1":
        analyzer.run_timeline_analysis(min_freq)

    elif choice == "2":
        analyzer.run_comprehensive_analysis(min_freq)

    elif choice == "3":
        analyzer.run_timeline_analysis(min_freq)
        analyzer.run_comprehensive_analysis(min_freq)

    elif choice == "4":
        analyzer.show_file_structure()

    elif choice == "5":
        analyzer.file_manager.cleanup_old_files()
        print("Old log files cleaned up")




def main():
    """Main entry point with organized file management"""
    parser = argparse.ArgumentParser(
        description="Harry Potter Neologisms Analysis - Organized Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
File Organization:
  config/user_decisions/     - JSON files with your manual choices
  results/csv/              - CSV analysis results  
  visualizations/plots/     - Generated charts
  visualizations/wordclouds/- Word cloud images
  logs/                     - Analysis execution logs

Examples:
  python main.py                          # Interactive menu
  python main.py --comprehensive         # By-book analysis
  python main.py --show-structure        # Display file organization
        """
    )

    parser.add_argument('--timeline', action='store_true',
                        help='Run timeline analysis')
    parser.add_argument('--comprehensive', action='store_true',
                        help='Run comprehensive by-book analysis')
    parser.add_argument('--both', action='store_true',
                        help='Run both analyses')
    parser.add_argument('--freq', type=int, default=2,
                        help='Minimum word frequency (default: 2)')
    parser.add_argument('--no-save', action='store_true',
                        help='Don\'t save results to files')
    parser.add_argument('--show-structure', action='store_true',
                        help='Show organized file structure')

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = OrganizedNeologismAnalyzer()

    # Handle special commands
    if args.show_structure:
        analyzer.show_file_structure()
        return

    # If no specific analysis chosen, run interactive menu
    if not any([args.timeline, args.comprehensive, args.both]):
        interactive_menu()
        return

    save_results = not args.no_save

    # Run requested analyses
    if args.both:
        analyzer.run_timeline_analysis(args.freq, save_results)
        analyzer.run_comprehensive_analysis(args.freq, save_results)

    elif args.timeline:
        analyzer.run_timeline_analysis(args.freq, save_results)

    elif args.comprehensive:
        analyzer.run_comprehensive_analysis(args.freq, save_results)

    print(f"\n✅ Analysis complete!")
    if save_results:
        analyzer.show_file_structure()


if __name__ == "__main__":
    try:
        # Force le menu interactif depuis PyCharm
        if len(sys.argv) == 1:  # Aucun argument
            interactive_menu()
        else:
            main()  # Arguments en ligne de commande
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)