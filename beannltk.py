import nltk
from nltk import FreqDist
from nltk.corpus import gutenberg
import json
import csv


print "* Loading corpus"
#raw = gutenberg.raw('melville-moby_dick.txt')
#raw = gutenberg.raw('bible-kjv.txt')
raw = gutenberg.raw('blake-poems.txt')
print "* Tokenizing"
tokens = nltk.word_tokenize(raw)

print "* Tagging parts of speech"
# Save this to strip articles later
parts_of_speech = nltk.pos_tag(tokens)

print "* Converting POS list into a dict for lookup"
# TODO -- fix this.  this is going to fuck up on homonyms
parts_of_speech = dict(parts_of_speech)

# You can ban other parts of speech by adding their tags to this list.
# You can find out what the part-of-speech tags mean by using code like
# this:
# >>> print nltk.help.upenn_tagset('DT')
# DT: determiner
#     all an another any both del each either every half la many much nary
#     neither no some such that the them these this those
banned_parts_of_speech = [
    'DT',
    'IN',
    'CC',
    'TO',
    'PRP',
    'PRP$',
]

banned_words = [
    'is',
    'has',
    'had',
    'have',
    'there',
    'so',
    'So',
    'on',
    'On',
    'did',
    'am',
    'are'
    'Is',
    'be',
    'my',
    'My',
    'can',
    'Can',
    'was',
    'of',
    'Of',
    'OF',
    'OH',
    'oh',
    'Oh',
    'the',
    'THE',
    'The',
    'that',
    'That',
    'when',
    'When',
    'what',
    'What',
    'who',
    'Who',
    'how',
    'How',
    'his',
    'His',
    'were',
    'Why',
    'why',
    'then',
    'Then',
    'Does',
    'does',
    'O',
    'do',
    'Do',
    'Go',
    'go',
]
print "* Stripping stuff we don't want"
# Strip punctuation and banned parts of speech
tokens = [
    token for token in tokens if (
        # Kill punctuation
        token.isalpha() and
        # Kill parts of speech that we don't want.
        not parts_of_speech[token] in banned_parts_of_speech and
        not token in banned_words #and
        #len(token) > 4
    )
]

print "* Building frequency distribution"
words = FreqDist(tokens)

N = 20
def showWords(N=100):
    print "* Printing top %i words" % N
    f = open('blake.csv', 'wb')
    writer = csv.writer(f)
    for i, pair in enumerate(words.items()):
        word, count = pair
        row = word, count, parts_of_speech[word]
        #row = "%r, %r, %r" % (word, count, parts_of_speech[word])
        #row = json.dumps([word, count, parts_of_speech[word]], separators=(',',':'))
        writer.writerow(row)
        print "%r appeared %i times.  Its part of speech is %r" % (
            word, count, parts_of_speech[word],
        )
        if i > N:
            break
    f.close()
    return (word, count, parts_of_speech)

showWords()
