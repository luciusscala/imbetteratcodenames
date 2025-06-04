<<<<<<< HEAD
# Codenames Spymaster (Python, PyQt5 & Word2Vec)

A complete Codenames board game experience with both a professional, interactive GUI (PyQt5) and a command-line spymaster clue research tool (leveraging Word2Vec).  
Modular, easy to extend, and perfect for both gameplay and computational linguistics experimentation.

---

## Project Overview

This project implements the classic party game **Codenames** using Python. It consists of two main components:

- **Interactive Game Board (gui.py):**  
  A visually clean, user-friendly 5x5 Codenames board playable directly in a GUI. Handles all core gameplay, turns, scoring, clues, and win conditions—no setup required.
- **AI Spymaster Research Tool (main.py):**  
  A command-line analytic tool for generating model-based clues with Gensim’s Word2Vec and detailed scoring for researchers and AI developers.

Words for the board are pulled from `words.txt` (classic Codenames pool), and the AI tool expects a pre-trained `model.bin` (e.g., GoogleNews word2vec) for advanced clue generation.

---

## Project Flow & How It Works

### Game Board (`gui.py`)

1. **Game Initialization**
   - The GUI window launches a 5x5 grid populated with randomly selected words from `words.txt`.
   - Blue always starts (per standard Codenames). Teams are assigned their roles in secret.

2. **Gameplay Loop**
   - At the start of each turn, the GUI "spymaster" gives a clue (random word, count)—displayed at the top. (You can later connect this to a model for smarter clues.)
   - Players guess by clicking unrevealed word cards:
     - **Correct Guess (teammate):** Card is revealed, guess again (if guesses remain).
     - **Incorrect Guess (opponent or bystander):** Card is revealed, turn ends automatically after a short notification.
     - **Assassin Guess:** Card is revealed, game ends instantly with loss for that team.

3. **Automatic Turn and Score Management**
   - Teams continue guessing until they run out of guesses or miss.
   - All turns, win conditions, and game control flows are automated—no manual state resets.
   - Score tracker at the top shows how many cards each team has left; interface updates smoothly after every guess.
   - Clear status messages communicate game progress ("bystander", "opponent", "assassin", victory).

4. **Accessibility**
   - All card and label text is black for optimal readability and visual clarity.
   - Layout, spacing, and fonts are chosen for maximum usability and clean design.

5. **Easy to Extend**
   - The game logic and clue generator are modular—swap in a smarter clue model easily by editing `generate_clue()`.

### Spymaster AI Research Tool (`main.py`)

1. **Board Setup**
   - 25 words are drawn randomly from `words.txt`.
   - Board and team-word assignments are printed for reference.

2. **Model Loading**
   - Loads a pre-trained word2vec binary model (supply as `model.bin` in the root folder).

3. **Clue Generation and Scoring**
   - Asks which team you are playing.
   - Finds the best clues according to the word2vec similarity between candidate clues and the respective team's words, penalizing for closeness to opponents/assassin.
   - Prints a ranked list of best clue candidates for further analysis or experimentation.

4. **For Advanced Research**
   - The modular clue scorer and candidate picker can be swapped out for advanced clue-generation algorithms, new models, or automated simulations.

---

## File Structure

| File         | Purpose                                                                                 |
| ------------ | --------------------------------------------------------------------------------------- |
| `gui.py`     | Complete PyQt5 GUI game implementation, with all gameplay managed by a clean interface. |
| `main.py`    | Command-line AI/word2vec clue research tool, modularized for experimentation.           |
| `words.txt`  | Word pool (classic Codenames words, one per line).                                      |
| `model.bin`  | (User supplies) Pre-trained word2vec binary file (for `main.py` AI work).              |

---

## Quick Start

### Playing in the GUI

```bash
python gui.py
```
- Just run and play! All logic occurs via clickable cards.
- See live scores, turn status, and readable game messages.
- Clues are randomly generated unless you connect a model.

### Running the Spymaster AI Research Tool

```bash
python main.py
```
- For advanced users/AI researchers.
- Requires Gensim and a word2vec model (`model.bin` in the root).

---

## Customization & Extension

- To connect the AI clue generator to the GUI, modify `generate_clue()` in `gui.py` to call model-based logic.
- Both CLI and GUI are cleanly componentized for testing strategies, new models, or altered rules.
- You can upgrade card styles, add network play, or develop your own spymaster agents using these foundations.

---

## Credits

- Inspired by Vlaada Chvátil’s Codenames board game.
- Model integration and similarity scoring with [Gensim](https://radimrehurek.com/gensim/).
- GUI crafted with PyQt5 and user-focused design.

---

## License

For educational and research uses only. Respect Codenames IP for any commercial applications.
=======
# imbetteratcodenames

An attempt to create a Spymaster for the game Codenames which gives the, semantically, most optimal guess for any given generated board. Gui is incomplete as of now but CLI is implemented.
>>>>>>> 62e8f7f6e3d344b203cc95521049a4586cf3a48d
