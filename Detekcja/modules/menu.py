from PySide6.QtWidgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QLineEdit, QDialog, QMessageBox, QInputDialog)
from PySide6.QtGui import QPixmap, QIcon, QKeySequence
from PySide6.QtCore import Qt, QSize
from modules.module_dialog import ModuleDialog
from modules.test import TestDialog, AdminPanel
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
        title = QLabel("Zasady detekcji bezpośredniej i koherentnej")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.scroll_layout.addWidget(title)

        # Instrukcja
        instruction = QLabel("Wybierz zagadnienie, którego chcesz się uczyć")
        instruction.setAlignment(Qt.AlignCenter)
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

        # Test wiedzy
        self.test_button = QPushButton("Test wiedzy")
        self.test_button.setEnabled(False)
        self.test_button.setStyleSheet("border: 1px solid gray; color: gray;")
        self.test_button.clicked.connect(self.start_test)

        self.scroll_layout.addWidget(self.test_button)

        # Przycisk zamknij
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.close_app)
        self.scroll_layout.addWidget(close_button)

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
            self.test_button.setStyleSheet("border: 1px solid black; color: black;")
            self.summary_button.setEnabled(True)

    def start_test(self):
        dialog = TestDialog(self)
        dialog.exec()
    
    def admin_login(self):
        password, ok = QInputDialog.getText(self, "Wprowadź hasło administratora", "Hasło:", QLineEdit.Password)
        if ok and password == "password":
            admin_panel = AdminPanel(self)
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
