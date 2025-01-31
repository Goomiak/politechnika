from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
import json

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

        self.option_buttons = []
        for _ in range(4):
            button = QPushButton()
            button.clicked.connect(self.check_answer)
            self.option_buttons.append(button)
            self.layout.addWidget(button)

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
        selected = sender.text()[0]
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