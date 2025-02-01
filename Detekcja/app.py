import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow
from modules.menu import MenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zasady Detekcji Bezpośredniej i Koherentnej")
        self.resize(800, 600)  # Zmieniamy setGeometry na resize
        self.center_window()  # Wywołujemy centrowanie okna
        self.setStyleSheet("background-color: white; color: black; border: none;")

        
        self.menu_widget = MenuWidget(self)
        self.setCentralWidget(self.menu_widget)

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2 - 50
        self.move(x, y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())