from retrieval_and_cleaning import get_books, get_chapters


def main():
    hp_books, books_names = get_books()
    # print(hp_books[books_names[0]])
    first_book_chapters = get_chapters(hp_books[books_names[1]])
    print("here")


if __name__ == "__main__":
    main()