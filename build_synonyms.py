import sys
import spacy
from pprint import pprint
from spacy.tokens.token import Token
from nltk.corpus import wordnet as wn
from six.moves import xrange
import random

nlp = spacy.load('en')

def build_sentence(original_doc, new_tokens):
    new_sentence = ' '.join(new_tokens).replace('_', ' ')
    new_doc = nlp(new_sentence)
    similarity_score = original_doc.similarity(new_doc)
    return (new_sentence, similarity_score)

def build_synonyms(sentences):
    construct_sentences = set([])
    doc = nlp(sentences)
    original_tokens = [token.text for token in doc]
    index_to_lemmas ={}

    for index, token in enumerate(doc):
        index_to_lemmas[index] = set([])
        index_to_lemmas[index].add(token)

        if token.pos_ == 'NOUN' and len(token.next) >= 3:
            pos = wn.NOUN
        elif token.pos_ == 'VERB' and len(token.text) >= 3:
            pos = wn.VERB
        elif token.pos_ == 'ADV' and len(token.text) >= 3:
            pos = wn.ADV
        elif token.pos_ == 'ADJ' and len(token.text) >= 3:
            pos = wn.ADJ
        else:
            continue

        for synonym_set in wn.synsets(token.text, pos):
            for lemma in synonym_set.lemmas():
                new_tokens = original_tokens.copy()
                new_tokens[index] = lemma.name()
                sentence_and_score = build_sentence(doc, new_tokens)
                construct_sentences.add(sentence_and_score)
                index_to_lemmas[index].add(lemma.name())

    count = sum([ len(words) for words in index_to_lemmas.values() ])

    for i in xrange(min(count, 40)):
        new_tokens = []
        for index, words in sorted(index_to_lemmas.items(), key = lambda x : x[0]):
            token = random.sample(index_to_lemmas[index], 1)[0]
            new_tokens.append(str(token))

        sentence_and_score = build_sentence(doc, new_tokens)
        construct_sentences.add(sentence_and_score)

    return construct_sentences


def paraphraser(sentences):
    return build_synonyms(sentences)

if __name__ == '__main__':
    print("yes")
    main()