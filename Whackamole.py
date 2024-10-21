import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

class WhackAMoleGame(QWidget):  # Define the WhackAMoleGame class
    def __init__(self):
        super().__init__()
        
        # Set constants
        self.timer_max = 60  # Maximum game time
        self.timer_min = 15  # Minimum game time
        self.grid_size_min = 3  # Minimum grid size
        self.grid_size_max = 5  # Maximum grid size
        self.mole_move_interval = 2000  # Mole moves every 2 seconds (2000 ms)
        
        # Initialize the game UI
        self.init_ui()

    def init_ui(self):
        """Sets up the game window and UI components."""
        self.setWindowTitle('Whack-A-Mole')

        # Prompt the user to enter the game duration
        self.time_limit, ok = QInputDialog.getInt(
            self, 'Input Dialog', 'Enter the game duration in seconds (15-60):', 
            self.timer_max, self.timer_min, self.timer_max
        )

        # Prompt the user to enter the grid size
        self.grid_size, ok = QInputDialog.getInt(
            self, 'Input Dialog', f'Enter the grid size ({self.grid_size_min}x{self.grid_size_min} to {self.grid_size_max}x{self.grid_size_max}):', 
            self.grid_size_max, self.grid_size_min, self.grid_size_max
        )

        # Initialize game variables
        self.score = 0
        self.mole_button = (0, 0)

        # Set up the main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Set up the score and time labels at the top
        self.score_label = QLabel(f'Score: {self.score}', self)
        self.time_label = QLabel(f'Time: {self.time_limit}', self)

        self.score_label.setAlignment(Qt.AlignCenter)
        self.time_label.setAlignment(Qt.AlignCenter)
        
        # Add the score and time labels to the main layout
        self.main_layout.addWidget(self.score_label)
        self.main_layout.addWidget(self.time_label)

        # Set up the grid layout
        self.grid = QGridLayout()
        self.main_layout.addLayout(self.grid)

        # Create buttons for the grid
        self.buttons = [[QPushButton(' ') for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Add each button to the grid and make them clickable
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                 button = self.buttons[row][col]
                 button.setFixedSize(100, 100)  # Button size
                 button.clicked.connect(lambda ch, row=row, col=col: self.mole_clicked(row, col))  # Makes button click work with the mole on it
                 self.grid.addWidget(button, row, col)
        
        # Place the initial mole
        self.place_mole()

        # Set up the game timer to update the remaining time every second
        self.remaining_time = self.time_limit
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_time)  # Connects timer to update_time function
        self.game_timer.start(1000)  # Updates time every second (1000 ms)

        # Set up the timer to move the mole every 2 seconds
        self.mole_timer = QTimer(self)
        self.mole_timer.timeout.connect(self.place_mole)  # Connects timer to place_mole function
        self.mole_timer.start(self.mole_move_interval)  # Makes the mole move every 2 seconds

    # Function to place a mole at a random button
    def place_mole(self):
        # Clear the old mole's position
        row, col = self.mole_button
        self.buttons[row][col].setText(' ')  # Resets text on the old mole button
        # Randomly selects a new position for the mole
        new_row, new_col = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
        self.mole_button = (new_row, new_col)
        self.buttons[new_row][new_col].setText('mole')  # Set the text of the new mole button

    # Function for when the button is clicked
    def mole_clicked(self, row, col):
        # Checks if the clicked button is the mole's position
        if (row, col) == self.mole_button:
            self.score += 1  # Increments the score
            self.score_label.setText(f'Score: {self.score}')  # Updates the score label text
            self.place_mole()  # Moves the mole again

    # Function to update the remaining time
    def update_time(self):
        self.remaining_time -= 1  # Decrements remaining time by 1 second
        self.time_label.setText(f'Time: {self.remaining_time}')  # Updates the time label text
        if self.remaining_time <= 0:
            self.end_game()  # Ends the game when time runs out

    # Function to end the game when the timer reaches 0
    def end_game(self):
        self.game_timer.stop()  # Stops game timer
        self.mole_timer.stop()  # Stops the mole's 2-second move timer
        QMessageBox.information(self, 'Game Over', f'Game Over! Your score is {self.score}')  # Displays the final score
        # Saves the score to a file
        with open('score.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')
        self.close()  # Closes the game window

# Function that runs the game
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Creates the app
    window = WhackAMoleGame()  # Creates the game window
    window.show()  # Shows the game window
    sys.exit(app.exec_())  # Allows the game to end
