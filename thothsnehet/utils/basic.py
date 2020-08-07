

from nltk import word_tokenize
import numpy as np

from os import listdir
from os.path import isfile, join
from typing import List
import nltk
from spacy import displacy
import en_core_web_sm

def get_files_in_directory(path:str) -> List[str]:
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

def merge_dictionaries(dict_list: List[str]) -> dict:
    all_dictionary = {}
    for dictionary in dict_list:
        # key = list(dictionary.keys())[0]
        # all_dictionary[key] = dictionary[key]
        all_dictionary = {**all_dictionary, **dictionary}
    return all_dictionary

def get_all_text_from_definitions(words_dictionary: dict)->str:
    """ Combines all the text from the definition given in the dictionary
    """
    text = ""
    for word in words_dictionary.keys():
        word_dict = words_dictionary[word]
        for word_type in word_dict.keys():
            text += " ".join(word_dict[word_type])+ " "
    return text

def get_unique_words(text:str) -> List[str]:
    """Returns list with the unique words lowered in the text
    """
    tokenized_word=word_tokenize(text)
    tokenized_word = [str(x).lower() for x in tokenized_word]
    unique_words = np.unique(tokenized_word)
    return unique_words

def nltk_pos_tag(text:str) ->str:
    text = nltk.word_tokenize(text)
    text = nltk.pos_tag(text)
    return text


def get_first_root(definition: str, nlp = None):

    if nlp is None:
        nlp = en_core_web_sm.load()

    doc = nlp(definition)
    json_doc = doc.to_json()
    for token in json_doc["tokens"]:
        if token["dep"] == "ROOT":
            return json_doc["text"][token["start"]:token["end"]]
    
    return None

def display_image_definition(definition:str, nlp = None):

    if nlp is None:
        nlp = en_core_web_sm.load()

    doc = nlp(definition)
    displacy.render(doc, jupyter=True, style='dep')