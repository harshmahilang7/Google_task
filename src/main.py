import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.app_window import GoogleTasksApp

def main():
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Google Tasks")
    app.setApplicationDisplayName("Google Tasks App")
    
    window = GoogleTasksApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()