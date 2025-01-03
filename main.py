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

def clue_scores(team, candidates, board, model):
    scores = {}

    #set team and opposing team words
    if team == "blue":
        my_team = board.blue
        opposing_team = board.red
    else:
        my_team = board.red
        opposing_team = board.blue
    
    for clue in candidates:
        #calculate how similar to team words
        team_similarity = sum(model.similarity(clue, word.word) for word in my_team)

        #calculate how different from opposing words and assasain (using max similarity of all words)
        max_non_team_similarity = max([model.similarity(clue, word.word) for word in opposing_team + board.black])

        #scoring function
        scores[clue] = team_similarity / (max_non_team_similarity + 1e-6)  # Avoid division by zero
   
    return scores

def main():
    """
    main method that runs program
    """
    file_path = "words.txt"
    with open(file_path, "r") as file:
        words = [line.strip() for line in file]

    #select 30 random words out of all words in txt (game only needs 25)
    random_words = random.sample(words, 30)

    board = Board(random_words)


    # Path to the downloaded model
    model_path = "model.bin"

    # Load the model (binary format)
    word2vec = KeyedVectors.load_word2vec_format(model_path, binary=True)

    #get input on which team to be spy master for
    user_input = str(input("Red or Blue? ")).lower()

    if user_input == "red":
        team = [word.word for word in board.red]
        board.print(board.red)
    else:
        team = [word.word for word in board.blue]
        board.print(board.blue)
    
    #filter out words not in model vocab
    valid_words = [word for word in team if word in word2vec.key_to_index]

    if not valid_words:
        print("No valid words from the team are present in the model's vocabulary.")
        return

    # Get the most similar words for the valid team words
    candidates = word2vec.most_similar(positive=valid_words, topn=100)


    #a list of the candidate words which are not in board list of words
    filtered_candidates = [word for word, _ in candidates if word not in board.list]

    #find best clue
    best_clues = clue_scores(user_input, filtered_candidates, board, word2vec)
    best_clue = max(best_clues)

    #display results
    print(best_clue)

if __name__ == "__main__":
    main()


