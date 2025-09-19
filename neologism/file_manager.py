import os
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class FileManager:
    """Manages file organization and paths for the neologism analysis project"""

    def __init__(self, base_dir: str = None):
        """Initialize file manager with organized directory structure"""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent

        # Define organized structure
        self.dirs = {
            'data': self.base_dir / 'data',
            'results': self.base_dir / 'results',
            'config': self.base_dir / 'config',
            'visualizations': self.base_dir / 'visualizations',
            'logs': self.base_dir / 'logs'
        }

        # Subdirectories
        self.dirs.update({
            'csv_files': self.dirs['results'] / 'csv',
            'json_files': self.dirs['config'] / 'user_decisions',
            'plots': self.dirs['visualizations'] / 'plots',
            'wordclouds': self.dirs['visualizations'] / 'wordclouds'
        })

        self._create_directories()

    def _create_directories(self):
        """Create all necessary directories"""
        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        # Create .gitkeep files in empty directories
        for dir_path in [self.dirs['logs']]:
            gitkeep = dir_path / '.gitkeep'
            if not gitkeep.exists():
                gitkeep.touch()

    def get_path(self, file_type: str, filename: str = None) -> Path:
        """Get organized path for different file types"""
        paths = {
            # CSV outputs
            'neologisms_csv': self.dirs['csv_files'] / 'harry_potter_neologisms.csv',
            'comprehensive_csv': self.dirs['csv_files'] / 'harry_potter_neologisms_comprehensive.csv',
            'books_summary_csv': self.dirs['csv_files'] / 'harry_potter_books_summary.csv',

            # JSON config files
            'blacklist_json': self.dirs['json_files'] / 'neologism_blacklist.json',
            'merge_decisions_json': self.dirs['json_files'] / 'neologism_merge_decisions.json',
            'compound_rules_json': self.dirs['json_files'] / 'compound_neologisms.json',

            # Visualization files
            'timeline_plot': self.dirs['plots'] / 'neologisms_by_book.png',
            'first_chapters_plot': self.dirs['plots'] / 'first_chapters_neologisms.png',
            'frequency_plot': self.dirs['plots'] / 'first_chapters_frequency.png',
            'creative_chapters_plot': self.dirs['plots'] / 'most_creative_chapters.png',
            'wordclouds_combined': self.dirs['wordclouds'] / 'neologisms_wordclouds_by_book.png',

            # Log files
            'analysis_log': self.dirs['logs'] / f'analysis_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        }

        if file_type in paths:
            return paths[file_type]
        elif filename:
            # Dynamic path based on file type and custom filename
            if file_type == 'csv':
                return self.dirs['csv_files'] / filename
            elif file_type == 'json':
                return self.dirs['json_files'] / filename
            elif file_type == 'plot':
                return self.dirs['plots'] / filename
            elif file_type == 'wordcloud':
                return self.dirs['wordclouds'] / filename

        raise ValueError(f"Unknown file type: {file_type}")

    def save_json(self, data: Dict[str, Any], file_type: str, filename: str = None) -> Path:
        """Save JSON data with proper organization"""
        path = self.get_path(file_type, filename)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return path

    def load_json(self, file_type: str, filename: str = None, default: Any = None) -> Any:
        """Load JSON data with fallback"""
        try:
            path = self.get_path(file_type, filename)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading JSON from {file_type}: {e}")

        return default or {}

    def get_all_csv_files(self) -> Dict[str, Path]:
        """Get all CSV files with descriptive names"""
        return {
            'Basic Neologisms': self.get_path('neologisms_csv'),
            'Comprehensive Analysis': self.get_path('comprehensive_csv'),
            'Books Summary': self.get_path('books_summary_csv')
        }

    def get_all_json_files(self) -> Dict[str, Path]:
        """Get all JSON config files"""
        return {
            'Blacklist': self.get_path('blacklist_json'),
            'Merge Decisions': self.get_path('merge_decisions_json'),
            'Compound Rules': self.get_path('compound_rules_json')
        }

    def cleanup_old_files(self, keep_days: int = 7):
        """Clean up old log files"""
        cutoff = datetime.now().timestamp() - (keep_days * 24 * 60 * 60)

        for log_file in self.dirs['logs'].glob('analysis_*.log'):
            if log_file.stat().st_mtime < cutoff:
                log_file.unlink()
                print(f"Removed old log: {log_file.name}")

    def create_readme(self):
        """Create README files explaining directory structure"""
        readme_content = {
            'results': """# Results Directory

Contains all analysis output files:

## CSV Files (/csv/)
- `harry_potter_neologisms.csv`: Basic timeline analysis
- `harry_potter_neologisms_comprehensive.csv`: Detailed by-book analysis  
- `harry_potter_books_summary.csv`: Summary statistics per book

## Structure
Each CSV contains:
- Neologism frequencies
- First appearance information
- Book-by-book breakdowns (comprehensive only)
""",

            'config': """# Configuration Directory

Contains user decisions and settings:

## User Decisions (/user_decisions/)
- `neologism_blacklist.json`: Words marked as non-neologisms
- `neologism_merge_decisions.json`: Similar words merge choices
- `compound_neologisms.json`: Compound word combination rules

These files preserve your manual review decisions across analysis runs.
""",

            'visualizations': """# Visualizations Directory

Contains all generated plots and visual outputs:

## Plots (/plots/)
- Timeline and frequency charts
- Comparative analysis graphs
- Creative chapter visualizations

## Word Clouds (/wordclouds/)
- Individual and combined word clouds by book
- Thematic visualizations
""",

            'logs': """# Logs Directory

Contains analysis execution logs for debugging and tracking.

Logs are automatically cleaned up after 7 days.
"""
        }

        for dir_name, content in readme_content.items():
            readme_path = self.dirs[dir_name] / 'README.md'
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def print_structure(self):
        """Print the organized directory structure"""
        print("📁 Project Structure:")
        print(f"{self.base_dir.name}/")

        structure = [
            ("├── config/", "User settings and decisions"),
            ("│   └── user_decisions/", "JSON files with manual choices"),
            ("├── results/", "Analysis outputs"),
            ("│   └── csv/", "CSV data files"),
            ("├── visualizations/", "Charts and plots"),
            ("│   ├── plots/", "Statistical charts"),
            ("│   └── wordclouds/", "Word cloud images"),
            ("└── logs/", "Analysis execution logs")
        ]

        for folder, description in structure:
            print(f"    {folder:<25} # {description}")

    def migrate_old_files(self):
        """Migrate existing files to new structure"""
        migrations = [
            # CSV files
            ('harry_potter_neologisms.csv', 'neologisms_csv'),
            ('harry_potter_neologisms_comprehensive.csv', 'comprehensive_csv'),
            ('harry_potter_books_summary.csv', 'books_summary_csv'),

            # JSON files
            ('neologism_blacklist.json', 'blacklist_json'),
            ('neologism_merge_decisions.json', 'merge_decisions_json'),
            ('compound_neologisms.json', 'compound_rules_json'),

            # Image files
            ('neologisms_by_book.png', 'timeline_plot'),
            ('first_chapters_neologisms.png', 'first_chapters_plot'),
            ('first_chapters_frequency.png', 'frequency_plot'),
            ('neologisms_wordclouds_by_book.png', 'wordclouds_combined')
        ]

        migrated = []
        for old_filename, file_type in migrations:
            old_path = self.base_dir / old_filename
            if old_path.exists():
                new_path = self.get_path(file_type)
                old_path.rename(new_path)
                migrated.append(f"{old_filename} → {new_path.relative_to(self.base_dir)}")

        if migrated:
            print("📦 Migrated files to organized structure:")
            for migration in migrated:
                print(f"    {migration}")

        return len(migrated)


# Update the classes to use FileManager
class ManagedSimilarityMatcher:
    """SimilarityMatcher with organized file management"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.saved_decisions = file_manager.load_json('merge_decisions_json', default={})

    def _save_decisions(self):
        self.file_manager.save_json(self.saved_decisions, 'merge_decisions_json')


class ManagedBlacklistFilter:
    """BlacklistFilter with organized file management"""

    def __init__(self, file_manager: FileManager):
        self.file_manager = file_manager
        self.blacklist = set(file_manager.load_json('blacklist_json', default=[]))

    def _save_blacklist(self):
        self.file_manager.save_json(sorted(list(self.blacklist)), 'blacklist_json')


class ManagedCompoundCombiner:
    """CompoundCombiner with organized file management"""

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

        # CORRECTION : Sauvegarder même les defaults
        if updated:
            self._save_compounds()
            print(
                f"Initialized {len([k for k in defaults.keys() if k not in self.file_manager.load_json('compound_rules_json', default={})])} default compounds")

    def _save_compounds(self):
        self.file_manager.save_json(self.compounds, 'compound_rules_json')