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
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal, QThread

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TrackerThread(QThread):
    update_status = pyqtSignal(str)
    
    def __init__(self, target_color, threshold, sensitivity):
        super().__init__()
        self.target_color = target_color
        self.threshold = threshold
        self.sensitivity = sensitivity
        self.running = True
        self.active = False
        self.mode = "Head"
        
    def run(self):
        while self.running:
            if self.active:
                try:
                    screenshot = pyautogui.screenshot()
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    
                    diff = np.abs(frame - self.target_color)
                    mask = np.sum(diff, axis=2) < self.threshold
                    mask = mask.astype(np.uint8) * 255
                    
                    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    if contours:
                        largest = max(contours, key=cv2.contourArea)
                        M = cv2.moments(largest)
                        if M['m00'] != 0:
                            cx = int(M['m10'] / M['m00'])
                            cy = int(M['m01'] / M['m00'])
                            
                            screen_width, screen_height = pyautogui.size()
                            center_x = screen_width // 2
                            center_y = screen_height // 2
                            
                            move_x = int((cx - center_x) * self.sensitivity)
                            move_y = int((cy - center_y) * self.sensitivity)
                            
                            pyautogui.moveRel(move_x, move_y, duration=0.01)
                            self.update_status.emit(f"Tracking | Target at ({cx}, {cy})")
                except Exception as e:
                    self.update_status.emit(f"Error: {str(e)}")
            
            if keyboard.is_pressed('f8'):
                self.running = False
                self.update_status.emit("Tracking stopped by user")
                break
                
            time.sleep(0.01)
    
    def activate(self, mode):
        self.active = True
        self.mode = mode
    
    def deactivate(self):
        self.active = False
    
    def set_color(self, color):
        self.target_color = color
    
    def set_threshold(self, threshold):
        self.threshold = threshold
    
    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        
    def stop(self):
        self.running = False
        self.wait(500)

class AimAssistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COD AimAssist v1.5")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.setGeometry(100, 100, 900, 700)
        
        self.target_color = np.array([201, 0, 141])
        self.threshold = 40
        self.sensitivity = 0.7
        
        # لن ننشئ الخيط هنا
        self.tracker = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # ... (نفس كود الواجهة) ...
        # أبقِ كود الواجهة كما هو

    # ... (بقية الدوال) ...
    
    def start_tracker(self):
        """إنشاء وتشغيل الخيط بعد إنشاء الواجهة"""
        if self.tracker and self.tracker.isRunning():
            self.tracker.stop()
        
        self.tracker = TrackerThread(
            self.target_color, 
            self.threshold, 
            self.sensitivity
        )
        self.tracker.update_status.connect(self.update_status)
        self.tracker.start()
        
    def activate_aim_assist(self, name):
        if not self.tracker or not self.tracker.isRunning():
            self.start_tracker()
        self.tracker.activate(name)
        self.status_label.setText(f"Active: {name} | Press F8 to stop")
        
    def deactivate_aim_assist(self, name):
        if self.tracker and self.tracker.isRunning():
            self.tracker.deactivate()
        self.status_label.setText("Aim assist deactivated")
        
    def set_color(self, color):
        self.target_color = color
        if self.tracker:
            self.tracker.set_color(color)
        
    def set_threshold(self, threshold):
        self.threshold = threshold
        if self.tracker:
            self.tracker.set_threshold(threshold)
    
    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity
        if self.tracker:
            self.tracker.set_sensitivity(sensitivity)

    def closeEvent(self, event):
        if self.tracker and self.tracker.isRunning():
            self.tracker.stop()
        event.accept()

if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
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
    
    # بدء الخيط بعد عرض النافذة
    QTimer.singleShot(500, window.start_tracker)
    
    sys.exit(app.exec_())