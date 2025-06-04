import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QGridLayout, QWidget, QMessageBox, QHBoxLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer

class Word:
    def __init__(self, word, color):
        self.word = word.lower()
        self.color = color
        self.revealed = False

class Board:
    RED_TEAM = "red"
    BLUE_TEAM = "blue"
    BYSTANDER = "tan"
    ASSASSIN = "black"
    COLOR_MAP = {
        RED_TEAM: "#EB455F",
        BLUE_TEAM: "#3b82f6",
        BYSTANDER: "#f0e68c",
        ASSASSIN: "#252422"
    }
    CARD_TEXT_COLOR = {
        RED_TEAM: "#111",
        BLUE_TEAM: "#111",
        BYSTANDER: "#111",
        ASSASSIN: "#111",
        "unrevealed": "#111"
    }

    def __init__(self, words):
        colors = (
            [self.BLUE_TEAM]*9 + [self.RED_TEAM]*8 +
            [self.BYSTANDER]*7 + [self.ASSASSIN]
        )
        random.shuffle(colors)
        self.cards = [Word(w, c) for w, c in zip(words, colors)]
        self.won = False

    def check_win(self):
        blue_left = sum(w.color == self.BLUE_TEAM and not w.revealed for w in self.cards)
        red_left = sum(w.color == self.RED_TEAM and not w.revealed for w in self.cards)
        if blue_left == 0:
            return self.BLUE_TEAM
        elif red_left == 0:
            return self.RED_TEAM
        else:
            return None

    def team_remaining(self, team):
        return sum(w.color == team and not w.revealed for w in self.cards)

