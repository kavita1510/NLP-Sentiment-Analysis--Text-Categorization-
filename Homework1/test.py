from collections import Counter
import glob
import os
import re
import string
#import nltk
#import numpy

cnt=Counter()
ngram_counter = Counter()
global ngram_list
ngram_list = []

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
            ngram_ct = ngrams(fileobj, 2);
    #print ngram_ct
    print ct

def ngrams(fileobj,n):
    with open(fileobj, 'r') as f:
        txt = f.read()
        splitted_txt = ''
        splitted_txt = txt.split()
        
        for i in range(len(splitted_txt)-n+1):
            ngram_str = ' '.join(splitted_txt[i:i+n])
            #print ngram_str
            ngram_list.append(ngram_str)
        
        #for word in ngram_list:
            #if word in ngram_list:
                #ngram_counter[word] += 1
    
        
    #return ngram_counter
    print ngram_list


# def print_summary(filepath, ct):
#     words=sorted(ct.keys())
#     counts=[str(ct[k]) for k in words]
#     print('{0}\n{1}\n{2}\n\n'.format(
#         filepath,
#         ', '.join(words),
#         ', '.join(counts)))

count_words_in_dir('txt_sentoken/pos')
