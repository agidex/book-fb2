# book-fb2
FB2 book generator from txt files

## howto use
1. Place `.txt` files with chapters in `book-txt` folder
2. Order filenames for you desired contents structure
3. Run `BOOK_FB2.py`
4. `ExampleBook.fb2` is your result
5. Profit!

## naming conventions
First line of file is a chapter title (shown in fb2 table of contents)

Other lines added as main text

Multiple newlines eradicated

## example file structure

**bold** part of filename are nesessary

- cwd (folder with `BOOK_FB2.py` file executable)
  - book-txt
    - **00**Prologue.txt
    - **01[Part 1]**
      - **01**Chapter 1.txt
      - **02**_Chapter 2.txt
      - **03** Chapter 3.txt
    - **02[Part 2]**
      - **01**Chapter 1.txt
      - **02**_Chapter 2.txt
    - **03**   Epilogue.txt

Note there are no need of separators between `index` and `chapter name`, you can add them for readability purpose

First numbers are index (for sorting purpose)

Superchapter (chapter with chapters inside) shoud be a folder with chapter index (leading digits) and chapter name in [square brackets]

Superchapters can be nested and mixed with ordinal chapters:

  - book-txt
    - **00**Prologue.txt
    - **01[Part 1]**
      - **01**Chapter 1.txt
      - **02**_Chapter 2.txt
      - **03[Part 1.5]**
        - **01**Some Chapter 1.txt
        - **02**Some Chapter 2.txt
        - **03**Some Chapter 3.txt
      - **04** Chapter 3.txt
    - **02[Part 2]**
      - **01**Chapter 1.txt
      - **02**_Chapter 2.txt
    - **03** Epilogue.txt