class Codenames(QMainWindow):
    GRID_DIMENSION = 5

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Codenames Spymaster - PyQt5")
        self.setGeometry(300, 100, 780, 880)
        self.setStyleSheet("background-color: #FAF7F0;")
        font = QFont("Roboto", 14)
        self.setFont(font)

        self.words = self.load_words()
        self.board = Board(self.words)
        self.current_team = Board.BLUE_TEAM
        self.clue = ""
        self.clue_count = 0
        self.guesses_left = 0
        self.turn_ending = False

        self.initUI()
        self.next_clue()

    def load_words(self):
        with open("words.txt", "r") as file:
            wordlist = [line.strip() for line in file if line.strip()]
        return random.sample(wordlist, self.GRID_DIMENSION ** 2)

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(24)

        # -- Score/Info Bar --
        info_bar = QHBoxLayout()

        self.team_indicator = QLabel("")
        self.team_indicator.setFont(QFont("Roboto", 20, QFont.Bold))
        self.team_indicator.setAlignment(Qt.AlignLeft)
        self.team_indicator.setStyleSheet("color: #111;")
        info_bar.addWidget(self.team_indicator)

        info_bar.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Score tracker
        self.score_label = QLabel("")
        self.score_label.setFont(QFont("Roboto", 17, QFont.Bold))
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("color: #111;")
        info_bar.addWidget(self.score_label)

        info_bar.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.clue_label = QLabel("")
        self.clue_label.setFont(QFont("Roboto", 18, QFont.Bold))
        self.clue_label.setAlignment(Qt.AlignRight)
        self.clue_label.setStyleSheet("color: #111;")
        info_bar.addWidget(self.clue_label)

        main_layout.addLayout(info_bar)

        # -- Grid Layout --
        grid_wrap = QHBoxLayout()
        grid_wrap.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(16)
        self.grid_layout.setVerticalSpacing(18)

        self.tiles = []
        for i in range(self.GRID_DIMENSION):
            row = []
            for j in range(self.GRID_DIMENSION):
                idx = i * self.GRID_DIMENSION + j
                word = self.board.cards[idx].word
                btn = QPushButton(word.title())
                btn.setFont(QFont("Roboto", 15, QFont.Bold))
                btn.setFixedSize(110, 72)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(f"""
                    QPushButton {{
                        border-radius: 13px;
                        border: 2px solid #E6DDDE;
                        background: #FFF2F2;
                        color: #111;
                        letter-spacing: 1.5px;
                        font-size: 17px;
                        font-weight: bold;
                    }}
                    QPushButton:hover:!pressed {{
                        background: #fed1ce;
                        border: 2px solid #FFABAB;
                        color: #111;
                    }}
                """)
                btn.clicked.connect(lambda checked, idx=idx: self.handle_tile_click(idx))
                self.grid_layout.addWidget(btn, i, j)
                row.append(btn)
            self.tiles.append(row)
        grid_wrap.addLayout(self.grid_layout)
        grid_wrap.addSpacerItem(QSpacerItem(30, 1, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(grid_wrap)

        # -- Status & Controls --
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Roboto", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #111;")
        main_layout.addWidget(self.status_label)
        main_layout.addSpacing(8)

        self.continue_btn = QPushButton("End Turn / Next Clue")
        self.continue_btn.setFont(QFont("Roboto", 14))
        self.continue_btn.clicked.connect(self.finish_turn)
        self.continue_btn.setStyleSheet("""
            QPushButton {
                border-radius: 11px;
                border: 2px solid #bababa;
                background: #3b82f6;
                color: #111;
                padding: 8px 32px;
                font-weight: bold;
            }
            QPushButton:hover:!pressed {
                background: #69b3ff;
                color: #111;
            }
        """)
        main_layout.addWidget(self.continue_btn)

    def update_score(self):
        red_left = self.board.team_remaining(Board.RED_TEAM)
        blue_left = self.board.team_remaining(Board.BLUE_TEAM)
        self.score_label.setText(
            f"<span style='color:#EB455F;'>🔴 {red_left}</span> &nbsp;|&nbsp; <span style='color:#3b82f6;'>🔵 {blue_left}</span>"
        )

    def next_clue(self):
        self.turn_ending = False
        self.clue, self.clue_count = self.generate_clue(self.current_team)
        self.guesses_left = self.clue_count + 1
        team_disp = "🔵 Blue" if self.current_team == Board.BLUE_TEAM else "🔴 Red"
        self.team_indicator.setText(f"{team_disp} team's turn")
        self.clue_label.setText(f"<b>Clue:</b> {self.clue.upper()} &nbsp; <b>({self.clue_count})</b>")
        self.status_label.setText("")
        self.update_score()
        self.update_board_display()
        self.continue_btn.setEnabled(False)
        self.continue_btn.setText(f"{self.guesses_left} guesses left")

    def generate_clue(self, team):
        # TODO: Integrate word2vec logic
        all_words = set(open("words.txt").read().split())
        board_words = set(w.word for w in self.board.cards)
        possible_clues = list(all_words - board_words)
        clue = random.choice(possible_clues) if possible_clues else "???"
        count = random.randint(1, 3)
        return clue, count

    def handle_tile_click(self, idx):
        if self.guesses_left <= 0 or self.turn_ending or self.board.won:
            return
        word_obj = self.board.cards[idx]
        if word_obj.revealed:
            return

        word_obj.revealed = True
        self.update_board_display()
        self.update_score()
        self.guesses_left -= 1

        winner = self.board.check_win()
        if winner or word_obj.color == Board.ASSASSIN:
            self.turn_ending = True
            msg = f"{winner.title()} team wins!" if winner else f"Game over! {self.current_team.title()} hit the assassin and loses!"
            QTimer.singleShot(650, lambda: self.game_over(msg))
            return

        if word_obj.color != self.current_team or word_obj.color == Board.ASSASSIN:
            self.guesses_left = 0
            self.turn_ending = True
            if word_obj.color == Board.ASSASSIN:
                self.status_label.setText("💣 ASSASSIN! Turn ends — Game Over")
            elif word_obj.color == Board.BYSTANDER:
                self.status_label.setText("🟤 Bystander! Turn ends.")
            else:
                wrong_team = "🔵" if word_obj.color == Board.BLUE_TEAM else "🔴"
                self.status_label.setText(f"{wrong_team} Opponent revealed! Turn ends.")
            QTimer.singleShot(1150, self.finish_turn)
            return

        if self.guesses_left == 0:
            self.continue_btn.setEnabled(True)
            self.continue_btn.setText("End Turn / Next Clue")
            self.status_label.setText("Maximum guesses reached. Click to end turn.")
            self.turn_ending = True
        else:
            self.continue_btn.setEnabled(False)
            self.continue_btn.setText(f"{self.guesses_left} guesses left")
            self.status_label.setText("Correct! Continue guessing or end turn early.")

    def finish_turn(self):
        if self.board.won:
            return
        self.current_team = Board.BLUE_TEAM if self.current_team == Board.RED_TEAM else Board.RED_TEAM
        self.next_clue()
        self.continue_btn.setEnabled(False)
        self.turn_ending = False

    def update_board_display(self):
        for i in range(self.GRID_DIMENSION):
            for j in range(self.GRID_DIMENSION):
                idx = i * self.GRID_DIMENSION + j
                word_obj = self.board.cards[idx]
                btn = self.tiles[i][j]
                color = Board.COLOR_MAP[word_obj.color] if word_obj.revealed else "#FFF2F2"
                tcolor = "#111"
                if word_obj.revealed:
                    btn.setText(word_obj.word.upper())
                else:
                    btn.setText(word_obj.word.title())
                btn.setEnabled(not word_obj.revealed and not self.board.won)
                btn.setStyleSheet(
                    f"""
                    QPushButton {{
                        background: {color};
                        color: {tcolor};
                        border-radius: 13px;
                        border: 2px solid #E6DDDE;
                        font-size: 15px;
                        font-weight: 700;
                        letter-spacing: 1.5px;
                    }}
                    QPushButton:hover:!pressed {{
                        background: #fed1ce;
                        border: 2px solid #FFABAB;
                        color: #111;
                    }}
                    """
                )

    def game_over(self, msg):
        self.board.won = True
        self.status_label.setText(msg)
        self.clue_label.setText("<b>Game Over!</b>")
        self.team_indicator.setText("")
        for row in self.tiles:
            for btn in row:
                btn.setEnabled(False)
        self.update_score()
        QMessageBox.information(self, "Game Over", msg)

def main():
    app = QApplication(sys.argv)
    window = Codenames()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
