import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow
from modules.menu import MenuWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zasady Detekcji Bezpośredniej i Koherentnej")
        self.setGeometry(000, 100, 800, 600)
        
        self.menu_widget = MenuWidget(self)
        self.setCentralWidget(self.menu_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())