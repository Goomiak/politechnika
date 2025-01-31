from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize
from modules.module_dialog import ModuleDialog
from modules.test import TestDialog
import json

class MenuWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Ustawienie jasnego tła
        self.setStyleSheet("background-color: white; color: black; border:none;")
        self.resize(900, 500)
        self.center_window()
        
        layout = QVBoxLayout()
        
        # Logo uczelni
        logo = QLabel()
        pixmap = QPixmap("img/wtie.png")
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
        layout.addLayout(module_layout)

        # Test wiedzy
        self.test_button = QPushButton("Test wiedzy")
        self.test_button.setEnabled(False)
        self.test_button.clicked.connect(self.start_test)
        layout.addWidget(self.test_button)

        # Przycisk zamknij
        close_button = QPushButton("Zamknij")
        close_button.clicked.connect(self.close_app)
        layout.addWidget(close_button)

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
            self.summary_button.setEnabled(True)

    def start_test(self):
        dialog = TestDialog(self)
        dialog.exec()
    
    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
    
    def close_app(self):
        self.parent().close()
