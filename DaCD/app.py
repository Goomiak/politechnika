import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, QStackedWidget,
    QWidget, QMessageBox, QFileDialog, QGridLayout
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Zasady Detekcji Bezpośredniej i Koherentnej")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout()
        
        # Logo uczelni
        logo = QLabel()
        pixmap = QPixmap("wtie.png")
        logo.setPixmap(pixmap.scaledToWidth(200, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # Tytuł aplikacji
        title = QLabel("Zasady detekcji bezpośredniej i koherentnej")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Instrukcja
        instruction = QLabel("Wybierz zagadnienie, którego chcesz się uczyć")
        instruction.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction)

        # Moduły z ikonami
        module_layout = QHBoxLayout()
        self.direct_detection_button = QPushButton()
        self.direct_detection_button.setIcon(QIcon("1-png.png"))
        self.direct_detection_button.setIconSize(QSize(100, 100))
        self.direct_detection_button.clicked.connect(lambda: self.open_module("direct_detection"))
        
        self.coherent_detection_button = QPushButton()
        self.coherent_detection_button.setIcon(QIcon("2-png.png"))
        self.coherent_detection_button.setIconSize(QSize(100, 100))
        self.coherent_detection_button.clicked.connect(lambda: self.open_module("coherent_detection"))
        
        self.summary_button = QPushButton()
        self.summary_button.setIcon(QIcon("3-png.png"))
        self.summary_button.setIconSize(QSize(100, 100))
        self.summary_button.setEnabled(False)  # Disabled until other modules are completed
        self.summary_button.clicked.connect(lambda: self.open_module("summary"))

        module_layout.addWidget(self.direct_detection_button)
        module_layout.addWidget(self.coherent_detection_button)
        module_layout.addWidget(self.summary_button)
        layout.addLayout(module_layout)

        # Test wiedzy
        self.test_button = QPushButton("Test wiedzy")
        self.test_button.setEnabled(False)
        self.test_button.clicked.connect(self.start_test)
        layout.addWidget(self.test_button)

        # Przycisk zamknij
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.main_widget.setLayout(layout)

        # Load data from config
        with open("json/config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.completed_modules = set()

    def open_module(self, module_name):
        dialog = ModuleDialog(self.config["slides"].get(module_name, []), self)
        dialog.exec()
        self.completed_modules.add(module_name)

        if len(self.completed_modules) == 3:  # All modules viewed
            self.test_button.setEnabled(True)
            self.summary_button.setEnabled(True)

    def start_test(self):
        dialog = TestDialog(self)
        dialog.exec()


class ModuleDialog(QDialog):
    def __init__(self, slides, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Moduł")
        self.setGeometry(100, 100, 800, 600)

        self.slides = slides
        self.current_slide = 0

        self.layout = QVBoxLayout()

        self.content = QLabel()
        self.content.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.content)

        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.next_slide)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.show_slide()

    def show_slide(self):
        slide = self.slides[self.current_slide]
        content = ""
        for element in slide["elements"]:
            if element["type"] == "text":
                content += element["content"] + "\n\n"
        self.content.setText(content)

    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.show_slide()
        else:
            self.accept()


class TestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test wiedzy")
        self.setGeometry(100, 100, 800, 600)

        with open("test.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)["questions"]

        self.current_question = 0
        self.score = 0

        self.layout = QVBoxLayout()

        self.question_label = QLabel()
        self.layout.addWidget(self.question_label)

        self.options_layout = QVBoxLayout()
        self.option_buttons = []
        for _ in range(4):
            button = QPushButton()
            button.clicked.connect(self.check_answer)
            self.option_buttons.append(button)
            self.options_layout.addWidget(button)

        self.layout.addLayout(self.options_layout)

        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.show_question()

    def show_question(self):
        question = self.questions[self.current_question]
        self.question_label.setText(question["question"])
        for i, (key, value) in enumerate(question["options"].items()):
            self.option_buttons[i].setText(f"{key}: {value}")
            self.option_buttons[i].setEnabled(True)

    def check_answer(self):
        sender = self.sender()
        selected = sender.text()[0]  # Get the letter (a, b, c, d)
        correct = self.questions[self.current_question]["answer"]
        if selected == correct:
            self.score += 1
        for button in self.option_buttons:
            button.setEnabled(False)

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.accept()
            QMessageBox.information(self, "Wynik", f"Twój wynik to: {self.score}/{len(self.questions)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
