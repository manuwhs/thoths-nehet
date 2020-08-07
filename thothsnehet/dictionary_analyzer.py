import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from .dictionary_crawler import DictionaryCrawler
from .utils.basic import merge_dictionaries, get_unique_words, get_all_text_from_definitions
from .utils.basic import get_files_in_directory



class DictionaryAnalyzer():
    """Big class that instantiates the smaller ones.
    """
    def __init__(self):
        self.words = {"word":["fuck", "me"], "caca":["fuck", "you","the"]}
        self.selected_words = ["word","caca"]
        self.G = nx.DiGraph()
        
    def add_selected_words(self):
        for word in self.selected_words:
            self.add_word(word)
            
    def add_word(self,word):
        list_words = self.words[word]
        unique_words = np.unique(list_words)
        
        edges = []
        for word_definition in unique_words:
            edges.append((word,word_definition,{'w':1}))
            
        self.G.add_nodes_from(list_words)
        self.G.add_nodes_from([word])
        self.G.add_edges_from(edges)
    
    def create_words_dict(self):
        pass