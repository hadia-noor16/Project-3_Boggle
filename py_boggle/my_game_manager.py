import copy
import random
from typing import List, Optional, Set, Tuple

from py_boggle.boggle_dictionary import BoggleDictionary
from py_boggle.boggle_game import BoggleGame

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

SHORT = 3
CUBE_SIDES = 6

class MyGameManager(BoggleGame):
    """Your implementation of `BoggleGame`
    """

    def __init__(self):
        """Constructs an empty Boggle Game.

        A newly-constructed game is unplayable.
        The `new_game` method will be called to initialize a playable game.
        Do not call `new_game` here.

        This method is provided for you, but feel free to change it.
        """

        self.board: List[List[str]] # current game board
        self.size: int # board size
        self.words: List[str] # player's current words
        self.dictionary: BoggleDictionary # the dictionary to use
        self.last_added_word: Optional[List[Tuple[int, int]]] # the position of the last added word, or None

    def new_game(self, size: int, cubefile: str, dictionary: BoggleDictionary) -> None:
        """This method is provided for you, but feel free to change it.
        """
        with open(cubefile, 'r') as infile:
            faces = [line.strip() for line in infile]
        cubes = [f.lower() for f in faces if len(f) == CUBE_SIDES]
        if size < 2 or len(cubes) < size*size:
            raise ValueError('ERROR: Invalid Dimensions (size, cubes)')
        random.shuffle(cubes)
        # Set all of the game parameters
        self.board =[[random.choice(cubes[r*size + c]) 
                    for r in range(size)] for c in range(size)]
        self.size = size
        self.words = []
        self.dictionary = dictionary
        self.last_added_word = None


    def get_board(self) -> List[List[str]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.board

    def find_word_in_board(self, word: str) -> Optional[List[Tuple[int, int]]]:
        """Helper method called by add_word()
        Expected behavior:
        Returns an ordered list of coordinates of a word on the board in the same format as get_last_added_word()
        (see documentation in boggle_game.py).
        If `word` is not present on the board, return None.
        """
        word = word.lower()

        possible_locations = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        def search(row, col, index, path):
            if self.board[row][col] != word[index]:  # if board letter does not match word[index]
                return None

            if (row,col) in path:                   # if one cell is already added, don't include that letter in path again
                return None

            path=path+[(row,col)]                   # otherwise add location of that letter to path

            if index == len(word)-1:                # if word is finished, return its path
                return path

            for change_row, change_col in possible_locations:   # keep changing rows, cols from possible_locations list of tuples
                new_row = row + change_row
                new_col = col + change_col

                #search (new_row, new_col, index+1, path)

                if  0 <= new_row < self.size and   0 <= new_col < self.size:   # new_row and new_col should be >=0 but less that size of board
                    result=search(new_row, new_col, index+1, path)            # index[word] is incremented by 1 to search for next letter of the word in board

                    if result:
                        return result

            return None

        # this will run first, starting with first row,col cell in board
        for row in range(self.size):
            for col in range(self.size):
                result = search(row, col, 0, [])   # search is called to keep looking in all directions.
                   # if self.board[row][col] == word[0]:
                      #  path=[(row,col)]
                if result:
                    return result
        return None



        #raise NotImplementedError("method find_word_in_board") #
    def add_word(self, word: str) -> int:
        """This method is provided for you, but feel free to change it.
        """
        word = word.lower()
        if (len(word) > SHORT and word not in self.words and self.dictionary.contains(word)):
            location = self.find_word_in_board(word)
            if location is not None:
                self.last_added_word = location
                self.words.append(word)
                return len(word) - SHORT
        return 0

    def get_last_added_word(self) -> Optional[List[Tuple[int, int]]]:
        """This method is provided for you, but feel free to change it.
        """
        return self.last_added_word

    def set_game(self, board: List[List[str]]) -> None:
        """This method is provided for you, but feel free to change it.
        """
        self.board = [[c.lower() for c in row] for row in board]

    def get_score(self) -> int:
        """This method is provided for you, but feel free to change it.
        """
        return sum([len(word) - SHORT for word in self.words])

    def dictionary_driven_search(self) -> Set[str]:
        """Find all words using a dictionary-driven search.

        The dictionary-driven search attempts to find every word in the
        dictionary on the board.

        Returns:
            A set containing all words found on the board.
        """

        words_in_dict=set()

        for word in self.dictionary:
            if len(word) > SHORT:
                result=self.find_word_in_board(word)

                if result is not None:
                    if word not in self.words:
                         words_in_dict.add(word)

        return words_in_dict

        #raise NotImplementedError("method dictionary_driven_search") #

    def board_driven_search(self) -> Set[str]:
        """Find all words using a board-driven search.

        The board-driven search constructs a string using every path on
        the board and checks whether each string is a valid word in the
        dictionary.

        Returns:
            A set containing all words found on the board.
        """

        found_words=set()
        possible_locations= [(-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]

        def search(row, col, collected_word, path):
            if (row,col) in path:
                return None

            path = path + [(row, col)]

            new_word= collected_word + self.board[row][col]  #already collected word so far + present cell letter

            if not self.dictionary.is_prefix(new_word):   # if new word is not a prefix in dict, stop searching more
                return None

            if self.dictionary.contains(new_word) and len(new_word) > SHORT: #if dict contains that word and >3
                if new_word not in self.words:   # word not already found by user
                    found_words.add(new_word)


            for change_row, change_col in possible_locations:  # keep changing rows, cols from possible_locations list of tuples
                new_row = row + change_row
                new_col = col + change_col


                if 0 <= new_row < self.size and 0 <= new_col < self.size:  # new_row and new_col should be >=0 but less that size of board
                    search(new_row, new_col, new_word,path)

            # this will run first, starting with first row,col cell in board
        for row in range(self.size):
            for col in range(self.size):
                search(row, col, "", [])  # search is called to keep looking in all directions.
                    # if self.board[row][col] == word[0]:
                    #  path=[(row,col)]

        return found_words



        #raise NotImplementedError("method board_driven_search")
