
import re
import itertools

# this regular expression describes what a "word" is.
WORD_PATTERN = r'\w(\w|-\w)*'
word_re = re.compile(WORD_PATTERN)
CONTEXT_LENGTH = 11

class Concordance(object):
    def __init__(self):
        self.words = {}
        self.text = ''

    def span_prefix(self, span):
        context_start, w_start, w_end, context_end = span
        return self.text[context_start:w_start]

    def span_suffix(self, span):
        context_start, w_start, w_end, context_end = span
        return self.text[w_end:context_end]

    def FromText(self, text):
        self.text = text
        # tokenize the input into words, and then add an infinite stream of
        # None to the end of the list. This keeps the algorithm working for
        # words near the end of the list.
        it = word_re.finditer(text)
        it = itertools.chain(it, itertools.cycle([None]))
        # context is our sliding window, where the middle word is the one we
        # will tablulate. Initialize context to a bunch of empty words.
        context = []
        middle = CONTEXT_LENGTH // 2
        for i in range(CONTEXT_LENGTH):
            context.append( ('', 0, 0) )
        for m in it:
            # add the next word to the context, and remove the first word.
            # remember the Nones are the end of the iterator.
            context.pop(0)
            if m == None:
                context.append( ('', len(text), len(text)) )
            else:
                context.append( (m.group(), m.start(), m.end()) )
            # tabulate this word unless it is one of our empty words
            word, w_start, w_end = context[middle]
            # is this word one of our initial blanks?
            if word == '' and w_start == 0:
                continue
            # are we at the end?
            if word == '' and w_start == len(text):
                break
            _, context_start, _ = context[0]
            _, _, context_end = context[-1]
            lst = self.words.get(word, None)
            if lst is None:
                lst = []
                self.words[word] = lst
            lst.append( (context_start, w_start, w_end, context_end) )


