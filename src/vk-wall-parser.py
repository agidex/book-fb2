import re

HTML_DIR = ''
PIC_DIR = ''

def parse_file(filename):
    with open(filename, 'r', encoding='cp1251', errors='ignore') as fh:
        txt = fh.read()
        

print('hello')