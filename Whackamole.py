import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, Qt

class WhackAMoleGame(QWidget): #define the WhackAMoleGame class
    def __init__(self):
        super().__init__()
        #set constants
        self.timer_max = 60 #max game time
        self.timer_min = 15  #minimum game time
        self.grid_size_min = 3 #Minimum grid size
        self.grid_size_max = 5 #max grid size
        self.mole_move_interval = 2000  # Mole moves every 2 seconds (1000 per second)
        self.init_ui()
    #makes the game window 
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
                 button.setFixedSize(100, 100)  #button size
                 button.clicked.connect(lambda ch, row=row, col=col: self.mole_clicked(row, col)) #makes button click work with the mole on it
                 self.grid.addWidget(button, row, col)
        
        # Place the initial mole
        self.place_mole()

        # Set up the game timer to update the remaining time every second
        self.remaining_time = self.time_limit
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_time)  #makes the timer update alongside the update time finction
        self.game_timer.start(1000)  #Updates time every second (1000 ms)

        # Set up the timer to move the mole every 2 seconds
        self.mole_timer = QTimer(self)
        self.mole_timer.timeout.connect(self.place_mole)  # Connects timer to place_mole function
        self.mole_timer.start(self.mole_move_interval) #makes the mole move every 2 seconds
   
   #Function to place a mole at a random button
    def place_mole(self):
        ## Clear the old mole's position
        row, col = self.mole_button
        self.buttons[row][col].setText(' ') #Resets text on the old mole button
        # Randomly selects a new position for the mole
        new_row, new_col = random.randint(0, self.grid_size-1), random.randint(0, self.grid_size-1)
        self.mole_button = (new_row, new_col)
        self.buttons[new_row][new_col].setText('mole')   # Set the text of the new mole button

    # Function for when the button is clicked
    def mole_clicked(self, row, col):
        # Checks if the clicked button is the mole's position
        if (row, col) == self.mole_button:
            self.score += 1 #changes the score (+1+)
            self.score_label.setText(f'Score: {self.score}') #changes the score labels text
            self.place_mole() #moves the mole again

    # Function to update the remaining time
    def update_time(self):
        self.remaining_time -= 1 #change remaining time by -1 second
        self.time_label.setText(f'Time: {self.remaining_time}') # Updates the time label text
        if self.remaining_time <= 0:
            self.end_game() # End the game when time runs out

    # Function to end the game when the timer reaches 0
    def end_game(self):
        self.game_timer.stop() #stops game timer
        self.mole_timer.stop() #stops the mole 2 sec move timer
        QMessageBox.information(self, 'Game Over', f'Game Over! Your score is {self.score}') # Displays the final score
        #saves ths score to a save file
        with open('score.txt', 'a') as file:
            file.write(f'Score: {self.score}\n')
        self.close() # Closes the game window

#Function that Runs the game
if __name__ == '__main__':
    app = QApplication(sys.argv) #makes the app
    window = WhackAMoleGame() #creates the game window
    window.show() #shows the game window
    sys.exit(app.exec_()) #allows the game to end
