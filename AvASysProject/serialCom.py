import serial
import serial.tools.list_ports
import threading
import time

from src.CTkMessagebox import CTkMessagebox


class COM:
    def __init__(self):
        self.com_ports = [port.device for port in serial.tools.list_ports.comports()]
        self.serial_port = None
        self.baudrate = None
        self.read_thread = None
        self.data_received = False
        self.is_connected = False

    def setSerialPort(self, serial_port):
        self.serial_port = serial_port

    def setBaudRate(self, baudrate):
        self.baudrate = baudrate

    def getSerialPort(self):
        return self.serial_port

    def getBaudRate(self):
        return self.baudrate

    def getSerialPorts(self):
        return self.com_ports

    def start_reading(self, console):
        try:
            self.serial_port = serial.Serial(self.getSerialPort(), self.getBaudRate(), timeout=1)
            self.read_thread = threading.Thread(target=lambda: self.read_data(console))
            self.read_thread.start()
            print("COM Bağlantısı Başarılı")

            # 5 saniye boyunca veri alınmazsa bağlantıyı durdur
            time.sleep(5)
            print(self.data_received)
            if not self.data_received:
                self.stop_reading(console)
                CTkMessagebox(title="Error", message="Belirli bir süre boyunca veri alınamadı. Bağlantı kapatıldı.",
                              icon="cancel")
                self.is_connected = False
            else:
                print("COM İstenilen Değer Okundu!")
                self.is_connected = True
                return True
        except serial.SerialException as e:
            CTkMessagebox(title="Error", message=str(e), icon="cancel")

    def stop_reading(self, console):
        try:
            if self.serial_port:
                self.serial_port.close()

            if self.read_thread and self.read_thread.is_alive():
                self.read_thread.join()

            self.is_connected = False

            console.configure(state="normal")
            console.insert("0.0", "Bağlantı kapatıldı\n")
            console.configure(state="disabled")
            return True
        except Exception as e:
            print(e)
            return False

    def read_data(self, console):
        while True:
            if self.serial_port.in_waiting > 0 and self.is_connected:
                try:
                    data = self.serial_port.readline().decode().strip()
                    if not self.data_received:
                        if str(data) == "0x55 Test Beat":
                            self.data_received = True
                            console.configure(state="normal")
                            console.insert("0.0", "Bağlantı Kuruldu\n")
                            console.configure(state="disabled")
                        else:
                            self.stop_reading()
                            CTkMessagebox(title="Error", message="Geçersiz mesaj. Bağlantı kapatıldı.",
                                          icon="cancel")
                            break
                    else:
                        strdata = str(data)
                        console.configure(state="normal")
                        console.insert("0.0", strdata + "\n")
                        console.configure(state="disabled")
                except Exception as e:
                    self.stop_reading(console)
                    CTkMessagebox(title="Error", message=str(e), icon="cancel")
                    break

            else:
                return
