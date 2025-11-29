from FB2 import Author, ChapterWithSubchapters, FictionBook2, SimpleChapter
import pathlib
import re
from xml.dom import minidom

from pprint import pprint

CHAPTERS_PATH = './book-fb2'
TEXT_ENCODING = 'utf-8'
BOOK_FILE = "ExampleBook.fb2"


## extract chapter text
## first line is the chapter's title
def extract(filename):
    with open(filename, 'r', encoding=TEXT_ENCODING, errors='replace') as fh:
        txt = fh.read()
        ##txt = re.sub(r'[ ]{0,1}\n', '', txt)
        ## eradicate two or more newlines
        txt = re.sub(r'\n{2,9}', '\n', txt)
        ## eradicate newlines with space between
        txt = re.sub(r'\n[ ]{0,1}\n', '\n', txt)
        ## test mode, print 50 characters of text only
        ## txt = txt[:50]
        lines = txt.splitlines()
        chapter_title = lines.pop(0)
        chapter_text = lines

        ##### prettify some titles, for example
        ## [Toradora] Taiga in trouble > Taiga in trouble
        ## Strike the blood: Yukina > Yukina
        if '] ' in chapter_title:
            chapter_title = chapter_title.split('] ')[1]
        if ': ' in chapter_title:
            chapter_title = chapter_title.split(': ')[1]

    return chapter_title, chapter_text


def extract_index(filename):
    result = re.search('^([0-9]{1,})(.*?)', filename)
    index = result.group(1)
    return index


def extract_superchapter_name(filename):
    result = re.search('^([0-9]{1,})\\[(.*?)\\]', filename)
    index, name = result.group(1), result.group(2)
    return index, name


def process_dir(path):
    chapters = []
    for item in sorted(path.iterdir()):
        index = extract_index(item.stem)
        if item.is_file() and item.suffix == '.txt':
            chapter_title, chapter_text = extract(item)
            print(index, item.name)
            print(chapter_text[0:2])
            chapters.append(
                SimpleChapter(
                    title=chapter_title,
                    content=chapter_text
                )
            )
            # chapters.append((chapter_title, chapter_text))
        if item.is_dir():
            index, chapter_name = extract_superchapter_name(item.stem)
            chapters.append(
                ChapterWithSubchapters(
                    title=chapter_name,
                    subchapters=process_dir(item)
                )
            )
            # chapters.append((chapter_name, process_dir(item)))
    return chapters


def make_book():
    book = FictionBook2()
    book.titleInfo.title = "Example book"
    book.titleInfo.annotation = "Small test book. Shows basics of FB2 library"
    book.titleInfo.authors = [
        Author(
            firstName="Alex",
            middleName="Unknown",
            nickname="Ae_Mc",
            emails=["ae_mc@mail.ru"],
            homePages=["ae-mc.ru"],
        )
    ]
    book.titleInfo.genres = ["sf", "sf_fantasy", ]

    book.chapters = process_dir(pathlib.Path(CHAPTERS_PATH))
    book.write(BOOK_FILE)

    ## prettify fb2 xml because some readers (Alreader) can't properly process
    ## file and show plain text with <p> tags and without table of contents
    doc = minidom.parse(BOOK_FILE)
    with open(BOOK_FILE, 'w', encoding=TEXT_ENCODING) as fh:
        fh.write(doc.toprettyxml(indent='    ',encoding=TEXT_ENCODING).decode())

if __name__ == '__main__':
    make_book()
    input("Press Enter to continue...")
