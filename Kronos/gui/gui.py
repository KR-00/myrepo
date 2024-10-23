# gui/gui.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QHBoxLayout, QInputDialog, QMessageBox
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt
from gui.worker_threads import CrawlerWorker, HiddenPageWorker  # Import the threading workers

class KronosApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Kronos")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c2c2c; color: #CD7F32;")  # Bronze text color
        self.setWindowIcon(QIcon("assets/kronos_logo.png"))  # Kronos logo

        layout = QVBoxLayout()

        # Add Kronos logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap("assets/kronos_logo.png")
        resized_logo_pixmap = logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio)
        logo_label.setPixmap(resized_logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Results text area
        self.results_box = QTextEdit(self)
        self.results_box.setReadOnly(True)
        self.results_box.setStyleSheet("background-color: #1e1e1e; color: #CD7F32; padding: 10px; font-size: 12px;")
        layout.addWidget(self.results_box)

        # Buttons
        button_layout = QHBoxLayout()
        self.run_crawler_button = QPushButton("Run Crawler")
        self.run_crawler_button.setStyleSheet("background-color: #1e1e1e; padding: 10px; font-size: 14px; color: #CD7F32;")
        button_layout.addWidget(self.run_crawler_button)

        self.hidden_page_button = QPushButton("Run Hidden Page Finder")
        self.hidden_page_button.setStyleSheet("background-color: #1e1e1e; padding: 10px; font-size: 14px; color: #CD7F32;")
        button_layout.addWidget(self.hidden_page_button)

        self.exit_button = QPushButton("Exit")
        self.exit_button.setStyleSheet("background-color: #1e1e1e; padding: 10px; font-size: 14px; color: #CD7F32;")
        button_layout.addWidget(self.exit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def run_crawler(self):
        input_value, ok = QInputDialog.getText(self, "Input URL or Port", "Please enter a full URL (e.g., http://localhost:42000) or just a port (e.g., 42000):")
        if ok and input_value:
            self.results_box.clear()
            self.results_box.append("Crawling started...")
            self.crawler_thread = CrawlerWorker(input_value)  # Pass the input (URL or port) to the worker
            self.crawler_thread.crawler_finished.connect(self.show_results)
            self.crawler_thread.start()

    def run_hidden_page_finder(self):
        base_url, ok = QInputDialog.getText(self, "Input Base URL", "Please enter the base URL (e.g., http://localhost:42000):")
        if ok:
            wordlist_file = "modules/route_mapper/common_paths.txt"
            self.results_box.clear()
            self.results_box.append("Hidden page discovery started...")
            self.hidden_page_thread = HiddenPageWorker(base_url, wordlist_file)
            self.hidden_page_thread.hidden_pages_found.connect(self.show_hidden_page_results)
            self.hidden_page_thread.start()

    def show_results(self, pages):
        self.results_box.clear()
        if pages:
            self.results_box.append("Crawler results:")
            for page in pages:
                self.results_box.append(str(page))
        else:
            self.results_box.append("No pages found.")

    def show_hidden_page_results(self, hidden_pages, auth_required_pages):
        self.results_box.clear()
        if hidden_pages:
            self.results_box.append("Hidden pages found:")
            for page in hidden_pages:
                self.results_box.append(str(page))
        else:
            self.results_box.append("No hidden pages found.")

        if auth_required_pages:
            self.results_box.append("\nPages requiring authorization:")
            for page in auth_required_pages:
                self.results_box.append(str(page))
        else:
            self.results_box.append("No pages require authorization.")

    def confirm_exit(self):
        exit_message = QMessageBox(self)
        exit_message.setWindowTitle("Exit Confirmation")
        exit_message.setText("Do you really want to exit?")
        exit_message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exit_message.setDefaultButton(QMessageBox.No)
        exit_message.setIcon(QMessageBox.NoIcon)
        return exit_message.exec() == QMessageBox.Yes
