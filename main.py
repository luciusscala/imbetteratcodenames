import random
from typing import List, Dict, Tuple
from gensim.models import KeyedVectors

class Word:
    """
    Represents a game word and its assigned color/team.
    """
    def __init__(self, word: str, color: str):
        self.word = word.lower()
        self.color = color

    def __repr__(self):
        return f"Word(word='{self.word}', color='{self.color}')"

    def print_word(self):
        print(f"{self.word} ({self.color})")


class Board:
    """Represents the codenames board containing all card assignments."""

    # Team/color constants
    RED_TEAM = "red"
    BLUE_TEAM = "blue"
    BYSTANDER = "tan"
    ASSASSIN = "black"

    def __init__(self, words: List[str]):
        """
        Initializes board by randomly assigning words to colors according to Codenames rules.
        - 9x blue, 8x red, 7x bystander, 1x assassin
        """
        # Set up color assignments to ensure correct distribution
        colors = (
            [self.BLUE_TEAM] * 9 +
            [self.RED_TEAM] * 8 +
            [self.BYSTANDER] * 7 +
            [self.ASSASSIN] * 1
        )
        random.shuffle(colors)  # Randomize color distribution

        # Assign each word its color
        self.words: List[Word] = []
        self.teams: Dict[str, List[Word]] = {self.RED_TEAM: [], self.BLUE_TEAM: [], self.BYSTANDER: [], self.ASSASSIN: []}
        for w, c in zip(words, colors):
            word_obj = Word(w, c)
            self.words.append(word_obj)
            self.teams[c].append(word_obj)

    def print_team_words(self):
        """Prints out all words by team, for debug."""
        print("Blue words:")
        for word in self.teams[self.BLUE_TEAM]:
            print(f"  {word.word}")
        print("Red words:")
        for word in self.teams[self.RED_TEAM]:
            print(f"  {word.word}")
        print("Bystanders:")
        for word in self.teams[self.BYSTANDER]:
            print(f"  {word.word}")
        print("Assassin:")
        for word in self.teams[self.ASSASSIN]:
            print(f"  {word.word}")

    def get_team_words(self, team: str) -> List[str]:
        """Returns all word strings for a given team."""
        return [w.word for w in self.teams[team]]

    def get_all_board_words(self) -> List[str]:
        """Returns all words on the board."""
        return [w.word for w in self.words]


def clue_scores(team: str, candidates: List[str], board: Board, model: KeyedVectors) -> Dict[str, float]:
    """
    Calculates a clue score for a list of candidates for a given team.
    - This favors clues close to team's words, but penalizes for being close to other/assassin words.
    - Returns a dict: candidate -> score (higher is better)
    """
    scores = {}
    # Get Word objects for each team
    my_words = board.teams[team]
    opposing = board.teams[Board.RED_TEAM if team == Board.BLUE_TEAM else Board.BLUE_TEAM]
    assassin = board.teams[Board.ASSASSIN]

    for clue in candidates:
        # Sum similarity to team words
        team_score = sum(model.similarity(clue, w.word) for w in my_words)
        # Penalize for closest similarity to opposing/assassin words
        danger = max([model.similarity(clue, w.word) for w in opposing + assassin])
        # The higher the team_score and the lower the danger, the better
        scores[clue] = team_score / (danger + 1e-6)
    return scores


def main():
    """
    Command-line driver for demonstrating spymaster clue generation using word2vec and Board logic.
    1. Loads words and selects 25 for the game.
    2. Configures board and assigns teams/colors.
    3. Loads a pretrained word2vec model.
    4. Interactively chooses spymaster team, computes clues, and prints best options.
    """
    # --- Step 1: Load and shuffle words ---
    file_path = "words.txt"
    with open(file_path, "r") as file:
        all_words = [line.strip() for line in file if line.strip()]
    random_words = random.sample(all_words, 25)

    # --- Step 2: Initialize board ---
    board = Board(random_words)
    board.print_team_words()  # Debug print

    # --- Step 3: Load pretrained word2vec model ---
    model_path = "model.bin"
    print("Loading word2vec model (may take a while)...")
    word2vec = KeyedVectors.load_word2vec_format(model_path, binary=True)

    # --- Step 4: Let user pick a team for spymaster clue ---
    user_choice = ""
    while user_choice not in [Board.RED_TEAM, Board.BLUE_TEAM]:
        user_choice = input("Which team are you giving clues for? (red/blue): ").strip().lower()

    # --- Step 5: Get the words for that team, validate with the model's vocab ---
    team_words = board.get_team_words(user_choice)
    valid_team_words = [w for w in team_words if w in word2vec.key_to_index]
    if not valid_team_words:
        print("No valid team words in model vocabulary. Try again with different words.")
        return

    # --- Step 6: Collect candidate clues (from model, but not on board, and single words only) ---
    # This uses the model's most_similar. You may replace this step with more advanced clue searching!
    candidates = word2vec.most_similar(positive=valid_team_words, topn=200)
    candidate_words = [w for w, _ in candidates if w not in board.get_all_board_words() and "_" not in w]

    print(f"\nTop candidate clues (raw): {candidate_words[:10]}")

    # --- Step 7: Score all clue candidates for best one ---
    best_clue_scores = clue_scores(user_choice, candidate_words, board, word2vec)
    best_clue = max(best_clue_scores, key=best_clue_scores.get)

    # --- Step 8: Output for demonstration/debugging ---
    print(f"\nBest clue for {user_choice.upper()}: '{best_clue}' (Score: {best_clue_scores[best_clue]:.4f})")
    print("All scored clues (top 10):")
    for clue in sorted(best_clue_scores, key=best_clue_scores.get, reverse=True)[:10]:
        print(f"  {clue:15} {best_clue_scores[clue]:.4f}")

    # --- Improvements Discussion: ---
    print("""
MODEL IMPROVEMENT TIPS:
- Use more advanced heuristics to pick clues that link multiple team words but avoid accidental overlap with opponent/assassin words.
- Employ banned clue filtering (e.g., for inflections/parts) and frequency heuristics to avoid rare or illegal clues.
- Consider beam search, combinatorial search, or ensemble techniques for smarter clue choices.
- Add tests to empirically evaluate risk/reward.
- Try richer models (BERT, ConceptNet) for smarter context!
""")

if __name__ == "__main__":
    main()
