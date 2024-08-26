import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

class WhackAMoleGame(QWidget):
    def __init__(self):
        super().__init__()
        self.timer_max = 60
        self.timer_min = 15
        self.grid_size_min = 3
        self.grid_size_max = 5
        self.mole_move_interval = 2000  # Mole moves every 2 seconds (1000 per second)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Whack-A-Mole')

        # Prompt the user to enter the game duration
        self.time_limit, ok = QInputDialog.getInt(self, 'Input Dialog', 'Enter the game duration in seconds (15-60):', self.timer_max, self.timer_min, self.timer_max)

        # Prompt the user to enter the grid size
        self.grid_size, ok = QInputDialog.getInt(self, 'Input Dialog', f'Enter the grid size ({self.grid_size_min}x{self.grid_size_min} to {self.grid_size_max}x{self.grid_size_max}):', self.grid_size_max, self.grid_size_min, self.grid_size_max)

        # Initialize game variables
        self.score = 0
        self.mole_button = (0, 0)

        # Set up the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Set up the score and time labels
        self.score_label = QLabel(f'Score: {self.score}', self)
        self.time_label = QLabel(f'Time: {self.time_limit}', self)

        self.score_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.main_layout.addWidget(self.score_label)
        self.main_layout.addWidget(self.time_label)

        # Set up the grid layout
        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)

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

        # Set up the game timer to update the remaining time every second
        self.remaining_time = self.time_limit
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_time)
        self.game_timer.start(1000)

        # Set up the timer to move the mole every 2 seconds
        self.mole_timer = QTimer(self)
        self.mole_timer.timeout.connect(self.place_mole)
        self.mole_timer.start(self.mole_move_interval)

    def place_mole(self):
        row, col = self.mole_button
        self.buttons[row][col].setText(' ')

        new_row, new_col = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
        self.mole_button = (new_row, new_col)
        self.buttons[new_row][new_col].setText('mole')

    def mole_clicked(self, row, col):
        if (row, col) == self.mole_button:
            self.score += 1
            self.score_label.setText(f'Score: {self.score}')
            self.place_mole()

    def update_time(self):
        self.remaining_time -= 1
        self.time_label.setText(f'Time: {self.remaining_time}')
        if self.remaining_time <= 0:
            self.end_game()

    def end_game(self):
        self.game_timer.stop()
        self.mole_timer.stop()
        QMessageBox.information(self, 'Game Over', f'Game Over! Your score is {self.score}')
        with open('score.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WhackAMoleGame()
    window.show()
    sys.exit(app.exec_())
