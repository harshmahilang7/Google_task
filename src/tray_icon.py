from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import os

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        # Set icon
        icon_path = os.path.join("assets", "icons", "tray.png")
        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
        
        # Create menu
        menu = QMenu()
        
        # Quick Actions
        new_task = QAction("Add New Task", self.parent)
        new_task.triggered.connect(self.parent.add_new_task)
        menu.addAction(new_task)
        
        complete_task = QAction("Complete Task", self.parent)
        complete_task.triggered.connect(self.parent.complete_selected_task)
        menu.addAction(complete_task)
        
        menu.addSeparator()
        
        # Export Submenu
        export_menu = QMenu("Export Tasks", self.parent)
        
        export_json = QAction("JSON", self.parent)
        export_json.triggered.connect(lambda: self.parent.export_tasks('json'))
        
        export_csv = QAction("CSV", self.parent)
        export_csv.triggered.connect(lambda: self.parent.export_tasks('csv'))
        
        export_txt = QAction("Text", self.parent)
        export_txt.triggered.connect(lambda: self.parent.export_tasks('txt'))
        
        export_menu.addAction(export_json)
        export_menu.addAction(export_csv)
        export_menu.addAction(export_txt)
        menu.addMenu(export_menu)
        
        menu.addSeparator()
        
        # Window Control
        show_hide = QAction("Show/Hide", self.parent)
        show_hide.triggered.connect(self.toggle_window)
        menu.addAction(show_hide)
        
        fullscreen = QAction("Toggle Fullscreen", self.parent)
        fullscreen.triggered.connect(self.parent.toggle_fullscreen)
        menu.addAction(fullscreen)
        
        menu.addSeparator()
        
        # App Control
        quit_action = QAction("Exit", self.parent)
        quit_action.triggered.connect(self.parent.close)
        menu.addAction(quit_action)
        
        self.setContextMenu(menu)
        self.setToolTip("Google Tasks\nDouble-click to show/hide\nRight-click for menu")
        self.activated.connect(self.on_tray_click)
    
    def toggle_window(self):
        if self.parent.isVisible():
            self.parent.hide()
        else:
            self.parent.show_normal()
    
    def on_tray_click(self, reason):
        if reason == self.Trigger:  # Single click
            self.toggle_window()
        elif reason == self.DoubleClick:
            self.parent.toggle_fullscreen()