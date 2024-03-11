import spacy
import textacy

class KnowledgeExtraction:

    def retrieveKnowledge(self, textInput):
        nlp = spacy.load('en_core_web_sm')
        text = nlp(textInput)
        text_ext = textacy.extract.subject_verb_object_triples(text)
        return list(text_ext)
