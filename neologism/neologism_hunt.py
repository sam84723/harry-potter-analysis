import json
import os
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple
import pandas as pd
from difflib import SequenceMatcher

from neologism.neologism_visualization import NeologismVisualizer, create_essential_visualizations
from neologism_filtering_tools import NeologismDetector, clean_and_extract_words
from file_manager import FileManager


class TimelineAnalyzer:
    """Analyzes when neologisms are first introduced"""

    def analyze_timeline(self, books: Dict[str, str], get_chapters_func,
                         detected_neologisms: Set[str]) -> Dict:
        """Analyze neologism introduction timeline"""
        print("Analyzing neologism timeline...")

        timeline_data = {
            'first_appearances': {},
            'chapter_analysis': {},
            'evolution_timeline': []
        }

        globally_seen = set()

        for book_file in books.keys():
            book_text = books[book_file]
            book_name = book_file.replace('.txt', '').replace('_', ' ').title()

            try:
                chapters = get_chapters_func(book_text)
                timeline_data['chapter_analysis'][book_name] = {}

                for chapter_idx, (title, subtitle, content) in enumerate(chapters, 1):
                    if not content:
                        continue

                    chapter_words = clean_and_extract_words(content)
                    chapter_neologisms = [word for word in chapter_words
                                          if word in detected_neologisms]

                    # Find new neologisms
                    new_neologisms = []
                    for neologism in set(chapter_neologisms):
                        if neologism not in globally_seen:
                            globally_seen.add(neologism)
                            new_neologisms.append(neologism)
                            timeline_data['first_appearances'][neologism] = (
                                book_name, chapter_idx,
                                title or subtitle or f"Chapter {chapter_idx}"
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
                print(f"Error analyzing {book_name}: {e}")

        return timeline_data


class BookAnalyzer:
    """Analyzes neologisms by book (comprehensive view)"""

    def analyze_by_book(self, books: Dict[str, str], get_chapters_func,
                        detected_neologisms: Set[str]) -> Dict:
        """Analyze ALL neologisms present in each book/chapter"""
        print("Analyzing all neologisms by book...")

        analysis_data = {
            'book_analysis': {},
            'chapter_analysis': {},
            'first_appearances': {}
        }

        globally_seen = set()

        for book_file in books.keys():
            book_text = books[book_file]
            book_name = book_file.replace('.txt', '').replace('_', ' ').title()

            # Book-level analysis
            book_words = clean_and_extract_words(book_text)
            book_neologisms = [word for word in book_words if word in detected_neologisms]
            book_counts = Counter(book_neologisms)

            analysis_data['book_analysis'][book_name] = {
                'total_words': len(book_words),
                'total_neologisms': len(book_neologisms),
                'unique_neologisms': len(book_counts),
                'neologism_counts': dict(book_counts),
                'most_common': book_counts.most_common(20)
            }

            # Chapter-level analysis
            try:
                chapters = get_chapters_func(book_text)
                chapter_data = {}

                for chapter_idx, (title, subtitle, content) in enumerate(chapters, 1):
                    if not content:
                        continue

                    chapter_words = clean_and_extract_words(content)
                    chapter_neologisms = [word for word in chapter_words
                                          if word in detected_neologisms]
                    chapter_counts = Counter(chapter_neologisms)

                    # Track first appearances
                    new_neologisms = []
                    for neologism in set(chapter_neologisms):
                        if neologism not in globally_seen:
                            globally_seen.add(neologism)
                            new_neologisms.append(neologism)
                            analysis_data['first_appearances'][neologism] = {
                                'book': book_name,
                                'chapter': chapter_idx,
                                'title': title or subtitle or f"Chapter {chapter_idx}"
                            }

                    chapter_data[chapter_idx] = {
                        'title': title or subtitle or f"Chapter {chapter_idx}",
                        'total_neologisms': len(chapter_neologisms),
                        'unique_neologisms': len(chapter_counts),
                        'new_neologisms': new_neologisms,
                        'all_neologisms': dict(chapter_counts),
                        'most_common': chapter_counts.most_common(10)
                    }

                analysis_data['chapter_analysis'][book_name] = chapter_data

            except Exception as e:
                print(f"Error analyzing chapters for {book_name}: {e}")

        return analysis_data

    def create_comprehensive_dataset(self, books: Dict[str, str], get_chapters_func,
                                     detected_neologisms: Dict[str, int]) -> pd.DataFrame:
        """Create comprehensive dataset with frequency by book"""
        analysis_data = self.analyze_by_book(
            books, get_chapters_func, set(detected_neologisms.keys())
        )

        dataset_rows = []

        for neologism, total_freq in detected_neologisms.items():
            # First appearance info
            first_info = analysis_data['first_appearances'].get(neologism)
            if first_info:
                first_book = first_info['book']
                first_chapter = first_info['chapter']
                first_title = first_info['title']
            else:
                first_book = "Unknown"
                first_chapter = 0
                first_title = "Unknown"

            # Book frequencies
            row = {
                'neologism': neologism,
                'total_frequency': total_freq,
                'first_book': first_book,
                'first_chapter': first_chapter,
                'first_chapter_title': first_title,
            }

            # Add frequency per book
            book_occurrences = {}
            for book_name, book_data in analysis_data['book_analysis'].items():
                freq = book_data['neologism_counts'].get(neologism, 0)
                book_occurrences[book_name] = freq
                safe_name = book_name.replace(' ', '_').replace('And', 'and')
                row[f'freq_{safe_name}'] = freq

            # Statistics
            row['books_present_in'] = sum(1 for count in book_occurrences.values() if count > 0)
            row['max_freq_per_book'] = max(book_occurrences.values()) if book_occurrences else 0

            dataset_rows.append(row)

        df = pd.DataFrame(dataset_rows)
        return df.sort_values('total_frequency', ascending=False).reset_index(drop=True), analysis_data


class ManagedSimilarityMatcher:
    """Handles detection and merging of similar neologisms with file management"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.saved_decisions = file_manager.load_json('merge_decisions_json', default={})

    def _save_decisions(self):
        """Save merge decisions using file manager"""
        self.file_manager.save_json(self.saved_decisions, 'merge_decisions_json')
        print(f"Saved decisions to {self.file_manager.get_path('merge_decisions_json')}")

    def _similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity between two words"""
        return SequenceMatcher(None, word1.lower(), word2.lower()).ratio()

    def find_similar_groups(self, neologisms: Dict[str, int],
                            threshold: float = 0.8) -> List[List[str]]:
        """Find groups of similar words"""
        words = list(neologisms.keys())
        similar_groups = []
        processed = set()

        for i, word1 in enumerate(words):
            if word1 in processed:
                continue

            group = [word1]
            for word2 in words[i + 1:]:
                if word2 in processed:
                    continue

                if self._similarity(word1, word2) >= threshold:
                    group.append(word2)
                    processed.add(word2)

            if len(group) > 1:
                similar_groups.append(group)
            processed.add(word1)

        return similar_groups

    def merge_similar_neologisms(self, neologisms: Dict[str, int]) -> Dict[str, int]:
        """Merge similar neologisms based on user decisions"""
        similar_groups = self.find_similar_groups(neologisms)
        merged = dict(neologisms)
        new_decisions = False

        for group in similar_groups:
            group_key = '|'.join(sorted(group))

            # Check saved decisions
            if group_key in self.saved_decisions:
                decision = self.saved_decisions[group_key]
                if decision['action'] in ['merge', 'manual'] and decision['canonical']:
                    canonical = decision['canonical']
                    if canonical in group:
                        total_count = sum(neologisms[word] for word in group if word in neologisms)
                        for word in group:
                            if word != canonical and word in merged:
                                del merged[word]
                        merged[canonical] = total_count
                        print(f"Applied saved decision: merged {group} -> {canonical}")
                continue

            # Ask user for new decision
            print(f"\nSimilar words: {group}")
            for i, word in enumerate(group):
                print(f"  {i + 1}. {word} ({neologisms.get(word, 0)} occurrences)")

            choice = input("Action (m=merge into most frequent, s=separate, c=choose): ").lower()

            decision = {'original_group': group, 'action': 'separate', 'canonical': None}

            if choice == 'm':
                canonical = max(group, key=lambda x: neologisms.get(x, 0))
                total_count = sum(neologisms[word] for word in group)
                for word in group:
                    if word != canonical and word in merged:
                        del merged[word]
                merged[canonical] = total_count
                decision.update({'action': 'merge', 'canonical': canonical})
                print(f"Merged into: {canonical}")

            elif choice == 'c':
                for i, word in enumerate(group):
                    print(f"  {i + 1}. {word}")
                try:
                    idx = int(input("Choose canonical (number): ")) - 1
                    if 0 <= idx < len(group):
                        canonical = group[idx]
                        total_count = sum(neologisms[word] for word in group)
                        for word in group:
                            if word != canonical and word in merged:
                                del merged[word]
                        merged[canonical] = total_count
                        decision.update({'action': 'manual', 'canonical': canonical})
                        print(f"Merged into: {canonical}")
                except (ValueError, IndexError):
                    print("Invalid choice, keeping separate")

            self.saved_decisions[group_key] = decision
            new_decisions = True

        if new_decisions:
            self._save_decisions()

        return merged


class ManagedBlacklistFilter:
    """Handles blacklist filtering with file management"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.blacklist = set(file_manager.load_json('blacklist_json', default=[]))

    def _save_blacklist(self):
        """Save blacklist using file manager"""
        self.file_manager.save_json(sorted(list(self.blacklist)), 'blacklist_json')
        print(f"Updated blacklist: {self.file_manager.get_path('blacklist_json')}")

    def filter_neologisms(self, neologisms: Dict[str, int]) -> Dict[str, int]:
        """Filter out blacklisted words and allow user to add new ones"""
        # Remove already blacklisted
        filtered = {word: count for word, count in neologisms.items()
                    if word.lower() not in self.blacklist}

        removed = len(neologisms) - len(filtered)
        if removed > 0:
            print(f"Removed {removed} blacklisted words")

        # Interactive review
        print("\nReviewing neologisms (batches of 20)...")
        sorted_words = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
        new_blacklist_words = set()

        for i in range(0, len(sorted_words), 20):
            batch = sorted_words[i:i + 20]

            print(f"\nBatch {i // 20 + 1}:")
            for j, (word, count) in enumerate(batch, i + 1):
                print(f"  {j:2d}. {word:<20} ({count} occurrences)")

            choice = input("Action (r=remove words, n=next, s=skip remaining): ").lower()

            if choice == 'r':
                remove_input = input("Word numbers to remove (e.g., 1,3,5): ")
                try:
                    indices = [int(x.strip()) for x in remove_input.split(',')]
                    for idx in indices:
                        if i + 1 <= idx <= min(i + 20, len(sorted_words)):
                            word_to_remove = sorted_words[idx - 1][0]
                            new_blacklist_words.add(word_to_remove.lower())
                            print(f"Marked for removal: {word_to_remove}")
                except ValueError:
                    print("Invalid input")
            elif choice == 's':
                break

        # Remove marked words
        for word in list(filtered.keys()):
            if word.lower() in new_blacklist_words:
                del filtered[word]

        if new_blacklist_words:
            self.blacklist.update(new_blacklist_words)
            self._save_blacklist()
            print(f"Added {len(new_blacklist_words)} words to blacklist")

        return filtered


class ManagedCompoundCombiner:
    """Handles combination of compound neologisms with file management"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.compounds = file_manager.load_json('compound_rules_json', default={})

        # Add default HP compounds if not present
        defaults = {
            "avada kedavra": ["avada", "kedavra"],
            "expecto patronum": ["expecto", "patronum"],
            "wingardium leviosa": ["wingardium", "leviosa"],
            "sirius black": ["sirius", "black"],
            "hermione granger": ["hermione", "granger"],
            "neville longbottom": ["neville", "longbottom"]
        }

        updated = False
        for compound, components in defaults.items():
            if compound not in self.compounds:
                self.compounds[compound] = components
                updated = True

        if updated:
            self._save_compounds()

    def _save_compounds(self):
        """Save compound rules using file manager"""
        self.file_manager.save_json(self.compounds, 'compound_rules_json')
        print(f"Saved compounds: {self.file_manager.get_path('compound_rules_json')}")

    def combine_compounds(self, neologisms: Dict[str, int]) -> Dict[str, int]:
        """Combine compound neologisms and preserve component information"""
        combined = dict(neologisms)
        created = []
        new_compounds = False

        for compound_name, components in self.compounds.items():
            found_components = {comp: combined.get(comp, 0) for comp in components
                                if comp in combined}

            if found_components:
                print(f"\nFound compound '{compound_name}': {list(found_components.keys())}")
                choice = input("Combine? (y/n): ")

                if choice.lower() == 'y':
                    # CORRECTION: Use the frequency of the most frequent component
                    # (rather than minimum, as it's more representative)
                    compound_freq = max(found_components.values())

                    # Remove individual components
                    for comp in components:
                        if comp in combined:
                            del combined[comp]

                    # Add the compound with preserved frequency
                    combined[compound_name] = compound_freq
                    created.append(compound_name)
                    print(f"Created: {compound_name} ({compound_freq} occurrences)")

        # Interactive creation
        print(f"\nAvailable neologisms for new compounds:")
        sorted_neo = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        for i, (word, count) in enumerate(sorted_neo[:20], 1):
            print(f"  {i:2d}. {word} ({count})")

        while True:
            user_input = input("\nCreate compound? (space-separated words or 'done'): ").strip()
            if user_input.lower() == 'done':
                break

            components = [w.strip().lower() for w in user_input.split() if w.strip()]
            if len(components) < 2:
                print("Need at least 2 components")
                continue

            found_components = {comp: combined.get(comp, 0) for comp in components
                                if comp in combined}

            if not found_components:
                print("No components found as neologisms")
                continue

            compound_name = ' '.join(components)

            # CORRECTION: Preserve the best information
            max_freq = max(found_components.values())
            best_component = max(found_components.keys(), key=lambda x: found_components[x])

            print(f"Creating compound '{compound_name}' from:")
            for comp, count in found_components.items():
                marker = " (will use this info)" if comp == best_component else ""
                print(f"  • {comp}: {count} occurrences{marker}")

            confirm = input(f"Confirm creation? (y/n): ")

            if confirm.lower() == 'y':
                # Remove the components
                for comp in components:
                    if comp in combined:
                        del combined[comp]

                # Add the compound with the best information
                combined[compound_name] = max_freq
                self.compounds[compound_name] = components
                created.append(compound_name)
                new_compounds = True
                print(f"Created: '{compound_name}' ({max_freq} occurrences)")

        if new_compounds:
            self._save_compounds()

        if created:
            print(f"Created {len(created)} compounds")

        return combined

# Main analysis functions with file management
def run_timeline_analysis(books: Dict[str, str], get_chapters_func,
                          min_frequency: int = 3, save_results: bool = True,
                          file_manager: FileManager = None):
    """Run timeline-based analysis with organized file management"""
    if file_manager is None:
        file_manager = FileManager()

    print("Timeline Analysis")

    # Detect neologisms
    detector = NeologismDetector()
    results = detector.detect_neologisms(books, min_frequency)

    # Filter and process with managed classes
    blacklist_filter = ManagedBlacklistFilter(file_manager)
    filtered = blacklist_filter.filter_neologisms(results['all_neologisms'])

    similarity_matcher = ManagedSimilarityMatcher(file_manager)
    merged = similarity_matcher.merge_similar_neologisms(filtered)

    # compound_combiner = ManagedCompoundCombiner(file_manager)
    # final_neologisms = compound_combiner.combine_compounds(merged)
    final_neologisms = merged

    # Timeline analysis
    timeline_analyzer = TimelineAnalyzer()
    timeline_data = timeline_analyzer.analyze_timeline(
        books, get_chapters_func, set(final_neologisms.keys())
    )

    return final_neologisms, timeline_data


def run_comprehensive_analysis(books: Dict[str, str], get_chapters_func,
                               min_frequency: int = 3, save_results: bool = True,
                               file_manager: FileManager = None):
    """Run comprehensive by-book analysis with proper compound handling"""
    if file_manager is None:
        file_manager = FileManager()

    print("Comprehensive By-Book Analysis")

    # Detect neologisms
    detector = NeologismDetector()
    results = detector.detect_neologisms(books, min_frequency)

    # Filter and process
    blacklist_filter = ManagedBlacklistFilter(file_manager)
    filtered = blacklist_filter.filter_neologisms(results['all_neologisms'])

    similarity_matcher = ManagedSimilarityMatcher(file_manager)
    merged = similarity_matcher.merge_similar_neologisms(filtered)

    # Calculate detailed information
    print("\nCalculating detailed information...")
    book_analyzer = BookAnalyzer()
    pre_compound_df, pre_compound_analysis = book_analyzer.create_comprehensive_dataset(
        books, get_chapters_func, merged
    )

    # COMPOUNDS DISABLED - no combination
    final_neologisms = merged
    compound_mapping = {}  # Empty because no compounds

    # No need for create_final_dataset_with_preserved_info()
    # because no compounds to preserve
    final_df = pre_compound_df  # Use the calculated dataset directly

    # No need to recalculate the analysis
    final_analysis_data = pre_compound_analysis
    if save_results:
        # Create essential visualizations
        create_essential_visualizations(final_df, final_analysis_data, file_manager)


    return final_df, final_analysis_data


def create_final_dataset_with_preserved_info(final_neologisms: Dict[str, int],
                                             original_df: pd.DataFrame,
                                             compound_mapping: Dict[str, List[str]]) -> pd.DataFrame:
    """Create final dataset preserving information from compound components"""
    final_rows = []

    for neologism, frequency in final_neologisms.items():
        if neologism in compound_mapping:
            # It's a compound - use the main component's information
            components = compound_mapping[neologism]

            # Find the component with the most info/frequency
            component_data = []
            for comp in components:
                comp_row = original_df[original_df['neologism'] == comp]
                if not comp_row.empty:
                    component_data.append(comp_row.iloc[0])

            if component_data:
                # Use the most frequent component's data
                best_component = max(component_data, key=lambda x: x['total_frequency'])

                # Create the compound row while preserving the best component's info
                row = best_component.to_dict()
                row['neologism'] = neologism
                row['total_frequency'] = frequency

                # Combine the components' frequencies by book
                for col in row.keys():
                    if col.startswith('freq_'):
                        # Add up the frequencies of all components for this book
                        combined_freq = sum(
                            comp_data.get(col, 0) for comp_data in
                            [comp.to_dict() for comp in component_data]
                        )
                        row[col] = combined_freq

                # Recalculate the statistics
                book_freqs = [row[col] for col in row.keys() if col.startswith('freq_')]
                row['books_present_in'] = sum(1 for f in book_freqs if f > 0)
                row['max_freq_per_book'] = max(book_freqs) if book_freqs else 0

                final_rows.append(row)
        else:
            # Simple neologism - copy from original
            original_row = original_df[original_df['neologism'] == neologism]
            if not original_row.empty:
                final_rows.append(original_row.iloc[0].to_dict())

    final_df = pd.DataFrame(final_rows)
    return final_df.sort_values('total_frequency', ascending=False).reset_index(drop=True)


# New method for ManagedCompoundCombiner
def combine_compounds_with_info_preservation(self, neologisms: Dict[str, int],
                                             detailed_df: pd.DataFrame) -> Tuple[Dict[str, int], Dict[str, List[str]]]:
    """Combine compounds while tracking which components were merged"""
    combined = dict(neologisms)
    compound_mapping = {}  # compound_name -> [list of original components]
    created = []
    new_compounds = False

    for compound_name, components in self.compounds.items():
        found_components = {comp: combined.get(comp, 0) for comp in components
                            if comp in combined}

        if found_components:
            print(f"\nFound compound '{compound_name}': {list(found_components.keys())}")

            # Show detailed component information
            print("Component details:")
            for comp in found_components.keys():
                comp_row = detailed_df[detailed_df['neologism'] == comp]
                if not comp_row.empty:
                    first_book = comp_row.iloc[0]['first_book'].replace('Harry Potter And The ', '')
                    first_ch = comp_row.iloc[0]['first_chapter']
                    print(f"  • {comp}: {found_components[comp]} occurrences "
                          f"(1st: {first_book}, Ch.{first_ch})")

            choice = input("Combine? (y/n): ")

            if choice.lower() == 'y':
                # Use the main component's frequency
                compound_freq = max(found_components.values())

                # Remove individual components
                for comp in components:
                    if comp in combined:
                        del combined[comp]

                # Add the compound
                combined[compound_name] = compound_freq
                compound_mapping[compound_name] = components
                created.append(compound_name)
                print(f"Created: {compound_name} ({compound_freq} occurrences, preserved component info)")

    # Interactive creation with detailed info
    print(f"\nAvailable neologisms for new compounds:")
    sorted_neo = sorted(combined.items(), key=lambda x: x[1], reverse=True)
    for i, (word, count) in enumerate(sorted_neo[:20], 1):
        word_row = detailed_df[detailed_df['neologism'] == word]
        if not word_row.empty:
            first_book = word_row.iloc[0]['first_book'].replace('Harry Potter And The ', '')
            first_ch = word_row.iloc[0]['first_chapter']
            print(f"  {i:2d}. {word} ({count}, 1st: {first_book} Ch.{first_ch})")
        else:
            print(f"  {i:2d}. {word} ({count})")

    while True:
        user_input = input("\nCreate compound? (space-separated words or 'done'): ").strip()
        if user_input.lower() == 'done':
            break

        components = [w.strip().lower() for w in user_input.split() if w.strip()]
        if len(components) < 2:
            print("Need at least 2 components")
            continue

        found_components = {comp: combined.get(comp, 0) for comp in components
                            if comp in combined}

        if not found_components:
            print("No components found as neologisms")
            continue

        compound_name = ' '.join(components)
        max_freq = max(found_components.values())
        best_component = max(found_components.keys(), key=lambda x: found_components[x])

        print(f"Creating compound '{compound_name}' from:")
        for comp, count in found_components.items():
            comp_row = detailed_df[detailed_df['neologism'] == comp]
            marker = " (will use this info)" if comp == best_component else ""
            if not comp_row.empty:
                first_book = comp_row.iloc[0]['first_book'].replace('Harry Potter And The ', '')
                first_ch = comp_row.iloc[0]['first_chapter']
                print(f"  • {comp}: {count} occurrences (1st: {first_book} Ch.{first_ch}){marker}")
            else:
                print(f"  • {comp}: {count} occurrences{marker}")

        confirm = input(f"Confirm creation? (y/n): ")

        if confirm.lower() == 'y':
            # Remove the components
            for comp in components:
                if comp in combined:
                    del combined[comp]

            # Add the compound
            combined[compound_name] = max_freq
            compound_mapping[compound_name] = components
            self.compounds[compound_name] = components
            created.append(compound_name)
            new_compounds = True
            print(f"Created: '{compound_name}' (preserved info from {best_component})")

    if new_compounds:
        self._save_compounds()

    if created:
        print(f"Created {len(created)} compounds with preserved component information")

    return combined, compound_mapping




# Legacy function names for backwards compatibility
def run_complete_analysis(books, get_chapters_func, min_frequency=3, save_results=True):
    """Legacy function - calls timeline analysis"""
    return run_timeline_analysis(books, get_chapters_func, min_frequency, save_results)


def run_enhanced_analysis(books, get_chapters_func, min_frequency=3, save_results=True):
    """Legacy function - calls comprehensive analysis"""
    return run_comprehensive_analysis(books, get_chapters_func, min_frequency, save_results)