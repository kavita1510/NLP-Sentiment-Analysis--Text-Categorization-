from collections import Counter
import glob
import os
import re
import string
#import nltk
#import numpy

cnt=Counter()


specials = '-"/.,' #etc



def word_frequency(fileobj):
#     for line in open(fileobj,'r'):
#         trans = string.maketrans(specials, ' '*len(specials))
#         cleanline = line.translate(trans)
    with open(fileobj, 'r') as f:
        txt = f.read()
        words=set(txt.split())
        for word in words:
            if word in words:
                cnt[word] += 1
    return cnt

def count_words_in_dir(dirPath):
    """To count the words from all the text files in a directory"""
    for fileobj in glob.iglob(os.path.join(dirPath, '*.txt')):
            ct = word_frequency(fileobj)
    print ct

# def print_summary(filepath, ct):
#     words=sorted(ct.keys())
#     counts=[str(ct[k]) for k in words]
#     print('{0}\n{1}\n{2}\n\n'.format(
#         filepath,
#         ', '.join(words),
#         ', '.join(counts)))

count_words_in_dir('txt_sentoken/pos')
