import importlib.util
import os
import json
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QSlider, QWidget
from PySide6.QtGui import QPixmap, QTextOption, QMovie
from PySide6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class ModuleDialog(QDialog):
    def __init__(self, slides, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Moduł")
        self.resize(1200, 650)
        self.center_window()
        
        self.setStyleSheet("background-color: white; color: black;")
        
        self.slides = slides
        self.current_slide = 0
        
        self.layout = QVBoxLayout()
        self.content_widgets = []
        
        self.slide_container = QWidget()
        self.slide_layout = QVBoxLayout()
        self.slide_container.setLayout(self.slide_layout)
        self.layout.addWidget(self.slide_container)
        
        self.button_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("Wstecz")
        self.prev_button.clicked.connect(self.prev_slide)
        self.button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Dalej")
        self.next_button.clicked.connect(self.next_slide)
        self.button_layout.addWidget(self.next_button)

        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)
        
        self.show_slide()

    def show_slide(self):
        for widget in self.content_widgets:
            widget.setParent(None)
        self.content_widgets.clear()
        
        slide = self.slides[self.current_slide]
        
        for element in slide["elements"]:
            if element["type"] == "text":
                text_widget = QTextEdit()
                text_widget.setReadOnly(True)
                text_widget.setWordWrapMode(QTextOption.WordWrap)
                text_widget.setStyleSheet("background-color: white; color: black; border: none; font-size: 14px;")

                # Sprawdzenie, czy tekst ma być pogrubiony
                content = element["content"]
                if "bold" in element and element["bold"]:
                    content = f"<b>{content}</b>"

                text_widget.setHtml(content)  # Używamy setHtml zamiast setText, aby obsłużyć formatowanie HTML
                self.slide_layout.addWidget(text_widget)
                self.content_widgets.append(text_widget)
            
            elif element["type"] == "image":
                image_label = QLabel()
                image_label.setAlignment(Qt.AlignCenter)
                image_path = element["content"]
                if os.path.exists(image_path):
                    pixmap = QPixmap(image_path)
                    image_label.setPixmap(pixmap)
                    self.slide_layout.addWidget(image_label)
                    self.content_widgets.append(image_label)
            
            elif element["type"] == "math":
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

                fig, ax = plt.subplots(figsize=(5, 2))
                ax.text(0.5, 0.5, f"${element['content']}$", fontsize=20, ha='center', va='center')
                ax.axis("off")
                

                canvas = FigureCanvas(fig)
                self.slide_layout.addWidget(canvas)
                self.content_widgets.append(canvas)
            
            elif element["type"] == "simulation":
                self.run_simulation(element["content"]) 

            elif element["type"] == "gif":
                gif_label = QLabel()
                gif_label.setAlignment(Qt.AlignCenter)
                gif_path = element["content"]
                if os.path.exists(gif_path):
                    movie = QMovie(gif_path)
                    gif_label.setMovie(movie)
                    movie.start()
                    self.slide_layout.addWidget(gif_label)
                    self.content_widgets.append(gif_label) 

        # Dezaktywacja "Wstecz" na pierwszym slajdzie
        if not hasattr(self, 'is_loading') or not self.is_loading:
            self.prev_button.setEnabled(self.current_slide > 0)
            self.next_button.setEnabled(True)
        self.apply_button_style()

    def next_slide(self):
        if self.current_slide < len(self.slides) - 1:
            self.current_slide += 1
            self.show_slide()
        else:
            self.accept()
    
    def prev_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.show_slide()

    def run_simulation(self, simulation_data):
        script_path = simulation_data["script_path"]
        sliders_config = simulation_data.get("sliders", {})

        # Wyłączenie i wyszarzenie obu przycisków przed załadowaniem symulacji
        self.is_loading = True  # Flaga oznaczająca ładowanie symulacji

        # Dezaktywacja przycisków
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.apply_button_style()

        # Dodanie ikonki ładowania
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_gif = QMovie("img/loading.gif")  # Upewnij się, że masz ten plik w katalogu img/
        self.loading_label.setMovie(self.loading_gif)
        self.loading_gif.start()
        self.slide_layout.addWidget(self.loading_label)
        self.content_widgets.append(self.loading_label)

        # Opóźnione uruchomienie symulacji (imitacja długiego ładowania)
        QTimer.singleShot(1500, lambda: self.load_simulation(script_path, sliders_config))

    def load_simulation(self, script_path, sliders_config):
        # Usunięcie ikonki ładowania
        self.loading_label.setParent(None)
        self.content_widgets.remove(self.loading_label)

        if not os.path.exists(script_path):
            error_label = QLabel(f"Błąd: Plik {script_path} nie istnieje.")
            self.slide_layout.addWidget(error_label)
            self.content_widgets.append(error_label)
            return
        
        spec = importlib.util.spec_from_file_location("simulation_module", script_path)
        simulation_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(simulation_module)
        
        if not hasattr(simulation_module, "Simulation"):
            error_label = QLabel("Błąd: Brak klasy Simulation w module symulacji.")
            self.slide_layout.addWidget(error_label)
            self.content_widgets.append(error_label)
            return
        
        self.simulation_widget = simulation_module.Simulation()
        self.canvas = FigureCanvas(self.simulation_widget.fig)
        self.slide_layout.addWidget(self.canvas)
        self.content_widgets.append(self.canvas)
        
        for slider_name, slider_params in sliders_config.items():
            slider_container = QWidget()
            slider_layout = QVBoxLayout()
            
            slider_label = QLabel(f"{slider_name}: {slider_params['default']:.2f}")
            slider_label.setStyleSheet("color: black; font-size: 14px;")
            slider_layout.addWidget(slider_label)
            
            slider = QSlider(Qt.Horizontal)
            slider.setMinimum(int(slider_params["min"] * 100))
            slider.setMaximum(int(slider_params["max"] * 100))
            slider.setValue(int(slider_params["default"] * 100))
            slider.valueChanged.connect(lambda value, s_name=slider_name, lbl=slider_label: self.update_slider(value, s_name, lbl))
            slider_layout.addWidget(slider)
            
            slider_container.setLayout(slider_layout)
            self.slide_layout.addWidget(slider_container)
            self.content_widgets.append(slider_container)

        # Aktywacja przycisków po załadowaniu symulacji
        self.is_loading = False  # Koniec ładowania

        # Aktywacja przycisków poprawnie dopiero po zakończeniu ładowania
        self.prev_button.setEnabled(self.current_slide > 0)
        self.next_button.setEnabled(True)
        self.apply_button_style()

    def apply_button_style(self):
        """ Wyszarzenie nieaktywnych przycisków """
        for button in [self.prev_button, self.next_button]:
            if button.isEnabled():
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #888888; /* Domyślne szare tło */
                        color: black;
                        border: 2px solid #555555;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 4px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #444444; /* Ciemne podświetlenie */
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: #d3d3d3;
                        color: #888;
                        border: 1px solid gray;
                    }
                """)
            else:
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #888888; /* Domyślne szare tło */
                        color: black;
                        border: 2px solid #555555;
                        font-size: 14px;
                        font-weight: bold;
                        padding: 4px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #444444; /* Ciemne podświetlenie */
                        color: white;
                    }
                    QPushButton:disabled {
                        background-color: #d3d3d3;
                        color: #888;
                        border: 1px solid gray;
                    }
                """)
    def update_slider(self, value, slider_name, label):
        label.setText(f"{slider_name}: {value / 100:.2f}")
        self.simulation_widget.update_parameter(slider_name, value / 100)

    def center_window(self):
        screen_geometry = self.screen().geometry()
        x = (screen_geometry.width() - self.width()) // 2 
        y = (screen_geometry.height() - self.height()) // 2 - 30
        self.move(x, y)