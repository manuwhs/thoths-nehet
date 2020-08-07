from typing import List
import pathlib
import os
from .utils.subprocess import call_subprocess
import json
from .utils.basic import merge_dictionaries, get_unique_words, get_all_text_from_definitions
from .utils.basic import get_files_in_directory


PATH = str(pathlib.Path(__file__).parent)


class DictionaryCrawler():
    """This class is a python interface that calls the scrapy spiders from the command line in order to crawl data.
    """

    def __init__(self, storage_path: str = "./", dictionary_source: str = "oxford"):
        """ Class to download the data if needed.
        It allows for easy crawling.
        """
        self.storage_path = os.getcwd() + "/" + storage_path
        self.dictionary_source = dictionary_source
        self.crawlers_path = PATH + "/scrapers/dictionary_crawler/spiders/"

        self.words_dict = dict()

    def crawl_definitions(self, words: List[str], filename: str = "words.jl", only_if_missing: bool = False, n_max_words: int = 2, verbose: int = 0) -> List[str]:
        """ It scraps the provided words from the source already set in self.dictionary_source.
        In essensce, the down

        Args:
            words (List[str]): List of words to be crawled.
            filename (str, optional): Name of the file where the crawled words will be stored in jason lines format. The new definitions will be appended at the end of the file if it already exists
            only_if_missing (bool, optional): If True, it only downloads the words that are missing in the word_dict.
            n_max_words (int, optional): Number of maximum words that the process crawler will handle. If the requested words is higher, it will make sequential calls to the scrapper in new processes. Defaults to 5.
            verbose (int, optional): Level of print information about the crawling. Defaults to 0.
        """
        if isinstance(words, str):
            words = words.split(" ")

        if only_if_missing:
            words = list(set(words).difference(self.words))

        if len(words) == 0:
            print("No words to download")
            return None, None, None
        # We need to temporarily change path to the directory where the scrapy crawlers are
        cwd = os.getcwd()
        file_path = self.storage_path + filename
        os.chdir(self.crawlers_path)

        # Crawl in handlable sets of words. The crawler is called from the command line 
        # and it has a limit of text we can call the command with. Therefore we have a limitation of words.
        n_words = len(words)
        i = 0
        while i < n_words: # While we are not done processing all words.
            words_set = [words[i + j]
                         for j in range(min(n_max_words, n_words-i))]
            cmd = f"scrapy crawl {self.dictionary_source} -o {file_path} -a words={','.join(words_set)}"
            if verbose == 1:
               
                print("Processing the words: ", words_set)
                print(cmd)

            # TODO: Handle out interruption, otherwise we cannot stop it
            if False:
                try:
                    output, error, return_code = call_subprocess(cmd=cmd)

                except:
                    print("Error downloading")
                    print(cmd)
                    output, error, return_code = [None, None, None]
            else:
                output, error, return_code = call_subprocess(cmd=cmd)
            i += len(words_set)

        # Return back to the original directory
        os.chdir(cwd)

        return output, error, return_code

    def crawl_definitions_recursively(self, word: str, recursive_depth: int = 1):
        word_downloads_filename = word + ".jl"

        all_still_unknown_words = []
        all_unique_words = []

        for r in range(recursive_depth):
            print(f"------ Recursion level {r+1}/{recursive_depth}-------")
            if r == 0:
                words = [word]

            for word in words:
                print(f"Source word: {word}")
                # Get all the vocabulary of the definition of the word that we do not know.
                if word not in self.words:
                    process_results = self.crawl_definitions(
                        word, word_downloads_filename, only_if_missing=True, verbose=1)
                    self.add_crawled_words(word_downloads_filename)

                unique_words = self.get_unique_words_from_definition(word)
                n_initial_unique_words = len(unique_words)

                # Remove the ones we know already we cannot download
                unique_words  = list(set(unique_words).difference(all_still_unknown_words))
                unknown_words = self.get_unknown_words(unique_words)

                print(f"--> {len(unknown_words)}/{len(unique_words)} unknown to unique words in definitions")
                print(f"--> {n_initial_unique_words-len(unique_words)} words we already know we cannot get the definition to")
                # print(list(set(unique_words).intersection(all_still_unknown_words)))

                # Crawl the words and add them to the dictionary
                process_results = self.crawl_definitions(
                    unknown_words, word_downloads_filename, only_if_missing=True, verbose=1)
                self.add_crawled_words(word_downloads_filename)

                # words that we still could not find the meaning in the dictionary
                still_unknown_word = self.get_unknown_words(unknown_words)

                all_still_unknown_words.extend(still_unknown_word)
                all_unique_words.extend(unique_words)

            # The words for the next iteration are those of the previous definitions that are not in the still_unknown_word group
            # This is done for optimization, avoiding looking for them again.
            words = list(set(all_unique_words).difference(all_still_unknown_words))

        return all_unique_words, all_still_unknown_words

    def get_unique_words_from_definition(self, word: str, only_unkwnow=False):
        """ Returns the words from the definition that we do not know
        """
        word_dict = {word: self.words_dict[word]}
        text = get_all_text_from_definitions(word_dict)
        unique_words = get_unique_words(text)

        if only_unkwnow:
            unique_words = self.get_unknown_words(unique_words)
        return unique_words

    def read_crawled_words(self, filename: str):
        """ The crawled words are stored in jason lines format
        """
        file_path = self.storage_path + filename

        with open(file_path) as f:
            definitions = [json.loads(line) for line in f]

        definitions = merge_dictionaries(definitions)
        return definitions

    def load_definitions(self):
        """ Loads the definitons from the storage place
        This include:
            - List of words in the
        """

        dictionary_files = get_files_in_directory(
            self.storage_path)

        dictionary_list = []
        for file in dictionary_files:
            definitions = self.read_crawled_words(file)
            dictionary_list.append(definitions)

        self.words_dict = merge_dictionaries(dictionary_list)

    def add_crawled_words(self, filename: str):
        definitions = self.read_crawled_words(filename)
        self.words_dict = {**self.words_dict, **definitions}

    def get_unknown_words(self, words: List[str]):
        unknown_words = list(set(words).difference(self.words))
        return unknown_words

    @property
    def words(self):
        return list(self.words_dict.keys())
