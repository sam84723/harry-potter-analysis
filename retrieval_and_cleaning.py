from typing import Tuple, Dict, List

import kagglehub
import os
import re

def get_books() -> Tuple[Dict, List]:
    """
    A function that gets the Harry Potter books from Kaggle
    :return:
    books : A dictionary of Harry Potter books
    names : A list with the book names
    """
    # Download latest version
    path = kagglehub.dataset_download("shubhammaindola/harry-potter-books")
    print("Path to dataset files:", path)
    books = {}
    names = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                text = f.read()
                print(f"\n=== {file} ===")
                # print(text[:500])  # print the first 500 characters of each book
                names.append(file)
                books[file] = text

    return books, names

def fix_first_word_spacing(text):
    # Target the first 5-10 words, where the issue usually lives
    lines = text.splitlines()
    fixed_lines = []
    for i, line in enumerate(lines):
        if line.strip():  # First non-empty line
            # Fix: Replace a capital letter followed by a space and a lowercase word (T he → The)
            fixed = re.sub(r'\b([A-Z])\s+([a-z]+)\b', r'\1\2', line)
            fixed_lines.append(fixed)
            fixed_lines.extend(lines[i+1:])
            break
        else:
            fixed_lines.append(line)
    return "\n".join(fixed_lines)



def get_chapters(book_text):
    """
    A function that gets the chapters from Harry Potter books
    :param book_text:
    :return:
    """
    # Split using CHAPTER in all caps at the start of a line
    matches = re.split(r'\n+(CHAPTER [A-Z ]+)\n+', book_text)

    chapter_data = []

    # The first chapter is a little bit different since it doesnt have a title
    if matches[0].strip():
        chapter_data.append(("CHAPTER ONE", matches[0].strip()))

    for i in range(1, len(matches), 2):
        chapter_title = matches[i].strip()  # CHAPTER ONE
        content = matches[i + 1].strip() if i + 1 < len(matches) else ""

        # Try to extract the line after the chapter (e.g., "THE JOURNEY FROM...")
        first_line = content.split('\n', 1)
        if len(first_line) == 2:
            subtitle, rest = first_line
            # chapter_content = f"{chapter_title}\n{subtitle}\n\n{rest}"
            chapter_content = rest[3:]
        else:
            # chapter_content = f"{chapter_title}\n\n{content}"
            chapter_content = content[3:]

        chapter_content = fix_first_word_spacing(chapter_content)

        chapter_data.append((chapter_title, chapter_content))


    # ✅ Print preview
    # for idx, (title, content) in enumerate(chapter_data[:2], 1):
    #     print(f"\n=== Chapter {idx + 1}: {title} ===\n")
    #     print(content[:500])  # Just a preview

    return chapter_data