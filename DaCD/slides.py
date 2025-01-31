from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import sys
import math
import json

def load_config(path):
    """Ładuje konfigurację z pliku JSON."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"slides": {}}
    except json.JSONDecodeError:
        return {"slides": {}}

def calculate_screen_diagonal(width, height):
    """Oblicza przekątną ekranu."""
    return math.sqrt(width ** 2 + height ** 2) / 96  # Zakładamy 96 DPI

class SlideWindow(QMainWindow):
    def __init__(self, slides, title):
        super().__init__()
        self.slides = slides
        self.current_index = 0

        self.setWindowTitle(title)

        # Oblicz przekątną ekranu
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        diagonal_inches = calculate_screen_diagonal(screen_width, screen_height)

        if diagonal_inches <= 19:  # Ekrany <= 19 cali: pełny ekran
            self.showFullScreen()
        else:  # Większe ekrany: wyśrodkowane okno
            self.setGeometry(
                (screen_width - 1300) // 2,
                (screen_height - 800) // 2,
                1300,
                800
            )

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Kontener przewijania
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.slide_content = QWidget()
        self.slide_layout = QVBoxLayout()
        self.slide_content.setLayout(self.slide_layout)
        self.scroll_area.setWidget(self.slide_content)

        layout.addWidget(self.scroll_area)

        # Przyciski nawigacji
        nav_layout = QHBoxLayout()

        self.back_button = QPushButton("Wstecz")
        self.back_button.clicked.connect(self.previous_slide)
        nav_layout.addWidget(self.back_button)

        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.next_slide)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        main_widget.setLayout(layout)
        self.update_slide()

    def update_slide(self):
        # Czyści poprzednią zawartość
        for i in reversed(range(self.slide_layout.count())):
            widget = self.slide_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Pobiera aktualny slajd
        slide = self.slides[self.current_index]
        for element in slide.get("elements", []):
            if element["type"] == "text":
                text_label = QLabel(element["content"])
                text_label.setWordWrap(True)
                text_label.setStyleSheet("font-size: 16px;")
                self.slide_layout.addWidget(text_label)
            elif element["type"] == "image":
                image_path = element["content"]
                if image_path and QPixmap(image_path).isNull() is False:
                    pixmap = QPixmap(image_path)
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    image_label.setAlignment(Qt.AlignCenter)
                    self.slide_layout.addWidget(image_label)
                else:
                    error_label = QLabel(f"Nie można załadować obrazu: {image_path}")
                    error_label.setStyleSheet("color: red; font-size: 14px;")
                    self.slide_layout.addWidget(error_label)

        self.back_button.setEnabled(self.current_index > 0)
        self.next_button.setEnabled(self.current_index < len(self.slides) - 1)

    def next_slide(self):
        if self.current_index < len(self.slides) - 1:
            self.current_index += 1
            self.update_slide()

    def previous_slide(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_slide()

def show_window_sequence(slides, title):
    """Uruchamia pokaz slajdów."""
    app = QApplication.instance() or QApplication(sys.argv)
    window = SlideWindow(slides, title)
    window.show()
    if not app.instance():
        app.exec()

if __name__ == "__main__":
    # Przykładowe dane do testu
    example_slides = [
        {
            "elements": [
                {"type": "text", "content": "Witamy na pierwszym slajdzie!"},
                {"type": "image", "content": "img/sample.png"}
            ]
        },
        {
            "elements": [
                {"type": "text", "content": "To jest drugi slajd."}
            ]
        }
    ]

    show_window_sequence(example_slides, "Przykładowy pokaz slajdów")
