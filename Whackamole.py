import sys
#imports all functions from that library
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QInputDialog, QMessageBox
from PyQt5.QtCore import QTimer

#This class is to define the entire process of the game
class ButtonGrid(QWidget):
    #This function has all the variables in it and initializes the code
    def __init__(self):
        super().__init__()
        self.number_of_rows = 3
        self.number_of_cols = 3
        self.player = 'X'
        self.number_of_turns = 0
        self.game_ended = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Whacka-Mole')

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.buttons = [[QPushButton(' ') for _ in range(3)] for _ in range(3)]

        for row in range(self.number_of_rows):
            for col in range(self.number_of_cols):
                button = self.buttons[row][col]
                button.setFixedSize(100,100)
                button.clicked.connect(lambda ch, row=row, col=col: self.button_clicked(row, col))
                self.grid.addWidget(button, row, col)

# Makes sure it is running the Main code
if __name__ == '__main__':

     # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create a main application window (QWidget)
    window = ButtonGrid()
    window.show()
    # Execute the application's event loop
    sys.exit(app.exec_())

