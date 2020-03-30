#!C:\Users\Dan\AppData\Local\Programs\Python\Python37-32\python.exe
# Spoonerism Bot
# define spoonerism:
# a verbal error in which a speaker accidentally
# transposes the initial sounds or letters of two or
# more words, often to humorous effect, as in the sentence
# 'you have hissed the mystery lectures',
# accidentally spoken instead of the intended sentence
# 'you have missed the history lectures'.

# TODO
# clean up input gathering
#	.\spoonerism.py file.txt

import sys
import pprint
# pprint.pprint(locals())
import numpy

# 'y' is a vowel if its the first vowel in a word
vowelPermissive = 'aeiouyAEIOUY'
# 'y' is not a vowel if it is following a full-time vowel
vowelStrict = 'aeiouAEIOU'
# words not to spoonerize
articles = ['a', 'an', 'the', 'is', 'if', 'in', 'with', 'and', 'or', 'but', 'at', 'you']


def swap(tupWords, syls):
    positions = splitPositions(tupWords)
    size = len(positions)
    swapOrder = derange(positions)
    tupSyls = []
    for i in range(len(swapOrder)):
        tupSyl = (swapOrder[i], syls[i])
        tupSyls.append(tupSyl)
    tupSpoon = []
    for tupWord in tupWords:
        for tupSyl in tupSyls:
            if tupWord[0] == tupSyl[0]:
                word = tupWord[1]
                sylA = startSyllable(word)
                sylB = tupSyl[1]
                finalSyl = spoonLogic(sylA, sylB)
                spoonWord = sylSwap(word, sylA, finalSyl)
                tup = (tupWord[0], spoonWord)
                tupSpoon.append(tup)
    return tupSpoon


# Swap rules:
#   Swap consonants upto but not including the first vowels of the words
#   If leading consonants match exactly, swap the first vowels too
def spoonLogic(sylA, sylB):
    tupA = syl2tup(sylA)
    tupB = syl2tup(sylB)
    newSyl = ''
    if tupA[0].lower() == tupB[0].lower():
        newSyl = sylB
    else:
        newSyl = tupB[0] + tupA[1].lower()
    return newSyl


def sylSwap(word, oldSyl, newSyl):
    newSyl = matchCase(oldSyl, newSyl)
    newWord = word.replace(oldSyl, newSyl, 1)
    return newWord


def gatherWords(input):
    tupWords = []
    for i in range(len(input)):
        word = input[i]
        if word.lower() not in articles:
            tupWord = (i, word)
            tupWords.append(tupWord)
    return tupWords


def gatherSyls(words):
    syls = []
    for word in words:
        syls.append(startSyllable(word))
    return syls


def startSyllable(word):
    # word = word.lower()
    syl = ''
    last = ''
    for i in word:
        curr = i
        syl += last
        if curr not in vowelStrict and last in vowelPermissive and last != '':
            break
        last = curr
    return syl


# matches the case of sylB to sylA
def matchCase(sylA, sylB):
    charA = sylA[0]
    charB = sylB[0]
    if charA.isupper():
        charB = charB.upper()
    else:
        charB = charB.lower()
    newSyl = charB + sylB[1:]
    return newSyl


def splitPositions(tupWords):
    positions = []
    for tup in tupWords:
        positions.append(tup[0])
    return positions


def splitWords(tupWords):
    words = []
    for tup in tupWords:
        words.append(tup[1])
    return words


def derange(positions):
    newOrder = numpy.random.permutation(positions)
    breakCond = False
    while not breakCond:
        for i in range(len(newOrder)):
            if positions[i] == newOrder[i]:
                newOrder = numpy.random.permutation(positions)
                breakCond = False
            else:
                breakCond = True
    return newOrder


def combineSpoon(input, tupSpoon):
    output = copyArr(input)
    for tup in tupSpoon:
        pos = tup[0]
        output[pos] = tup[1]
    return output


def copyArr(input):
    output = []
    for i in input:
        output.append(i)
    return output


def arr2str(arr):
    sentence = ''
    for i in arr:
        sentence += i + ' '
    return sentence.strip()


def syl2tup(syl):
    tup = ''
    consts = ''
    vowels = ''
    for i in syl:
        if i not in vowelPermissive:
            consts += i
        else:
            vowels += i
    tup = (consts, vowels)
    return tup


def main():
    input = sys.argv[1:]
    tupWords = gatherWords(input)
    words = splitWords(tupWords)
    syls = gatherSyls(words)
    tupSpoon = swap(tupWords, syls)
    output = combineSpoon(input, tupSpoon)

    print(arr2str(input))
    print(arr2str(output))
    return 0


if __name__ == "__main__":
    main()
