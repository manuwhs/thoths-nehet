
class Netword():
    def __init__(self):
        self.word_to_node = dict()# Dictionary with word to node in the hierarchy
        self.tree_peaks = []
    
    def add_node(word, parent):
        node = WordNode(word, parent)

        # If the parent exists:
        if parent in word_to_node.keys():
            parent_node = word_to_node[parent]
            parent_node.children.append(node)
        else:
            # If it does not exist, then add it to the peaks 
            tree_peaks.append(word)
        word_to_node[word] = node

    
class WordNode():
    def __init__(word, parent):
        self.word = word
        self.parent = parent
        self.chilren = []