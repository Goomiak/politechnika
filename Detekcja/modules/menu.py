from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QLineEdit, QDialog, QMessageBox, QInputDialog)
from PySide6.QtGui import QPixmap, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize
from modules.module_dialog import ModuleDialog
from modules.test import TestDialog, AdminPanel, NameDialog
import json

class MenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Ustawienie jasnego tła
        self.setStyleSheet("background-color: white; color: black; border:none;")
        
        self.resize(900, 500)
        self.center_window()
        
        layout = QVBoxLayout()
        
        # Scroll area for content
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)
        
        # Skrót klawiszowy do panelu admina
        from PySide6.QtGui import QShortcut
        self.admin_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        self.admin_shortcut.activated.connect(self.admin_login)
        
        # Logo uczelni
        logo = QLabel()
        pixmap = QPixmap("img/wtie.png")
        logo.setPixmap(pixmap.scaledToWidth(400, Qt.SmoothTransformation))
        logo.setAlignment(Qt.AlignCenter)
        self.scroll_layout.addWidget(logo)

        # Tytuł aplikacji
        title = QLabel("Aplikacja: Zasady detekcji bezpośredniej i koherentnej")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; ")
        self.scroll_layout.addWidget(title)

        # Instrukcja
        instruction = QLabel("Wybierz zagadnienie, którego chcesz się uczyć:")
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setStyleSheet("font-size: 16px; ")
        self.scroll_layout.addWidget(instruction)

        # Moduły z ikonami zamiast przycisków
        module_layout = QHBoxLayout()
        self.direct_detection_button = QPushButton()
        self.direct_detection_button.setIcon(QIcon("img/1-png.png"))
        self.direct_detection_button.setIconSize(QSize(200, 200))
        self.direct_detection_button.setStyleSheet("border: none;")
        self.direct_detection_button.clicked.connect(lambda: self.open_module("direct_detection"))

        self.coherent_detection_button = QPushButton()
        self.coherent_detection_button.setIcon(QIcon("img/2-png.png"))
        self.coherent_detection_button.setIconSize(QSize(200, 200))
        self.coherent_detection_button.setStyleSheet("border: none;")
        self.coherent_detection_button.clicked.connect(lambda: self.open_module("coherent_detection"))

        self.summary_button = QPushButton()
        self.summary_button.setIcon(QIcon("img/3-png.png"))
        self.summary_button.setIconSize(QSize(200, 200))
        self.summary_button.setStyleSheet("border: none;")
        #self.summary_button.setEnabled(False)  # Disabled until other modules are completed
        self.summary_button.clicked.connect(lambda: self.open_module("summary"))

        module_layout.addWidget(self.direct_detection_button)
        module_layout.addWidget(self.coherent_detection_button)
        module_layout.addWidget(self.summary_button)
        self.scroll_layout.addLayout(module_layout)

        # Instrukcja
        test_instruction = QLabel("Test wiedzy aktywuje się po obejrzeniu wszystkich modułów:")
        test_instruction.setAlignment(Qt.AlignCenter)
        test_instruction.setStyleSheet("font-size: 16px;")
        self.scroll_layout.addWidget(test_instruction)

        # Test wiedzy
        self.test_button = QPushButton("Test wiedzy")
        self.test_button.setEnabled(False)
        self.test_button.setStyleSheet("border: none; color: gray;")
        self.test_button.clicked.connect(self.start_test)

        self.scroll_layout.addWidget(self.test_button)

        # Przycisk zamknij
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.close_app)
        self.scroll_layout.addWidget(close_button)

        button_style = """
            QPushButton {
                background-color: #bbbbbb; /* Ciemniejsze tło */
                color: #888888; /* Biały tekst */
                font-size: 16px; /* Większa czcionka */
                font-weight: bold;
                padding: 4px;
                border-radius: 5px;
                border: 2px solid #888888;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """

        close_button_style = """
            QPushButton {
                background-color: #777777; /* Czerwone tło */
                color: white; /* Biały tekst */
                font-size: 16px;
                font-weight: bold;
                padding: 4px;
                border-radius: 5px;
                border: 2px solid #444444;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """

        # Ustawienie stylu dla przycisków
        self.test_button.setStyleSheet(button_style)
        close_button.setStyleSheet(close_button_style)

        self.setLayout(layout)
        
        # Load data from config
        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        self.completed_modules = set()

    def open_module(self, module_name):
        dialog = ModuleDialog(self.config["slides"].get(module_name, []), self)
        dialog.exec()
        self.completed_modules.add(module_name)

        if len(self.completed_modules) == 3:  # All modules viewed
            self.test_button.setEnabled(True)
            self.test_button.setStyleSheet("""
                QPushButton {
                    background-color: #777777; /* Ciemniejsze tło */
                    color: white; /* Biały tekst */
                    font-size: 16px;
                    font-weight: bold;
                    padding: 4px;
                    border-radius: 5px;
                    border: 2px solid #444444;
                }
                QPushButton:hover {
                    background-color: #444444;
                }
            """)
            self.summary_button.setEnabled(True)

    def start_test(self):
        name_dialog = NameDialog()
        if name_dialog.exec() == QDialog.Accepted:  # Jeśli użytkownik kliknie "Rozpocznij test"
            name = name_dialog.get_name()
            if name:  # Sprawdzamy, czy użytkownik coś wpisał
                test_dialog = TestDialog(name)
                test_dialog.exec()
            else:
                QMessageBox.warning(None, "Błąd", "Musisz podać imię i nazwisko!")
    
    def admin_login(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Wprowadź hasło administratora")
        dialog.setLabelText("Hasło:")
        dialog.setTextEchoMode(QLineEdit.Password)
        dialog.setStyleSheet("""
                QDialog {
                    background-color: #f5f5f5;
                    border: 2px solid #333333;
                }
                QLabel {
                    color: black;
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
                    background-color: #444444;
                    color: white;
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

        password, ok = dialog.getText(self, "Wprowadź hasło administratora", "Hasło:", QLineEdit.Password)

        if ok and password == "password":
            admin_panel = AdminPanel(self)
            admin_panel.setStyleSheet("""
                    QPushButton {
                        background-color: #444444;
                        color: white;
                        font-size: 12px;
                        font-weight: bold;
                        padding: 2px;
                        border-radius: 3px;
                        border: 2px solid #222222;
                    }
                    QPushButton:hover {
                        background-color: #555555;
                    }
                """)
            admin_panel.exec()
        else:
            QMessageBox.warning(self, "Błąd", "Nieprawidłowe hasło!")

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def close_app(self):
        self.parent().close()
