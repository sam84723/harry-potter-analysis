import shutil
from typing import Tuple, Dict, List
import kagglehub
import os
import re
from kagglehub import KaggleDatasetAdapter

path = ""


def get_dialogues_dataset():

    download_path = download_kaggle_dataset("shreyasur965/harry-potter-characters-with-dialogues")
    print("Path to dataset files:", download_path)
    return download_path


def get_characters_datasets():
    """
    Load the dataset that includes Characters.csv, Potions.csv, Spells.csv and more.
    """

    download_path = download_kaggle_dataset("gulsahdemiryurek/harry-potter-dataset")
    print("Path to dataset files:", download_path)
    return download_path


def get_books_dataset() -> Tuple[Dict, List]:
    """
    A function that gets the Harry Potter books from Kaggle
    :return:
    books : A dictionary of Harry Potter books
    names : A list with the book names
    """
    # Download latest version

    #TODO Fix the problem of chapters cleaning in books

    download_path = download_kaggle_dataset("shubhammaindola/harry-potter-books")
    print("Path to dataset files:", download_path)
    books = {}
    names = []
    for file in os.listdir(download_path):
        if file.endswith(".txt"):
            with open(os.path.join(download_path, file), "r", encoding="utf-8") as f:
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
        # chapter_data.append(("CHAPTER ONE", matches[0].strip()))
        chapter_content = fix_first_word_spacing(matches[0].strip())
        chapter_data.append(chapter_content)

    for i in range(1, len(matches), 2):
        subtitle = None
        chapter_title = matches[i].strip()  # CHAPTER ONE
        content = matches[i + 1].strip() if i + 1 < len(matches) else ""
        # Try to extract the line after the chapter (e.g., "THE JOURNEY FROM...")
        first_line = content.split('\n', 1)
        if len(first_line) == 2:
            subtitle, rest = first_line
            # print(chapter_title, subtitle)
            # chapter_content = f"{chapter_title}\n{subtitle}\n\n{rest}"
            chapter_content = rest[3:]
        else:
            # chapter_content = f"{chapter_title}\n\n{content}"
            chapter_content = content[3:]

        chapter_content = fix_first_word_spacing(chapter_content)

        chapter_data.append((chapter_title, subtitle, chapter_content))


    # ✅ Print preview
    # for idx, (title, content) in enumerate(chapter_data[:2], 1):
    #     print(f"\n=== Chapter {idx + 1}: {title} ===\n")
    #     print(content[:500])  # Just a preview

    return chapter_data


def download_kaggle_dataset(handle_name):

    """

    :param handle_name:
    :return:
    """

    # Checks if the folder Kaggle datasets exist and else creates it
    folder_name = "Kaggle_datasets"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Creating a folder for Kaggle datasets : {folder_name}")


    dataset_name = handle_name.split("/")[-1]
    destination_path = os.getcwd() + '\\' + folder_name + '\\' + dataset_name

    if not os.path.exists(destination_path):
        source_path = kagglehub.dataset_download(handle_name)

        # print("Source path:", source_path)
        # print("Destination path:", destination_path)

        # 1. Create the folder name if needed
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)

        # 2. Copy all the folder with all whats inside
        shutil.copytree(source_path, destination_path)

        # 3. Delete the source folder
        shutil.rmtree(source_path)

        print(f"Folder transferred from {source_path} to {destination_path}")

    return destination_path


if __name__ == "__main__":

    get_books_dataset()
    get_dialogues_dataset()
    get_characters_datasets()