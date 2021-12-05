import spacy
from spacy_langdetect import LanguageDetector

# python -m spacy download en
nlp = spacy.load('en')
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True)

def cleanup(text):
    text = text.replace("\n", " ")
    if word_count > 512:
        text = ' '.join(word_list[:511])
    return text

def usable(text):
    word_list = text.split()
    word_count = len(word_list)
    if word_count > 750:
        return False

    doc = nlp(text)
    detect_language = doc._.language
    if detect_language.get("language") != 'en':
        return False
    else:
        return True
