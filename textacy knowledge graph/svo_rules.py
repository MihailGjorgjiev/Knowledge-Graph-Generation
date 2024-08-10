import nltk
import inflect
from nltk.corpus import wordnet as wn

# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('omw-1.4')
p = inflect.engine()


def is_plural(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return False
    return word != lemma

def plural_to_singular(word):
    """Convert a plural word to singular"""
    if p.singular_noun(word):
        return p.singular_noun(word)
    return word


def rules(sop_list_strings):
    "fix multiple relationships in a sentence towards the same subject"
    for i in range(len(sop_list_strings)):
        if i > 0 and sop_list_strings[i][0] == "that":
            sop_list_strings[i][0] = sop_list_strings[i - 1][0]

    "fix mapping one entity to itself"
    sop_list_strings = [el for el in sop_list_strings if el[0] != el[2]]

    "exclude punctuation symbols as entities"
    sop_list_strings = [el for el in sop_list_strings if len(el[0]) > 2 and len(el[1]) > 2 and len(el[2]) > 2]

    "exclude verbs presented as entities beginning with 'to' for example :to begin, to supress ..."
    "exclude verbs presented as entities ending with 'ing' for example :to begin, to supress ..."
    sop_list_strings = [el for el in sop_list_strings if el[0][:2] != 'to' and el[2][:2] != 'to']
    sop_list_strings = [el for el in sop_list_strings if el[0][-3:] != 'ing' and el[2][-3:] != 'ing']

    "convert entities from plural to singular"
    sop_list_strings = [[plural_to_singular(el[0]) if is_plural(el[0]) else el[0], el[1], plural_to_singular(el[2]) if is_plural(el[2]) else el[2]] for el in sop_list_strings]

    "remove duplicates"
    sop_list_strings = [el for el in sop_list_strings if sop_list_strings.count(el) == 1]
    return sop_list_strings
