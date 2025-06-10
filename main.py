from retrieval_and_cleaning import (get_books_dataset, get_chapters,
                                    get_characters_datasets, get_dialogues_dataset)
from sanity_checks import run_all_sanity_checks

def main():
    hp_books, books_names = get_books_dataset()
    # print(hp_books[books_names[0]])
    first_book_chapters = get_chapters(hp_books[books_names[0]])
    print("Books Loaded")

    dialogue_path = get_dialogues_dataset()
    print("Dialogue Dataset Loaded")

    characters_path = get_characters_datasets()
    print("Characters Dataset Loaded")

    run_all_sanity_checks()

if __name__ == "__main__":
    main()