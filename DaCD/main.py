from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import math
from menu import MenuWindow

def calculate_screen_diagonal(width, height):
    """Oblicza przekątną ekranu w calach."""
    diagonal = math.sqrt(width ** 2 + height ** 2)
    return diagonal / 96  # Zakładamy 96 DPI (pikseli na cal)

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Start")

        # Oblicz przekątną ekranu
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        diagonal_inches = calculate_screen_diagonal(screen_width, screen_height)

        if diagonal_inches <= 19:  # Dla ekranów 19 cali i mniejszych pełny ekran
            self.showFullScreen()
        else:  # Dla większych ekranów ustaw rozmiar okna na środku
            window_width = 1300
            window_height = 800
            self.setGeometry(
                (screen_width - window_width) // 2,
                (screen_height - window_height) // 2,
                window_width,
                window_height
            )

        # Główny widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QVBoxLayout()

        # Nagłówek z obrazem
        pixmap = QPixmap('img/wtie.png').scaled(720, 270, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Tytuł
        title_label = QLabel("Aplikacja dydaktyczna: Zasady detekcji bezpośredniej i koherentnej")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(title_label)

        # Opis
        info_label = QLabel(
            "Aplikacja została wykonana w ramach projektu z przedmiotu Cyfrowe Modulacje i Kodowanie na studiach "
            "magisterskich Kierunek: Elektronika i Telekomunikacja"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(info_label)

        # Autorzy
        authors_label = QLabel("Autorzy:\nKamil Jankowski\nFilip Grządziel")
        authors_label.setAlignment(Qt.AlignCenter)
        authors_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(authors_label)

        # Przyciski
        button_layout = QVBoxLayout()

        start_button = QPushButton("Start")
        start_button.setStyleSheet("font-size: 16px;")
        start_button.clicked.connect(self.start_app)
        button_layout.addWidget(start_button)

        close_button = QPushButton("Zamknij")
        close_button.setStyleSheet("font-size: 16px;")
        close_button.clicked.connect(self.close)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)

        main_widget.setLayout(layout)

    def start_app(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = StartWindow()
    window.show()

    sys.exit(app.exec())
