from FB2 import Author, ChapterWithSubchapters, FictionBook2, Image, SimpleChapter
import pathlib
import re
from pprint import pprint

#old abandoned format

def extract(txt):
##    txt = re.sub(r'[ ]{0,1}\n', '', txt)
    txt = re.sub(r'\n{2,9}', '\n', txt)
    txt = re.sub(r'\n[ ]{0,1}\n', '\n', txt)
##    txt = txt[:50]
    lines = txt.splitlines()
    chapter_title = lines.pop(0)
    chapter_text = lines
    #####
    if '] ' in chapter_title:
        chapter_title = chapter_title.split('] ')[1]
    if ': ' in chapter_title:
        chapter_title = chapter_title.split(': ')[1]
    #print(title)

    return chapter_title, chapter_text


def process_dir2():
    chapters = {}
    for item in sorted(pathlib.Path('./book2').iterdir()):
        if item.is_dir():
            index = item.stem.split('[')[0]
            chapter_name = item.stem.split('[')[1]
            chapter_name = chapter_name.split(']')[0]
            print(index, chapter_name)
            
            for subitem in sorted(item.iterdir()):
                if subitem.is_file() and subitem.suffix == '.txt':                        
                    with open(subitem, 'r', encoding='utf-8', errors='ignore') as fh:
                        txt = fh.read()
                        chapter_title, chapter_text = extract(txt)

                        chapter_index = index
##                        print('CI, CN ', chapter_index, chapter_name)
                       
                        try:
                            chapters[chapter_index].append((chapter_name, chapter_title, chapter_text))
                        except KeyError:
                            chapters[chapter_index] = []
                            chapters[chapter_index].append((chapter_name, chapter_title, chapter_text))
    return chapters

##pprint(process_dir2())


def process_dir():
    chapters = {}
    for item in sorted(pathlib.Path('./book').iterdir()):
##        print(item.name)
        with open(item, 'r', encoding='utf-8', errors='ignore') as fh:
            txt = fh.read()

            chapter_title, chapter_text = extract(txt)

            index = item.stem.split(']')[0]
            chapter_index, chapter_name = index.split('[')

##            print(chapter_name)
##            print(chapter_index)


            if '.' in chapter_index:
                sup_chap, sub_chap = chapter_index.split('.')
                try:
                    chapters[sup_chap].append((chapter_name, chapter_title, chapter_text))
                except KeyError:
                    chapters[sup_chap] = []
                    chapters[sup_chap].append((chapter_name, chapter_title, chapter_text))
            else:
                chapters[chapter_index] = []
                chapters[chapter_index].append((chapter_name, chapter_title, chapter_text))

    return chapters

##pprint(process_dir())


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
    book.titleInfo.genres = ["sf", "sf_fantasy"]

    chapters = process_dir2()
##    pprint(chapters)

    book.chapters = []

    for index in sorted(chapters.keys()):
        chapter = chapters[index]
##        print('CH: ', chapter)
        if len(chapter) == 1:
            ch_name, ch_title, ch_text = chapter[0]
            print(index, ch_name, ch_title)
            book.chapters.append(
                    SimpleChapter(
                        title=ch_title,
                        content=ch_text
                    ),
                )
        else:
##            print(chapter)
            sub = []
            for ch_name, ch_title, ch_text in chapter:
##                print(ch_name, ch_title, ch_text )
                print(index, ch_name, ch_title)
                sub.append(
                    SimpleChapter(
                        title=ch_title,
                        content=ch_text
                        ),
                    )

            book.chapters.append(
                ChapterWithSubchapters(
                    title=ch_name,
                    subchapters=sub
                ),
            )

    book.write("ExampleBook.fb2")


make_book()
