from retrieval_and_cleaning import get_books, get_chapters

def book_sanity_check(book):

    word_dict = dict()

    for word in book:
        pass

def main():
    hp_books, books_names = get_books()
    # print(hp_books[books_names[0]])
    first_book_chapters = get_chapters(hp_books[books_names[0]])
    print("here")


    book_sanity_check(hp_books[books_names[0]])

if __name__ == "__main__":
    main()