import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QGridLayout, QWidget, QComboBox, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtCore import Qt

class Codenames(QMainWindow):
    """
    class which defines the main window interface with PyQt
    """
    #constants
    GRID_DIMENSION = 5

    def __init__(self):
        super().__init__()
        self.setWindowTitle("codenames")
        self.setGeometry(500, 250, 500, 500)

        self.initUI()
    
    def initUI(self):
        #main layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        #create main layout
        main_layout = QVBoxLayout(central_widget)

        #create grid layout
        self.grid_layout = QGridLayout()

        self.tiles = [] #TODO tiles (bottons) for the grid
        for i in range(self.GRID_DIMENSION):
            for j in range(self.GRID_DIMENSION):
                word = "hello" #TODO fetch real words
                tile_button = QPushButton(word)
                
                #style
                tile_button.setFont(QFont("Arial", 14))
                tile_button.setStyleSheet("background-color: #cf9846;")
                tile_button.setFixedSize(75, 75)
                
                self.grid_layout.addWidget(tile_button, i, j) #add widget to grid

        # Set spacing between columns and rows
        self.grid_layout.setHorizontalSpacing(5)  # Horizontal space between columns
        self.grid_layout.setVerticalSpacing(20)    # Vertical space between rows

        # Add the grid layout to the main layout
        main_layout.addLayout(self.grid_layout)



def main():
    app = QApplication(sys.argv)
    window = Codenames()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
