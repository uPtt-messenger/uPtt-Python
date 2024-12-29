from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton)
from PyQt6.QtCore import Qt, QTimer, QRect, QPropertyAnimation
from PyQt6.QtGui import QFont, QPainter, QColor
import math

class LoadingSpinner(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.spinner_size = 40
        self.line_width = 3
        self.color = '#4a9eff'
        self.angle = 0
        self.running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self._draw_base_circle()
        
    def _draw_base_circle(self):
        """繪製底層淡色圓圈"""
        self.setFixedSize(self.spinner_size, self.spinner_size)
        self.setStyleSheet(f"""
            background: #2a2a2a;
            border-radius: {self.spinner_size // 2}px;
            border: {self.line_width}px solid #2a2a2a;
        """)
        
    def paintEvent(self, event):
        if not self.running:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 設置畫筆
        pen_width = self.line_width
        painter.setPen(Qt.PenStyle.NoPen)
        
        # 計算中心點和半徑
        center = self.rect().center()
        radius = (min(self.width(), self.height()) - pen_width) // 2
        
        # 繪製旋轉的弧形
        gradient = QColor(self.color)
        painter.setBrush(gradient)
        
        start_angle = self.angle * 16  # QPainter uses 16th of a degree
        span_angle = 120 * 16  # 120 degrees * 16
        
        painter.drawPie(self.rect().adjusted(pen_width, pen_width, -pen_width, -pen_width),
                       start_angle, span_angle)
        
    def rotate(self):
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def start(self):
        self.running = True
        self.timer.start(50)  # 更新頻率50毫秒
        self.show()
        
    def stop(self):
        self.running = False
        self.timer.stop()
        self.hide()

class FadeLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.alpha = 0
        self.fading = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._fade_step)
        self.hide()  # 初始時隱藏
        
    def fade_in(self):
        self.alpha = 0
        self.fading = True
        self.show()
        self.timer.start(50)  # 每50毫秒更新一次
        
    def _fade_step(self):
        if not self.fading:
            return
            
        if self.alpha < 1.0:
            self.alpha += 0.1
            self.setStyleSheet(f"color: rgba(74, 158, 255, {self.alpha});")
        else:
            self.fading = False
            self.timer.stop()

class DarkLoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("uPtt")
        self.setFixedSize(400, 500)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("uPtt Connect")
        title.setFont(QFont("SF Pro Display", 36))
        title.setStyleSheet("color: #4a9eff;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("The first PTT Messenger")
        subtitle.setFont(QFont("SF Pro Display", 14))
        subtitle.setStyleSheet("color: #a0a0a0;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Username
        username_label = QLabel("PTT ID")
        username_label.setFont(QFont("SF Pro Display", 13))
        username_label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(username_label)
        
        self.username_entry = QLineEdit()
        self.username_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                color: white;
            }
        """)
        layout.addWidget(self.username_entry)
        
        # Password
        password_label = QLabel("Password")
        password_label.setFont(QFont("SF Pro Display", 13))
        password_label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(password_label)
        
        self.password_entry = QLineEdit()
        self.password_entry.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_entry.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                color: white;
            }
        """)
        layout.addWidget(self.password_entry)
        
        # Login button
        self.login_button = QPushButton("Connect")
        self.login_button.setFont(QFont("SF Pro Display", 13))
        self.login_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #4a9eff;
                border: none;
                border-radius: 4px;
                color: white;
            }
            QPushButton:hover {
                background: #3a8eef;
            }
        """)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)
        
        # Spinner
        self.spinner = LoadingSpinner()
        self.spinner.setFixedSize(40, 40)
        layout.addWidget(self.spinner)
        
        # Status label
        self.status_label = FadeLabel()
        self.status_label.setFont(QFont("SF Pro Text", 12))
        self.status_label.setStyleSheet("color: #4a9eff;")
        layout.addWidget(self.status_label)
        
        # Version info
        version_label = QLabel("v1.0.0")
        version_label.setFont(QFont("SF Pro Text", 10))
        version_label.setStyleSheet("color: #666666;")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: #1e1e1e;
            }
            QWidget {
                background: #1e1e1e;
            }
        """)
        
    def login(self):
        username = self.username_entry.text().strip()
        password = self.password_entry.text()
        
        if not username or not password:
            return
        
        # 禁用登入按鈕並添加動畫效果
        self.login_button.setEnabled(False)
        animation = QPropertyAnimation(self.login_button, b"geometry")
        animation.setDuration(300)  # 300毫秒
        
        # 獲取按鈕當前位置
        current_geometry = self.login_button.geometry()
        
        # 創建一個輕微的"按下"效果
        pressed_geometry = QRect(
            current_geometry.x(),
            current_geometry.y() + 2,  # 向下移動2像素
            current_geometry.width(),
            current_geometry.height()
        )
        
        # 設置動畫
        animation.setStartValue(current_geometry)
        animation.setEndValue(pressed_geometry)
        animation.start()
        
        # 顯示載入動畫
        self.spinner.start()
        self.status_label.fade_in()
        self.status_label.setText("Connecting...")
        
        # TODO: Add login logic here
        print(f"Login attempt with username: {username}")
        self.hide()  # Hide window instead of closing
        
    def closeEvent(self, event):
        # Hide window instead of closing when user clicks the X button
        event.ignore()
        self.hide()
        
if __name__ == "__main__":
    app = QApplication([])
    window = DarkLoginWindow()
    window.show()
    app.exec()
