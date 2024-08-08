import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import QTimer

class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()
        self.timer_min= 15
        self.timer_max=60
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Whack-A-Mole')

        # makes the player to enter game duration
        self.time_limit, ok = QInputDialog.getInt(self, 'Input Dialog', 'Enter the game duration in seconds (15-60):',self.timer_min, self.timer_max)

        # Set up timer to end the game after the specified time limit
        QTimer.singleShot(self.time_limit * 1000, self.end_game)

        # Initialize game variables
        self.grid_size = 5
        self.score = 0
        self.mole_button = (0, 0)
        
        # Set up the grid layout
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        # Create buttons for the grid
        self.buttons = [[QPushButton(' ') for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                button = self.buttons[row][col]
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda ch, row=row, col=col: self.mole_clicked(row, col))
                self.grid.addWidget(button, row, col)
        
        # Place the initial mole
        self.place_mole()

    def place_mole(self):
        row, col = self.mole_button
        self.buttons[row][col].setText(' ')

        new_row, new_col = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
        self.mole_button = (new_row, new_col)
        self.buttons[new_row][new_col].setText('mole')

    def mole_clicked(self, row, col):
        if (row, col) == self.mole_button:
            self.score += 1
            self.place_mole()

    def end_game(self):
        QMessageBox.information(self, 'Game Over', f'Game Over! Your score is {self.score}')
        with open('score.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WhackAMoleGame()
    window.show()
    sys.exit(app.exec_())
