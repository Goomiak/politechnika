from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import math
from slides import show_window_sequence, load_config
from test import start_test_window

def calculate_screen_diagonal(width, height):
    """Oblicza przekątną ekranu w calach."""
    diagonal = math.sqrt(width ** 2 + height ** 2)
    return diagonal / 96  # Zakładamy 96 DPI (pikseli na cal)

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Menu")

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

        # Wczytaj konfigurację
        try:
            self.config = load_config("json/config.json")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się wczytać konfiguracji: {e}")
            self.config = {"slides": {}}

        # Główny widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Tytuł
        title_label = QLabel("Kliknij ikonę i wybierz moduł, który chcesz trenować.")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(title_label)

        # Opis
        info_label = QLabel(
            "Moduły zawierają opracowanie teoretyczne, modele matematyczne oraz interaktywne symulacje."
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(info_label)

        # Obrazy z przyciskami
        button_layout = QHBoxLayout()

        btn_direct = self.create_image_button("img/1-png.png", "Detekcja bezpośrednia", self.on_direct_detection)
        button_layout.addWidget(btn_direct)

        btn_coherent = self.create_image_button("img/2-png.png", "Detekcja koherentna", self.on_coherent_detection)
        button_layout.addWidget(btn_coherent)

        btn_summary = self.create_image_button("img/3-png.png", "Podsumowanie", self.on_summary)
        button_layout.addWidget(btn_summary)

        layout.addLayout(button_layout)

        # Przycisk testu
        self.test_button = QPushButton("Test wiedzy")
        self.test_button.setStyleSheet("font-size: 16px;")
        self.test_button.setEnabled(False)
        self.test_button.clicked.connect(self.start_test)
        layout.addWidget(self.test_button, alignment=Qt.AlignCenter)

        # Przycisk zamknięcia
        close_button = QPushButton("Zamknij")
        close_button.setStyleSheet("font-size: 16px;")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)

        main_widget.setLayout(layout)

        # Stan obejrzanych slajdów
        self.viewed_slides = {"direct_detection": False, "coherent_detection": False, "summary": False}

    def create_image_button(self, image_path, tooltip, callback):
        pixmap = QPixmap(image_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        button = QPushButton()
        button.setIcon(pixmap)
        button.setIconSize(pixmap.size())
        button.setToolTip(tooltip)
        button.clicked.connect(callback)
        return button

    def on_direct_detection(self):
        slides = self.config["slides"].get("direct_detection", [])
        if slides:
            show_window_sequence(slides, "Direct Detection")
            self.viewed_slides["direct_detection"] = True
        else:
            QMessageBox.warning(self, "Błąd", "Brak danych dla detekcji bezpośredniej.")
        self.update_test_button_state()

    def on_coherent_detection(self):
        slides = self.config["slides"].get("coherent_detection", [])
        if slides:
            show_window_sequence(slides, "Coherent Detection")
            self.viewed_slides["coherent_detection"] = True
        else:
            QMessageBox.warning(self, "Błąd", "Brak danych dla detekcji koherentnej.")
        self.update_test_button_state()

    def on_summary(self):
        slides = self.config["slides"].get("summary", [])
        if slides:
            show_window_sequence(slides, "Summary")
            self.viewed_slides["summary"] = True
        else:
            QMessageBox.warning(self, "Błąd", "Brak danych dla podsumowania.")
        self.update_test_button_state()

    def update_test_button_state(self):
        if all(self.viewed_slides.values()):
            self.test_button.setEnabled(True)

    def start_test(self):
        try:
            start_test_window()
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się uruchomić testu: {e}")

def create_menu_window():
    menu_window = MenuWindow()
    menu_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    create_menu_window()
    sys.exit(app.exec())
