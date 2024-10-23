import sys
from PySide6.QtWidgets import QApplication
from gui.gui import KronosApp  # Import the GUI from the gui folder

class MainApp(KronosApp):
    def __init__(self):
        super().__init__()  # Initialize the GUI layout from gui.py
        self.connect_events()

    def connect_events(self):
        # Connect buttons to their respective functions (inherited from KronosApp)
        self.run_crawler_button.clicked.connect(self.run_crawler)
        self.hidden_page_button.clicked.connect(self.run_hidden_page_finder)
        self.exit_button.clicked.connect(self.exit_application)

    # Define exit_application method to use confirm_exit method
    def exit_application(self):
        if self.confirm_exit():
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
