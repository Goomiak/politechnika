from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox, QLineEdit, QListWidget,
    QInputDialog, QFileDialog, QListWidgetItem, QRadioButton, QGroupBox, QButtonGroup
)

from PySide6.QtGui import QBrush, QColor, QFont, QPixmap, Qt
import json
import random
import os
import datetime




class NameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Podaj swoje dane")
        self.resize(400, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5; /* Jasne tło */
                border: 2px solid #333333; /* Ciemna ramka */
            }
            QLabel {
                color: black; /* Czarny tekst */
                font-size: 16px;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 2px solid #333333;
                padding: 5px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #444444; /* Ciemniejsze przyciski */
                color: white; /* Biały tekst */
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border-radius: 5px;
                border: 2px solid #222222;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)


        self.layout = QVBoxLayout()

        self.label = QLabel("Wpisz swoje imię i nazwisko:")
        self.layout.addWidget(self.label)

        self.name_input = QLineEdit()
        self.layout.addWidget(self.name_input)

        self.start_button = QPushButton("Rozpocznij test")
        self.start_button.clicked.connect(self.accept)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def validate_and_accept(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Błąd", "Musisz podać imię i nazwisko!")
        else:
            self.accept()  # Zamknięcie okna dialogowego

    def get_name(self):
        return self.name_input.text().strip()

class TestDialog(QDialog):
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test wiedzy")
        self.resize(900, 600)
        self.center_window()

        self.setStyleSheet("""
                            QDialog {
                                background-color: #f5f5f5; /* Jasne tło */
                                border: 2px solid #333333; /* Ciemna ramka */
                            }
                            QLabel {
                                color: black; /* Czarny tekst */
                            }
                            QGroupBox {
                                border: 2px solid #333333; /* Ciemna ramka */
                                background-color: white; /* Białe tło grup */
                                font-weight: bold;
                            }
                            QRadioButton {
                                color: black; /* Czarny tekst dla opcji */
                                background-color: white;
                            }
                            QPushButton {
                                background-color: #444444; /* Ciemniejsze przyciski */
                                color: white; /* Biały tekst */
                                border-radius: 5px;
                                padding: 5px;
                            }
                            QPushButton:hover {
                                background-color: #555555;
                            }
                            QRadioButton {
                                color: black; /* Czarny tekst */
                                background-color: white; /* Białe tło */
                                spacing: 5px; /* Dystans między tekstem a kółkiem */
                            }

                            QRadioButton::indicator {
                                width: 18px;
                                height: 18px;
                                border-radius: 9px; /* Upewnia się, że kółko jest okrągłe */
                                border: 2px solid #333333; /* Ciemna ramka */
                                background-color: white; /* Tło dla niezaznaczonego */
                            }

                            QRadioButton::indicator:checked {
                                background-color: #333333; /* Ciemny kolor po zaznaczeniu */
                                border: 2px solid black; /* Ciemniejsza ramka po zaznaczeniu */
                            }
                        """)

        with open("config/test.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)["questions"]

        self.questions = random.sample(all_questions, min(10, len(all_questions)))
        self.current_question = 0
        self.score = 0
        self.name = name  # Przechowuje imię użytkownika

        self.layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.question_label = QLabel()
        self.question_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.question_label.setWordWrap(True)  
        #self.question_label.setAlignment(Qt.AlignCenter) 
        self.layout.addWidget(self.question_label)



        # Opcje odpowiedzi
        self.option_group = QGroupBox("Wybierz odpowiedź:")
        self.option_layout = QVBoxLayout()
        self.option_group.setLayout(self.option_layout)
        self.layout.addWidget(self.option_group)

        self.radio_buttons = []
        self.button_group = QButtonGroup()
        for i in range(4):
            radio = QRadioButton()
            self.radio_buttons.append(radio)
            self.button_group.addButton(radio, i)
            self.option_layout.addWidget(radio)

        # Przycisk Dalej
        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.next_question)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)
        self.show_question()

    def next_question(self):
        selected_button = self.button_group.checkedId()
        if selected_button == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz odpowiedź przed przejściem dalej!")
            return

        selected_text = self.radio_buttons[selected_button].text()
        if selected_text == self.correct_answer:
            self.score += 1

        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.finish_test()

    def show_question(self):
        question = self.questions[self.current_question]
        self.question_label.setText(question["question"])

        # Obsługa obrazu
        image_path = question.get("image", "")
        if image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.image_label.setPixmap(pixmap)  # Ustawienie obrazu bez zmiany rozmiaru
                self.image_label.show()
        else:
                self.image_label.hide()

        # Odznaczanie wszystkich opcji
        self.button_group.setExclusive(False)  # Tymczasowo wyłącz ekskluzywność, aby móc odznaczyć
        for radio_button in self.radio_buttons:
            radio_button.setChecked(False)
        self.button_group.setExclusive(True)  # Włącz ponownie, aby działała zasada pojedynczego wyboru

        # Pobranie i przetasowanie odpowiedzi
        options = list(question["options"].values())  # Pobieramy tylko wartości (bez A, B, C, D)
        random.shuffle(options)  # Mieszamy odpowiedzi

        # Aktualizacja treści opcji
        for i in range(len(self.radio_buttons)):
            if i < len(options):
                self.radio_buttons[i].setText(options[i])
                self.radio_buttons[i].setEnabled(True)
            else:
                self.radio_buttons[i].setText("")
                self.radio_buttons[i].setEnabled(False)

        # Zapamiętanie poprawnej odpowiedzi po przetasowaniu
        self.correct_answer = question["options"][question["answer"]]

    def finish_test(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - {self.name}: {self.score}/10\n")

        QMessageBox.information(self, "Wynik", f"Twój wynik to: {self.score}/10")
        self.accept()

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2 - 50
        self.move(x, y)


class AdminPanel(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Panel administracyjny testu")
        self.resize(900, 500)
        self.center_window()

        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border: 2px solid #333333;
            }
            QLabel {
                color: black;
                font-size: 16px;
            }
            QLineEdit, QListWidget {
                background-color: white;
                color: black;
                border: 2px solid #333333;
                padding: 5px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 4px;
                border-radius: 5px;
                border: 2px solid #222222;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)

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
        with open("config/test.json", "r", encoding="utf-8") as f:
            self.questions = json.load(f)["questions"]

        self.question_list.clear()
        for question in self.questions:
            item = QListWidgetItem(question["question"])
            self.question_list.addItem(item)

    def highlight_selected_item(self):
     
   
        """Podświetlenie tylko wybranego pytania przez pogrubienie czcionki"""
        for i in range(self.question_list.count()):
            item = self.question_list.item(i)
            if item is not None:
                font = item.font()  # Pobieramy aktualną czcionkę
                font.setBold(False)  # Resetujemy pogrubienie dla wszystkich elementów
                item.setFont(font)

        # Pobieramy zaznaczony element i ustawiamy mu pogrubienie
        selected_items = self.question_list.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            font = selected_item.font()  # Pobieramy czcionkę dla wybranego elementu
            font.setBold(True)  # Pogrubiamy tylko ten element
            selected_item.setFont(font)


    def add_question(self):
        question_text, ok = QInputDialog.getText(self, "Dodaj pytanie", "Treść pytania:")
        if ok and question_text:
            options = {}
            for option in ["A", "B", "C", "D"]:
                answer, ok = QInputDialog.getText(self, "Dodaj odpowiedź", f"Odpowiedź {option}:")
                if not ok or not answer:
                    return
                options[option] = answer

            correct_answer, ok = QInputDialog.getItem(self, "Poprawna odpowiedź", "Wybierz poprawną odpowiedź:", ["A", "B", "C", "D"], 0, False)
            if not ok:
                return

            image_path, _ = QFileDialog.getOpenFileName(self, "Wybierz obraz", "", "Images (*.png *.jpg *.jpeg)")

            new_question = {
                "question": question_text,
                "options": options,
                "answer": correct_answer,
                "image": image_path
            }

            self.questions.append(new_question)
            self.save_questions()
            self.load_questions()

    def edit_question(self):
        selected_index = self.question_list.currentRow()
        if selected_index == -1:
            QMessageBox.warning(self, "Błąd", "Wybierz pytanie do edycji!")
            return

        question = self.questions[selected_index]

        # Edytowanie treści pytania - poprawne wywołanie bez self i bez text=
        new_text, ok = self.get_wider_text_input("Edytuj pytanie", "Treść pytania:", question.get("question", ""))
        if ok and new_text:
            question["question"] = new_text

        # Upewniamy się, że pytanie ma sekcję 'options'
        if "options" not in question or not isinstance(question["options"], dict):
            question["options"] = {"A": "", "B": "", "C": "", "D": ""}

        # Konwersja kluczy 'a', 'b', 'c', 'd' na 'A', 'B', 'C', 'D'
        corrected_options = {key.upper(): value for key, value in question["options"].items()}
        question["options"] = corrected_options

        # Sprawdzamy, czy każda opcja istnieje – jeśli nie, to uzupełniamy pustą wartością
        for option in ["A", "B", "C", "D"]:
            if option not in question["options"]:
                question["options"][option] = ""

        # Edycja odpowiedzi
        for option in ["A", "B", "C", "D"]:
            new_option, ok = QInputDialog.getText(
                self, 
                "Edytuj odpowiedź", 
                f"Odpowiedź {option}:",
                QLineEdit.Normal,  # Poprawne przekazanie trybu pola edycyjnego
                question["options"][option]  # Domyślna wartość tekstowa
            )

            if ok and new_option:
                question["options"][option] = new_option

        # Konwersja poprawnej odpowiedzi na wielką literę
        current_answer = question.get("answer", "A").upper()
        
        new_correct_answer, ok = QInputDialog.getItem(
            self, "Edytuj poprawną odpowiedź",
            "Wybierz poprawną odpowiedź:",
            ["A", "B", "C", "D"],
            ["A", "B", "C", "D"].index(current_answer) if current_answer in ["A", "B", "C", "D"] else 0,
            False
        )
        if ok:
            question["answer"] = new_correct_answer.upper()

        # Edycja ścieżki do obrazka (zapisujemy tylko względną ścieżkę!)
        new_image_path, _ = QFileDialog.getOpenFileName(self, "Wybierz nowy obraz", "", "Images (*.png *.jpg *.jpeg)")
        if new_image_path:
            relative_path = os.path.relpath(new_image_path, os.getcwd()).replace("\\", "/")
            if relative_path.startswith("img/"):
                question["image"] = relative_path
            else:
                QMessageBox.warning(self, "Błąd", "Obraz musi znajdować się w katalogu 'img/'.")

        # Zapisujemy zmiany
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
        with open("config/test.json", "w", encoding="utf-8") as f:
            json.dump({"questions": self.questions}, f, indent=4, ensure_ascii=False)

    def get_wider_text_input(self, title, label, default_text=""):
        """Tworzy szersze pole dialogowe do wpisywania tekstu"""
        dialog = QInputDialog(self)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setTextValue(default_text)  # Poprawione przypisanie wartości początkowej
        dialog.setMinimumWidth(500)  # Szerokie okno
        ok = dialog.exec()
        return dialog.textValue(), ok
    
    