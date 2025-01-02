import random
from gensim.models import KeyedVectors

class Word:
    """
    Word class that defines the properties of each word in the game
    """
    def __init__(self, word, color):
        self.word = word.lower()
        self.color = color
    
    def print_word(self):
        print(self.word + " " + self.color)
    
class Board:
    """
    Board class that assigns a list of words to the colors/teams of the game
    """
    #constants
    RED_TEAM = "red"
    BLUE_TEAM = "blue"
    BYSTANDER = "tan"
    ASSASAIN = "black"

    #constructor
    def __init__(self, words):
        self.red = []
        self.blue = []
        self.tan = []
        self.black = []
        self.list = self.set_words(words)
        
    #method: assigns words to colors
    def set_words(self, words):
        colors = [self.BYSTANDER] * 7 + [self.ASSASAIN] * 1 + [self.RED_TEAM] * 8 + [self.BLUE_TEAM] * 9
        random.shuffle(colors)

        #set each word with a random color
        list = []
        for i in range(len(colors)):
            word = Word(words[i], colors[i])
            list.append(word)
            
            #add to other variables
            if colors[i] == self.RED_TEAM:
                self.red.append(word)
            elif colors[i] == self.BLUE_TEAM:
                self.blue.append(word)
            elif colors[i] == self.BYSTANDER:
                self.tan.append(word)
            else:
                self.black.append(word)
            
        
        return list
    
    #method: prints
    def print(self, array):
        #assumes array of Word objects
        for i in range(len(array)):
            array[i].print_word()

def clue_scores(candidates, board, model):
    pass

def main():
    """
    main method that runs program
    """
    file_path = "words.txt"
    with open(file_path, "r") as file:
        words = [line.strip() for line in file][:25]

    board = Board(words)


    # Path to the downloaded model
    model_path = "model.bin"

    # Load the model (binary format)
    word2vec = KeyedVectors.load_word2vec_format(model_path, binary=True)

    #get input on which team to be spy master for
    input = str(input("Red or Blue? ")).lower()

    if input == "red":
        candidates = word2vec.most_similar(positive=board.red, topn=100)
    else:
        candidates = word2vec.most_similar(positive=board.blue, topn=100)

    #a list of the candidate words which are not in board list of words
    filtered_candidates = [word for word, _ in candidates if word not in board.list]


    board.print(board.red)

if __name__ == "__main__":
    main()


