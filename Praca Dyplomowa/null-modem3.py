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
def generate_prbs(length=1024, seed=123):
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

        # Stats
        self.tx_sent = 0
        self.rx_received = 0
        self.rx_errors = 0
        self.sniff_received = 0
        self.sniff_errors = 0
        self.start_time = None

        # PRBS Reference Buffer
        self.prbs_data = generate_prbs(1024)
        self.rx_offset = 0
        self.sniff_offset = 0

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

        self.stats_label = QLabel("Stats: -")
        self.debug_label = QLabel("Debug: -")

        self.init_ui()

        self.port_timer = QTimer()
        self.port_timer.timeout.connect(self.populate_ports)
        self.port_timer.start(1000)

        self.stats_timer = QTimer()
        self.stats_timer.timeout.connect(self.update_stats)
        self.stats_timer.start(1000)

        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_port_statuses)
        self.status_timer.start(1000)

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
        layout.addWidget(self.stats_label)
        layout.addWidget(self.debug_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.start_button.clicked.connect(self.start_transmission)
        self.stop_button.clicked.connect(self.stop_transmission)

    def populate_ports(self):
        current_ports = [port.device for port in serial.tools.list_ports.comports()]

        selected_tx = self.tx_combo.currentText()
        selected_rx = self.rx_combo.currentText()
        selected_sniff = self.sniff_combo.currentText()

        self.tx_combo.blockSignals(True)
        self.rx_combo.blockSignals(True)
        self.sniff_combo.blockSignals(True)

        self.tx_combo.clear()
        self.rx_combo.clear()
        self.sniff_combo.clear()

        used_ports = set()

        for port in current_ports:
            if selected_tx == port:
                self.tx_combo.addItem(port)
                used_ports.add(port)
            elif selected_rx == port:
                self.rx_combo.addItem(port)
                used_ports.add(port)
            elif selected_sniff == port:
                self.sniff_combo.addItem(port)
                used_ports.add(port)

        for port in current_ports:
            if port not in used_ports:
                if self.tx_combo.count() == 0:
                    self.tx_combo.addItem(port)
                elif self.rx_combo.count() == 0:
                    self.rx_combo.addItem(port)
                elif self.sniff_combo.count() == 0:
                    self.sniff_combo.addItem(port)

        self.tx_combo.blockSignals(False)
        self.rx_combo.blockSignals(False)
        self.sniff_combo.blockSignals(False)

    def try_open_port(self, port_name, label, param_label, role):
        for attempt in range(3):
            try:
                port = serial.Serial(port_name, 9600, timeout=1)
                label.setText(f"{role}: {port_name} opened")
                param_label.setText("Baud: 9600, Timeout: 1")
                return port
            except Exception as e:
                time.sleep(0.5)
        self.status_label.setText(f"{role} error: {e}")
        return None

    def start_transmission(self):
        tx_name = self.tx_combo.currentText()
        rx_name = self.rx_combo.currentText()
        sniff_name = self.sniff_combo.currentText()

        self.tx_port = self.try_open_port(tx_name, self.tx_status, self.tx_params, "TX")
        if not self.tx_port:
            return

        self.rx_port = self.try_open_port(rx_name, self.rx_status, self.rx_params, "RX")
        if not self.rx_port:
            return

        self.sniff_port = self.try_open_port(sniff_name, self.sniff_status, self.sniff_params, "Sniffer")
        if not self.sniff_port:
            return

        self.running = True
        self.start_time = time.time()
        self.tx_sent = 0
        self.rx_received = 0
        self.rx_errors = 0
        self.sniff_received = 0
        self.sniff_errors = 0
        self.rx_offset = 0
        self.sniff_offset = 0

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
            try:
                self.tx_port.write(self.prbs_data)
                self.tx_sent += len(self.prbs_data)
                time.sleep(0.5)
            except Exception as e:
                self.status_label.setText(f"TX write error: {e}")
                self.tx_status.setText("TX: disconnected")
                self.running = False

    def receive_data(self):
        while self.running:
            try:
                data = self.rx_port.read(256)
                self.rx_received += len(data)
                for i, byte in enumerate(data):
                    expected = self.prbs_data[(self.rx_offset + i) % len(self.prbs_data)]
                    if byte != expected:
                        self.rx_errors += 1
                self.rx_offset = (self.rx_offset + len(data)) % len(self.prbs_data)
            except Exception as e:
                self.status_label.setText(f"RX read error: {e}")
                self.rx_status.setText("RX: disconnected")
                self.running = False

    def sniff_data(self):
        while self.running:
            try:
                data = self.sniff_port.read(256)
                self.sniff_received += len(data)
                for i, byte in enumerate(data):
                    expected = self.prbs_data[(self.sniff_offset + i) % len(self.prbs_data)]
                    if byte != expected:
                        self.sniff_errors += 1
                self.sniff_offset = (self.sniff_offset + len(data)) % len(self.prbs_data)
            except Exception as e:
                self.status_label.setText(f"Sniffer read error: {e}")
                self.sniff_status.setText("Sniffer: disconnected")
                self.running = False

    def update_stats(self):
        if self.start_time:
            duration = time.time() - self.start_time
            if self.rx_received > 0:
                rx_ber = self.rx_errors / (self.rx_received * 8)
                rx_ber_str = f"{rx_ber:.2e}"
            else:
                rx_ber_str = "No RX data"

            if self.sniff_received > 0:
                sniff_ber = self.sniff_errors / (self.sniff_received * 8)
                sniff_ber_str = f"{sniff_ber:.2e}"
            else:
                sniff_ber_str = "No Sniff data"

            self.stats_label.setText(
                f"Time: {duration:.1f}s | RX BER: {rx_ber_str} | Sniff BER: {sniff_ber_str}"
            )

            self.debug_label.setText(
                f"RX Bytes: {self.rx_received}, Errors: {self.rx_errors} | Sniff Bytes: {self.sniff_received}, Errors: {self.sniff_errors}"
            )

    def update_port_statuses(self):
        def check_port(port, label):
            if port and not port.is_open:
                label.setText("Disconnected")
        check_port(self.tx_port, self.tx_status)
        check_port(self.rx_port, self.rx_status)
        check_port(self.sniff_port, self.sniff_status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RS232Monitor()
    window.show()
    sys.exit(app.exec())
