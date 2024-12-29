from PyQt6.QtWidgets import QApplication
from system_tray import SystemTray
from login import DarkLoginWindow
import sys

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.system_tray = None
        
    def start(self):
        # Initialize system tray
        self.system_tray = SystemTray(self.app)
        
        # Create and show login window
        self.login_window = DarkLoginWindow()
        self.login_window.show()
        
        # Start the application event loop
        self.app.exec()

def main():
    app = Application()
    app.start()

if __name__ == "__main__":
    main()