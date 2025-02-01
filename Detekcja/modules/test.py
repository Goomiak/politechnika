from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit, QListWidget,
    QInputDialog, QFileDialog, QListWidgetItem
)
from PySide6.QtGui import QBrush, QColor, QFont
import json
import random
import os

class TestDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test wiedzy")
        self.resize(800, 600)
        self.center_window()

        with open("test.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)["questions"]

        self.questions = random.sample(all_questions, min(10, len(all_questions)))
        self.current_question = 0
        self.score = 0

        self.layout = QVBoxLayout()

        self.name_label = QLabel("Imię i nazwisko:")
        self.layout.addWidget(self.name_label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.start_button = QPushButton("Rozpocznij test")
        self.start_button.clicked.connect(self.start_test)
        self.layout.addWidget(self.start_button)

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
        self.next_button.setEnabled(False)

        self.setLayout(self.layout)

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2 - 50
        self.move(x, y)

    def start_test(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Błąd", "Podaj imię i nazwisko przed rozpoczęciem testu!")
            return

        self.name_input.setDisabled(True)
        self.start_button.setDisabled(True)
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

        self.next_button.setEnabled(True)

    def next_question(self):
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
            self.next_button.setEnabled(False)
        else:
            self.finish_test()

    def finish_test(self):
        name = self.name_input.text()
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(f"{name}: {self.score}/10\n")

        QMessageBox.information(self, "Wynik", f"Twój wynik to: {self.score}/10")
        self.accept()


class AdminPanel(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Panel administracyjny testu")
        self.resize(900, 500)
        self.center_window()

        self.layout = QVBoxLayout()

        self.question_list = QListWidget()
        self.question_list.itemSelectionChanged.connect(self.highlight_selected_item)
        self.layout.addWidget(self.question_list)

        self.add_button = QPushButton("Dodaj pytanie")
        self.add_button.clicked.connect(self.add_question)
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edytuj pytanie")
        self.edit_button.clicked.connect(self.edit_question)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Usuń pytanie")
        self.delete_button.clicked.connect(self.delete_question)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)
        self.load_questions()

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2 - 50
        self.move(x, y)

    def load_questions(self):
        with open("test.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)["questions"]

        self.question_list.clear()
        for question in self.questions:
            item = QListWidgetItem(question["question"])
            self.question_list.addItem(item)

    def highlight_selected_item(self):
        for i in range(self.question_list.count()):
            item = self.question_list.item(i)
            if item is not None:
                font = item.font()
                font.setBold(False)
                item.setFont(font)

        selected_items = self.question_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            font = selected_item.font()
            font.setBold(True)
            selected_item.setFont(font)

    def edit_question(self):
        selected_index = self.question_list.currentRow()
        if selected_index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz pytanie do edycji!")
            return

        question = self.questions[selected_index]

        from PySide6.QtWidgets import QLineEdit  # Dodajemy import dla poprawnego działania

        new_text, ok = QInputDialog.getText(
            self, "Edytuj pytanie", "Treść pytania:", QLineEdit.Normal, question.get("question", "")
        )
        if ok and new_text:
            question["question"] = new_text

        for option in ["A", "B", "C", "D"]:
            new_option, ok = QInputDialog.getText(
                self, "Edytuj odpowiedź", f"Odpowiedź {option}:", QLineEdit.Normal, question["options"][option]
            )
            if ok and new_option:
                question["options"][option] = new_option

        self.save_questions()
        self.load_questions()

    def delete_question(self):
        selected_index = self.question_list.currentRow()
        if selected_index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz pytanie do usunięcia!")
            return

        del self.questions[selected_index]
        self.save_questions()
        self.load_questions()

    def save_questions(self):
        with open("test.json", "w", encoding="utf-8") as f:
            json.dump({"questions": self.questions}, f, indent=4, ensure_ascii=False)
