import sys
import serial
import serial.tools.list_ports
import threading
import time
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                               QWidget, QLabel, QComboBox, QHBoxLayout, QGroupBox, QGridLayout)
from PySide6.QtCore import QTimer

# Helper: Generate PRBS (Pseudo-Random Binary Sequence)
def generate_prbs(length=1024, seed=None):
    if seed is not None:
        random.seed(seed)
    return bytes([random.getrandbits(8) for _ in range(length)])

class RS232Monitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PRBS RS232 Transmission Monitor")

        self.tx_port = None
        self.rx_port = None
        self.sniff_port = None
        self.running = False

        # UI Elements
        self.tx_combo = QComboBox()
        self.rx_combo = QComboBox()
        self.sniff_combo = QComboBox()
        self.prbs_type = QComboBox()
        self.status_label = QLabel("Status: Ready")
        self.start_button = QPushButton("Start Transmission")
        self.stop_button = QPushButton("Stop")

        self.tx_status = QLabel("TX: Not connected")
        self.rx_status = QLabel("RX: Not connected")
        self.sniff_status = QLabel("Sniffer: Not connected")

        self.tx_params = QLabel("TX Params: -")
        self.rx_params = QLabel("RX Params: -")
        self.sniff_params = QLabel("Sniffer Params: -")

        self.init_ui()

        # Refresh COM ports every second
        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.populate_ports)
        self.port_timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout()

        port_layout = QGridLayout()
        port_layout.addWidget(QLabel("TX Port:"), 0, 0)
        port_layout.addWidget(self.tx_combo, 0, 1)
        port_layout.addWidget(self.tx_status, 0, 2)
        port_layout.addWidget(self.tx_params, 0, 3)

        port_layout.addWidget(QLabel("RX Port:"), 1, 0)
        port_layout.addWidget(self.rx_combo, 1, 1)
        port_layout.addWidget(self.rx_status, 1, 2)
        port_layout.addWidget(self.rx_params, 1, 3)

        port_layout.addWidget(QLabel("Sniffer Port:"), 2, 0)
        port_layout.addWidget(self.sniff_combo, 2, 1)
        port_layout.addWidget(self.sniff_status, 2, 2)
        port_layout.addWidget(self.sniff_params, 2, 3)

        prbs_layout = QHBoxLayout()
        prbs_layout.addWidget(QLabel("PRBS Type:"))
        self.prbs_type.addItems(["PRBS-8", "PRBS-15", "PRBS-23"])
        prbs_layout.addWidget(self.prbs_type)

        layout.addLayout(port_layout)
        layout.addLayout(prbs_layout)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.start_button.clicked.connect(self.start_transmission)
        self.stop_button.clicked.connect(self.stop_transmission)

    def populate_ports(self):
        current_ports = [port.device for port in serial.tools.list_ports.comports()]

        def update_combo(combo):
            selected = combo.currentText()
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(current_ports)
            if selected in current_ports:
                combo.setCurrentText(selected)
            combo.blockSignals(False)

        update_combo(self.tx_combo)
        update_combo(self.rx_combo)
        update_combo(self.sniff_combo)

    def start_transmission(self):
        tx_name = self.tx_combo.currentText()
        rx_name = self.rx_combo.currentText()
        sniff_name = self.sniff_combo.currentText()

        try:
            self.tx_port = serial.Serial(tx_name, 9600, timeout=1)
            self.tx_status.setText(f"TX: {tx_name} opened")
            self.tx_params.setText("Baud: 9600, Timeout: 1")
        except Exception as e:
            self.status_label.setText(f"TX error: {e}")
            return

        try:
            self.rx_port = serial.Serial(rx_name, 9600, timeout=1)
            self.rx_status.setText(f"RX: {rx_name} opened")
            self.rx_params.setText("Baud: 9600, Timeout: 1")
        except Exception as e:
            self.status_label.setText(f"RX error: {e}")
            return

        try:
            self.sniff_port = serial.Serial(sniff_name, 9600, timeout=1)
            self.sniff_status.setText(f"Sniffer: {sniff_name} opened")
            self.sniff_params.setText("Baud: 9600, Timeout: 1")
        except Exception as e:
            self.status_label.setText(f"Sniffer error: {e}")
            return

        self.running = True
        self.tx_thread = threading.Thread(target=self.transmit_prbs)
        self.rx_thread = threading.Thread(target=self.receive_data)
        self.sniff_thread = threading.Thread(target=self.sniff_data)

        self.tx_thread.start()
        self.rx_thread.start()
        self.sniff_thread.start()

        self.status_label.setText("Status: Transmitting")

    def stop_transmission(self):
        self.running = False
        self.status_label.setText("Status: Stopped")
        for port, label, param in [
            (self.tx_port, self.tx_status, self.tx_params),
            (self.rx_port, self.rx_status, self.rx_params),
            (self.sniff_port, self.sniff_status, self.sniff_params),
        ]:
            if port and port.is_open:
                port.close()
            label.setText("Not connected")
            param.setText("-")

    def transmit_prbs(self):
        while self.running:
            data = generate_prbs(256)
            self.tx_port.write(data)
            time.sleep(0.5)

    def receive_data(self):
        while self.running:
            data = self.rx_port.read(256)
            # TODO: implement BER/PER calculation here
            pass

    def sniff_data(self):
        while self.running:
            data = self.sniff_port.read(256)
            # TODO: implement sniffer BER/PER analysis here
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RS232Monitor()
    window.show()
    sys.exit(app.exec())
