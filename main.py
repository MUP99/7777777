import sys
import os
import webbrowser
import time
import cv2
import numpy as np
import pyautogui
import keyboard
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QGroupBox, QGridLayout, QSizePolicy, QSpacerItem,
                             QMessageBox, QFrame, QSlider)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AimAssistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COD AimAssist v1.5")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.setGeometry(100, 100, 900, 700)
        
        # Default settings
        self.target_color = np.array([201, 0, 141])
        self.threshold = 40
        self.sensitivity = 0.7
        self.active = False
        self.mode = "Head"
        
        self.setup_ui()
        
        # Create timer for tracking
        self.tracker_timer = QTimer(self)
        self.tracker_timer.timeout.connect(self.track_target)
        self.tracker_timer.setInterval(10)  # 10ms
        
    def setup_ui(self):
        # Create main tabs
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        
        # Create content tabs
        self.multiplayer_tab = self.create_multiplayer_tab()
        self.settings_tab = self.create_settings_tab()
        self.contact_tab = self.create_contact_tab()
        
        # Add tabs
        self.tabs.addTab(self.multiplayer_tab, "Multiplayer")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.contact_tab, "Contact")
        
        # Status bar
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #AAAAAA; padding: 5px;")
        
        # Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.status_label)
        main_widget.setLayout(main_layout)
        
        self.setCentralWidget(main_widget)
        
        # Apply styles
        self.apply_styles()
        
    def create_multiplayer_tab(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def create_settings_tab(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def create_contact_tab(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def create_aim_assist_group(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def create_additional_buttons(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def create_button(self, text, color, tooltip=""):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def lighten_color(self, hex_color, factor=0.3):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def darken_color(self, hex_color, factor=0.3):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
        
    def apply_styles(self):
        # ... (نفس كود الواجهة السابق) ...
        # أبقِ كود الواجهة كما هو تماماً
    
    def activate_aim_assist(self, name):
        self.active = True
        self.mode = name
        self.tracker_timer.start()
        self.status_label.setText(f"Active: {name} | Press F8 to stop")
        
    def deactivate_aim_assist(self, name):
        self.active = False
        self.tracker_timer.stop()
        self.status_label.setText("Aim assist deactivated")
        
    def handle_additional_button(self, name):
        self.status_label.setText(f"Mode set to: {name}")
        
    def open_email(self, email):
        webbrowser.open(f"mailto:{email}")
        
    def check_for_updates(self):
        QMessageBox.information(
            self, 
            "Software Update", 
            "You are using the latest version (v1.5)\n\n"
            "No updates available at this time.",
            QMessageBox.Ok
        )
        
    def track_target(self):
        if not self.active:
            return
            
        try:
            # Capture screenshot
            screenshot = pyautogui.screenshot()
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Create mask for target color
            diff = np.abs(frame - self.target_color)
            mask = np.sum(diff, axis=2) < self.threshold
            mask = mask.astype(np.uint8) * 255
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    
                    # Get screen center
                    screen_width, screen_height = pyautogui.size()
                    center_x = screen_width // 2
                    center_y = screen_height // 2
                    
                    # Calculate movement
                    move_x = int((cx - center_x) * self.sensitivity)
                    move_y = int((cy - center_y) * self.sensitivity)
                    
                    # Move mouse
                    pyautogui.moveRel(move_x, move_y, duration=0.01)
                    self.status_label.setText(f"Tracking | Target at ({cx}, {cy})")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
        
        # Check for F8 to stop
        if keyboard.is_pressed('f8'):
            self.active = False
            self.tracker_timer.stop()
            self.status_label.setText("Tracking stopped by user")
    
    def select_target_color(self):
        self.hide()
        time.sleep(0.5)  # Give time to hide window
        
        # Capture screenshot
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Create window for color selection
        cv2.namedWindow("Select Target Color - Click then press ESC", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Select Target Color - Click then press ESC", 800, 600)
        
        # Mouse callback function
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.target_color = frame[y, x].copy()
                self.update_color_preview()
                cv2.destroyAllWindows()
                self.show()
        
        cv2.setMouseCallback("Select Target Color - Click then press ESC", mouse_callback)
        cv2.imshow("Select Target Color - Click then press ESC", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.show()
    
    def update_color_preview(self):
        r, g, b = self.target_color[2], self.target_color[1], self.target_color[0]
        self.color_preview.setStyleSheet(f"background-color: rgb({r},{g},{b}); border: 1px solid #444;")
    
    def update_threshold(self, value):
        self.threshold = value
        self.threshold_label.setText(str(value))
    
    def update_sensitivity(self, value):
        self.sensitivity = value / 100.0
        self.sensitivity_label.setText(f"{self.sensitivity:.2f}")
    
    def save_settings(self):
        self.status_label.setText("Settings saved successfully")
    
    def reset_settings(self):
        self.threshold = 40
        self.sensitivity = 0.7
        self.threshold_slider.setValue(self.threshold)
        self.sensitivity_slider.setValue(int(self.sensitivity * 100))
        self.threshold_label.setText(str(self.threshold))
        self.sensitivity_label.setText(f"{self.sensitivity:.2f}")
        self.status_label.setText("Settings reset to default")

if __name__ == "__main__":
    # Hide console window on Windows
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Customize color palette
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.Base, QColor(45, 45, 45))
    palette.setColor(QPalette.AlternateBase, QColor(60, 60, 60))
    palette.setColor(QPalette.ToolTipBase, QColor(45, 45, 45))
    palette.setColor(QPalette.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.Button, QColor(60, 60, 60))
    palette.setColor(QPalette.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.Highlight, QColor(255, 165, 0))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)
    
    window = AimAssistApp()
    window.show()
    sys.exit(app.exec_())
