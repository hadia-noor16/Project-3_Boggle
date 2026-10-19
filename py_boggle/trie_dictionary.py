import typing
from typing import Optional, Dict
from collections.abc import Iterator

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but 
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children : Dict[str, TrieNode] = {} # maps a child letter to its TrieNode class
        self.is_word = False # whether or not this Node is a valid word ending


class TrieDictionary(BoggleDictionary):
    """
    Your implementation of BoggleDictionary.
    Several functions have been filled in for you from our solution, but you are free to change their implementations.
    Do NOT change the name of self.root, as our autograder will manually traverse using self.root
    """

    def __init__(self):
        self.root : TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        # Remember to add every word to the trie, not just the words over some length.
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                current_node=self.root
                for w in word:
                    if w not in current_node.children:
                        current_node.children[w] = TrieNode()

                    current_node = current_node.children[w]
                current_node.is_word=True


       # raise NotImplementedError("method load_dictionary") #

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """
        Traverse will traverse the Trie down a given path of letters `prefix`.
        If there is ever a missing child node, then returns None.
        Otherwise, returns the TrieNode referenced by `prefix`.
        """
        current_node = self.root
        for letter in prefix:
            if letter not in current_node.children:
                return None
            current_node = current_node.children[letter]
        return current_node


        #raise NotImplementedError("method traverse") #

    def is_prefix(self, prefix: str) -> bool:

        test=self.traverse(prefix)
        if test is None:
            return False
        else:
            return True


        raise NotImplementedError("method is_prefix") #

    def contains(self, word: str) -> bool:
        current_node=self.root
        for letter in word.lower():
            if letter not in current_node.children:
                return False
            current_node = current_node.children[letter]

        if current_node.is_word:
            return True
        else:
            return False



        raise NotImplementedError("method contains") #

    def __iter__(self) -> typing.Iterator[str]:

        words=[]    # an empty list of words

        def helper(current_node, current_prefix):  # a new func initializing with current node, current prefix
            if current_node.is_word:                                       #current prefix will keep adding letters starting from root, until is_word==True
                words.append(current_prefix)                           #if is_word is true, it will append it in list

            for letter in current_node.children:                   # current node is root in the beginning, so starting from its first children
                helper(current_node.children[letter], current_prefix+letter)   # calling same func to see if is_word==true?
                                                                              # but this time change node to that children, also add that letter to the prefix

        helper(self.root, "")    #when the funx is first called, it's started with root, and prefix is empty string
        return iter(words)






        #raise NotImplementedError("method __iter__") #

