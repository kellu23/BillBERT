import spacy
from spacy_langdetect import LanguageDetector

# python -m spacy download en
nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

def clean_doc(text):
    text = text.replace("\n", " ")
    doc = nlp(text)
    detect_language = doc._.language
    if detect_language.get("language") == 'en':
        return text
    else:
        return -1