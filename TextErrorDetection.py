#!/usr/bin/env python
# coding: utf-8

# # Spelling correction 
# 
# Niraj Dev Pandey (271484)

# first of all, we need some words. First we need some text, possibly from a file. Then we can break the text into words or tokens. I have a big text called train3.txt which I have saved in my local directry. This text file is from NLTK website. We can read it, and see how many characters are there in the file

# In[4]:


# importing preliminaries
get_ipython().run_line_magic('pylab', 'inline')
import re
import math
import string
from collections import Counter
#from __future__ import division


# In[28]:


TEXT = open('big.txt').read()
len(TEXT)


# So, it's 28,42164 characters.
# 
# Now let's break the text up into tokens. For now we'll ignore all the punctuation and numbers, and anything that is not a letter.

# In[29]:


def tokens(text):
    "List all the word tokens (consecutive letters) in a text. Normalize to lowercase."
    return re.findall('[a-z]+', text.lower()) 


# In[30]:


tokens('Hey, I am working with NLTK..!')


# In[31]:


WORDS = tokens(TEXT)
len(WORDS)


# So, a million words. Here are the top 10 words:

# In[32]:


print(WORDS[:10])


# Here we are using a model that is known as "Bag of words" We know that language is very complicated, but we can create a simplified model of language that captures part of the complexity. In this model, we avoid the order of words, but carry their frequencies. Here's a function to sample an n word sentence from a bag of words:

# In[33]:


def sample(bag, n=10):
    "Sample a random n-word sentence from the model described by the bag of words."
    return ' '.join(random.choice(bag) for _ in range(n))


# In[76]:


sample(WORDS)


# In[35]:


Counter(tokens('Hey, this is the third exercise'))


# Another way to use this model is "Counter", which is a dictionary of {'word': count} pairs. see the below code: 

# In[36]:


COUNTS = Counter(WORDS)

print (COUNTS.most_common(10))


# A Counter is like a dict, but with a few extra methods. one can see the differences below -

# In[37]:


for w in tokens('pound is widely expected to take another sharp drive '):
    print (COUNTS[w], w)


# linguist 'George Zipf' Doctorate from Harvard, noted that in any big text file, the nth most frequent word appears with a frequency of about 1/n. He is the enventor of Zipf's Law. If we plot the frequency of words, most common first, on a log-log plot, they should come out as a straight line if Zipf's Law holds. Here we see that it is a fairly close fit: 

# In[38]:


M = COUNTS['is']
yscale('log'); xscale('log'); title('Frequency of n-th most frequent word and 1/n line.')
plot([c for (w, c) in COUNTS.most_common()])
plot([M/i for i in range(1, len(COUNTS)+1)]);


# Given a word w, find the most likely correction c = correct(w).
# 
# Approach: Try all candidate words c that are known words that are near w. Choose the most likely one.
# 
# How to balance near and likely?
# 
# For this time we always prefer nearer, but when there is a tie on nearness, then the program use the word with the highest WORDS count. to Measure nearness we are going to use edit distance.I have determined that going out to edit distance 2 will give us reasonable results. Then we can define correct(w)

# In[39]:


def correct(word):
    "Find the best spelling correction for this word."
    # Prefer edit distance 0, then 1, then 2; otherwise default to word itself.
    candidates = (known(edits0(word)) or 
                  known(edits1(word)) or 
                  known(edits2(word)) or 
                  [word])
    return max(candidates, key=COUNTS.get)


# The functions known and edits0 are easy; and edits2 is easy if we assume we have edits1

# In[40]:


def known(words):
    "Return the subset of words that are actually in the dictionary."
    return {w for w in words if w in COUNTS}

def edits0(word): 
    "Return all strings that are zero edits away from word (i.e., just word itself)."
    return {word}

def edits2(word):
    "Return all strings that are two edits away from this word."
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}


# Now for edits1(word): the set of candidate words that are one edit away. For example, given "speech", this would include "sepech"and also "spechz". One can see this in the code below in(print (edits1('speech')) Then How could we detect them? One way is to split the original word in all possible places, each split forming a pair of words, (a, b), before and after the place, and at each place, either delete, transpose, replace, or insert a letter.

# In[41]:


def edits1(word):
    "Return all strings that are one edit away from this word."
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def splits(word):
    "Return a list of all possible (first, rest) pairs that comprise word."
    return [(word[:i], word[i:]) 
            for i in range(len(word)+1)]

alphabet = 'abcdefghijklmnopqrstuvwxyz'


# In[42]:


splits('speech')


# In[54]:


print (edits0('speech'))


# In[55]:


print (edits1('speech'))


# In[61]:


print (len(edits2('speech')))


# In[62]:


map(correct, tokens('speech eis not good'))


# In[63]:


def correct_text(text):
    "Correct all the words within a text, returning the corrected text."
    return re.sub('[a-zA-Z]+', correct_match, text)

def correct_match(match):
    "Spell-correct word in match, and preserve proper upper/lower/title case."
    word = match.group()
    return case_of(word)(correct(word.lower()))

def case_of(text):
    "Return the case-function appropriate for text: upper, lower, title, or just str."
    return (str.upper if text.isupper() else
            str.lower if text.islower() else
            str.title if text.istitle() else
            str)


# In[64]:


map(case_of, ['UPPER', 'lower', 'Title', 'CamelCase'])


# In[85]:


correct_text('spech is noot goad')


# In[84]:


correct_text('havee yoo dane thaat projecct')


# In[87]:


correct_text('Profesor is a nyce persan')


# Here we saw that how we can correct the miss spelled words from our text. This is not the one and only or best methodes to do so. but it's the easiest and prity fast way to do so.

# I would like to thanks one website from where I took some tutorial to finish this exercise 

# http://norvig.com/spell-correct.html
