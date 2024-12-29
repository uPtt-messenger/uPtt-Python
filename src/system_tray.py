import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon
from login import DarkLoginWindow
import utils

class SystemTray:
    def __init__(self, app: QApplication):
        self.app = app
        self.tray_icon = None
        self.login_window = None
        self.setup_icon()

    def setup_icon(self):
        try:
            # 創建系統托盤圖標
            self.tray_icon = QSystemTrayIcon(self.app)
            self.tray_icon.setIcon(QIcon(f'{utils.script_path}/assets/icon.jpeg'))
            
            # 創建右鍵選單
            menu = QMenu()
            login_action = menu.addAction("登入")
            login_action.triggered.connect(self.show_login_window)
            
            chat_action = menu.addAction("新聊天視窗")
            chat_action.triggered.connect(self.new_chat_window)
            
            about_action = menu.addAction("關於")
            about_action.triggered.connect(self.show_about)
            
            quit_action = menu.addAction("退出")
            quit_action.triggered.connect(self.quit_application)
            
            self.tray_icon.setContextMenu(menu)
            self.tray_icon.show()
            
        except Exception as e:
            print(f"Error setting up system tray icon: {e}")
            self.tray_icon = None

    def show_login_window(self):
        try:
            if not self.login_window:
                self.login_window = DarkLoginWindow()
            
            # 如果視窗被最小化，恢復它
            if self.login_window.isMinimized():
                self.login_window.showNormal()
            
            # 顯示視窗並帶到前景
            self.login_window.show()
            self.login_window.raise_()
            self.login_window.activateWindow()
            
        except Exception as e:
            print(f"Error showing login window: {e}")

    def new_chat_window(self):
        msg = QMessageBox()
        msg.setWindowTitle("提示")
        msg.setText("新聊天視窗功能即將推出")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def show_about(self):
        msg = QMessageBox()
        msg.setWindowTitle("關於 uPtt")
        msg.setText("uPtt Messenger")
        msg.setInformativeText("版本: 1.0.0\n\n一個現代化的 PTT 即時通訊軟體")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()

    def quit_application(self):
        self.tray_icon.hide()
        self.app.quit()
        
    def run(self):
        try:
            if self.tray_icon:
                self.app.exec()
        except Exception as e:
            print(f"Error running system tray: {e}")

if __name__ == "__main__":
    app = QApplication([])
    system_tray = SystemTray(app)
    system_tray.run()
