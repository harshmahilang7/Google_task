import os
import json
from PyQt5.QtCore import QSize, QUrl, Qt, QTimer, QDateTime
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QMenuBar, 
                            QMenu, QAction, QSystemTrayIcon, QStatusBar,
                            QInputDialog, QMessageBox, QFileDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineSettings
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QSound

class GoogleTasksApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration
        self.zoom_factor = 1.0
        self.current_theme = "light"
        self.font_size = 14
        self.notification_enabled = True
        self.notification_sound = True
        
        # Initialize UI
        self.init_ui()
        self.create_menu_bar()
        self.init_tray_icon()
        self.create_status_bar()
        self.setup_notification_checker()
    
    def init_ui(self):
        self.setWindowTitle("Google Tasks")
        self.setMinimumSize(QSize(800, 600))
        
        # Main browser view
        self.browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        
        # Enable web engine features
        settings = self.browser.settings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        
        self.browser.setUrl(QUrl("https://tasks.google.com/embed/"))
        
        # Layout with subtle margins
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.browser)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        # Apply initial view settings
        self.apply_view_settings()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Tasks Menu
        tasks_menu = menubar.addMenu("Tasks")
        
        # Add Task
        add_task = QAction("Add New Task", self)
        add_task.setShortcut("Ctrl+N")
        add_task.triggered.connect(self.add_new_task)
        tasks_menu.addAction(add_task)
        
        # Complete Selected Task
        complete_task = QAction("Complete Selected Task", self)
        complete_task.setShortcut("Ctrl+D")
        complete_task.triggered.connect(self.complete_selected_task)
        tasks_menu.addAction(complete_task)
        
        # Export Submenu
        export_menu = QMenu("Export Tasks", self)
        
        export_json = QAction("JSON", self)
        export_json.triggered.connect(lambda: self.export_tasks('json'))
        
        export_csv = QAction("CSV", self)
        export_csv.triggered.connect(lambda: self.export_tasks('csv'))
        
        export_txt = QAction("Text", self)
        export_txt.triggered.connect(lambda: self.export_tasks('txt'))
        
        export_menu.addAction(export_json)
        export_menu.addAction(export_csv)
        export_menu.addAction(export_txt)
        tasks_menu.addMenu(export_menu)
        
        # View Menu
        view_menu = menubar.addMenu("View")
        
        # Zoom Submenu
        zoom_menu = QMenu("Zoom", self)
        
        zoom_in = QAction("Zoom In (+)", self)
        zoom_in.setShortcut("Ctrl++")
        zoom_in.triggered.connect(lambda: self.adjust_zoom(0.1))
        
        zoom_out = QAction("Zoom Out (-)", self)
        zoom_out.setShortcut("Ctrl+-")
        zoom_out.triggered.connect(lambda: self.adjust_zoom(-0.1))
        
        reset_zoom = QAction("Reset Zoom", self)
        reset_zoom.setShortcut("Ctrl+0")
        reset_zoom.triggered.connect(lambda: self.set_zoom(1.0))
        
        zoom_menu.addAction(zoom_in)
        zoom_menu.addAction(zoom_out)
        zoom_menu.addAction(reset_zoom)
        
        # Theme Submenu
        theme_menu = QMenu("Theme", self)
        
        light_theme = QAction("Light", self)
        light_theme.triggered.connect(lambda: self.set_theme("light"))
        
        dark_theme = QAction("Dark", self)
        dark_theme.triggered.connect(lambda: self.set_theme("dark"))
        
        sepia_theme = QAction("Sepia", self)
        sepia_theme.triggered.connect(lambda: self.set_theme("sepia"))
        
        theme_menu.addAction(light_theme)
        theme_menu.addAction(dark_theme)
        theme_menu.addAction(sepia_theme)
        
        # Font Size Submenu
        font_menu = QMenu("Font Size", self)
        
        font_sizes = [10, 12, 14, 16, 18]
        for size in font_sizes:
            action = QAction(f"{size}px", self)
            action.triggered.connect(lambda _, s=size: self.set_font_size(s))
            font_menu.addAction(action)
        
        # Fullscreen toggle
        fullscreen_action = QAction("Toggle Fullscreen", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        
        # Add to view menu
        view_menu.addMenu(zoom_menu)
        view_menu.addMenu(theme_menu)
        view_menu.addMenu(font_menu)
        view_menu.addSeparator()
        view_menu.addAction(fullscreen_action)
        
        # Settings Menu
        settings_menu = menubar.addMenu("Settings")
        
        # Notifications
        notification_action = QAction("Notification Settings", self)
        notification_action.triggered.connect(self.show_notification_settings)
        settings_menu.addAction(notification_action)
    
    def create_status_bar(self):
        self.statusBar().showMessage("Ready")
        self.statusBar().setFont(QFont("Segoe UI", 9))
    
    def init_tray_icon(self):
        """Initialize system tray icon with enhanced menu"""
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.join("assets", "icons", "tray.png")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # Create tray menu
        tray_menu = QMenu()
        
        # Quick Actions
        new_task = QAction("Add New Task", self)
        new_task.triggered.connect(self.add_new_task)
        tray_menu.addAction(new_task)
        
        complete_task = QAction("Complete Task", self)
        complete_task.triggered.connect(self.complete_selected_task)
        tray_menu.addAction(complete_task)
        
        tray_menu.addSeparator()
        
        # Window Control
        show_hide = QAction("Show/Hide", self)
        show_hide.triggered.connect(self.toggle_window_visibility)
        tray_menu.addAction(show_hide)
        
        fullscreen = QAction("Toggle Fullscreen", self)
        fullscreen.triggered.connect(self.toggle_fullscreen)
        tray_menu.addAction(fullscreen)
        
        tray_menu.addSeparator()
        
        # App Control
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_click)
        self.tray_icon.show()
    
    def setup_notification_checker(self):
        """Setup timer for checking due tasks"""
        if self.notification_enabled:
            self.notification_timer = QTimer()
            self.notification_timer.timeout.connect(self.check_due_tasks)
            self.notification_timer.start(60000)  # Check every minute
    
    def check_due_tasks(self):
        """Check for due tasks and show notifications"""
        if not self.notification_enabled:
            return
            
        js = """
        function getDueTasks() {
            const dueTasks = [];
            const now = new Date();
            const items = document.querySelectorAll('[role="listitem"]');
            
            items.forEach(item => {
                const checkbox = item.querySelector('input[type="checkbox"]');
                if (checkbox && !checkbox.checked) {
                    const dateElem = item.querySelector('[aria-label="Due date"]');
                    if (dateElem && dateElem.textContent) {
                        const dueDate = new Date(dateElem.textContent);
                        if (dueDate <= now) {
                            const titleElem = item.querySelector('[aria-label="Task title"]');
                            if (titleElem) {
                                dueTasks.push({
                                    title: titleElem.textContent,
                                    due: dateElem.textContent
                                });
                            }
                        }
                    }
                }
            });
            
            return dueTasks;
        }
        getDueTasks();
        """
        
        self.browser.page().runJavaScript(js, self.show_due_task_notifications)
    
    def show_due_task_notifications(self, due_tasks):
        """Show notifications for due tasks"""
        if not due_tasks or not self.notification_enabled:
            return
            
        for task in due_tasks:
            self.tray_icon.showMessage(
                "Task Due!",
                f"'{task['title']}' was due on {task['due']}",
                QSystemTrayIcon.Warning,
                10000
            )
            if self.notification_sound:
                QSound.play(os.path.join("assets", "sounds", "notification.mp3"))
    
    def apply_view_settings(self):
        """Apply all current view settings"""
        self.browser.setZoomFactor(self.zoom_factor)
        self.inject_css(self.get_theme_css())
        self.inject_css(f"body {{ font-size: {self.font_size}px; }}")
    
    def adjust_zoom(self, delta):
        """Adjust zoom by delta amount"""
        self.zoom_factor += delta
        self.zoom_factor = max(0.5, min(2.0, self.zoom_factor))
        self.browser.setZoomFactor(self.zoom_factor)
        self.statusBar().showMessage(f"Zoom: {int(self.zoom_factor*100)}%", 2000)
    
    def set_zoom(self, factor):
        """Set zoom to specific factor"""
        self.zoom_factor = factor
        self.browser.setZoomFactor(self.zoom_factor)
        self.statusBar().showMessage("Zoom reset to 100%", 2000)
    
    def set_theme(self, theme_name):
        """Change application theme"""
        self.current_theme = theme_name
        self.inject_css(self.get_theme_css())
        self.statusBar().showMessage(f"Theme set to {theme_name.capitalize()}", 2000)
    
    def set_font_size(self, size):
        """Change base font size"""
        self.font_size = size
        self.inject_css(f"body {{ font-size: {size}px; }}")
        self.statusBar().showMessage(f"Font size set to {size}px", 2000)
    
    def get_theme_css(self):
        """Return CSS for current theme"""
        themes = {
            "light": """
                body { 
                    background-color: #ffffff;
                    color: #202124;
                }
                [role="listitem"] {
                    background-color: #f8f9fa !important;
                }
            """,
            "dark": """
                body { 
                    background-color: #202124;
                    color: #e8eaed;
                }
                [role="listitem"] {
                    background-color: #303134 !important;
                }
                input, textarea {
                    background-color: #303134 !important;
                    color: #e8eaed !important;
                }
            """,
            "sepia": """
                body { 
                    background-color: #f4ecd8;
                    color: #5b4636;
                }
                [role="listitem"] {
                    background-color: #e8e0c8 !important;
                }
            """
        }
        return themes.get(self.current_theme, themes["light"])
    
    def inject_css(self, css):
        """Safely inject CSS into the web view"""
        # Sanitize CSS input
        sanitized_css = css.replace('`', r'\`').replace('${', r'\${')
        
        js = """
        try {
            const style = document.createElement('style');
            style.textContent = `%s`;
            document.head.appendChild(style);
        } catch (e) {
            console.error('CSS injection failed:', e);
        }
        """ % sanitized_css
        
        self.browser.page().runJavaScript(js)
    
    def add_new_task(self):
        """Add a new task through dialog"""
        task_name, ok = QInputDialog.getText(
            self, "Add New Task", "Task description:"
        )
        
        if ok and task_name:
            due_date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
            js = f"""
            try {{
                const input = document.querySelector('input[aria-label="Add a task"]');
                if (input) {{
                    input.value = `{task_name.replace('`', r'\`')}`;
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    const dateInput = document.querySelector('input[aria-label="Due date"]');
                    if (dateInput) {{
                        dateInput.value = `{due_date}`;
                        dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                    
                    const addButton = document.querySelector('div[role="button"][aria-label="Add task"]');
                    if (addButton) addButton.click();
                }}
            }} catch (e) {{
                console.error('Failed to add task:', e);
            }}
            """
            self.browser.page().runJavaScript(js)
            self.statusBar().showMessage(f"Added task: {task_name}", 3000)
    
    def complete_selected_task(self):
        """Mark selected task as complete"""
        js = """
        try {
            const selected = document.querySelector('[role="listitem"][aria-selected="true"]');
            if (selected) {
                const checkbox = selected.querySelector('input[type="checkbox"]');
                if (checkbox) {
                    checkbox.click();
                    return true;
                }
            }
            return false;
        } catch (e) {
            console.error('Failed to complete task:', e);
            return false;
        }
        """
        
        self.browser.page().runJavaScript(js, self.handle_task_completion)
    
    def handle_task_completion(self, success):
        """Callback for task completion"""
        if success:
            self.statusBar().showMessage("Task marked as complete", 3000)
        else:
            QMessageBox.warning(self, "No Task Selected", 
                              "Please select a task first by clicking on it")
    
    def export_tasks(self, format_type):
        """Export tasks to different formats"""
        js = """
        function getTasks() {
            const tasks = [];
            const items = document.querySelectorAll('[role="listitem"]');
            
            items.forEach(item => {
                const textElem = item.querySelector('[aria-label="Task title"]');
                const dateElem = item.querySelector('[aria-label="Due date"]');
                const completed = !!item.querySelector('input[type="checkbox"]:checked');
                
                if (textElem) {
                    tasks.push({
                        title: textElem.textContent,
                        due: dateElem ? dateElem.textContent : '',
                        completed: completed
                    });
                }
            });
            
            return tasks;
        }
        getTasks();
        """
        
        self.browser.page().runJavaScript(js, lambda result: self.process_export(result, format_type))
    
    def process_export(self, tasks, format_type):
        """Process exported tasks based on format"""
        if not tasks:
            QMessageBox.warning(self, "No Tasks", "No tasks found to export")
            return
        
        if format_type == 'json':
            self.export_json(tasks)
        elif format_type == 'csv':
            self.export_csv(tasks)
        elif format_type == 'txt':
            self.export_txt(tasks)
    
    def export_json(self, tasks):
        """Export tasks to JSON file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Tasks", "", "JSON Files (*.json)")
        
        if filename:
            with open(filename, 'w') as f:
                json.dump(tasks, f, indent=2)
            self.statusBar().showMessage(f"Tasks exported to {filename}", 5000)
    
    def export_csv(self, tasks):
        """Export tasks to CSV file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Tasks", "", "CSV Files (*.csv)")
        
        if filename:
            import csv
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Title', 'Due Date', 'Completed'])
                for task in tasks:
                    writer.writerow([task['title'], task['due'], task['completed']])
            self.statusBar().showMessage(f"Tasks exported to {filename}", 5000)
    
    def export_txt(self, tasks):
        """Export tasks to plain text file"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Tasks", "", "Text Files (*.txt)")
        
        if filename:
            with open(filename, 'w') as f:
                for task in tasks:
                    status = "✓" if task['completed'] else "✗"
                    f.write(f"{status} {task['title']} (Due: {task['due']})\n")
            self.statusBar().showMessage(f"Tasks exported to {filename}", 5000)
    
    def show_notification_settings(self):
        """Show notification settings dialog"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Notification Settings")
        layout = QVBoxLayout()
        
        # Notification toggle
        notify_check = QCheckBox("Enable notifications", dialog)
        notify_check.setChecked(self.notification_enabled)
        
        # Sound toggle
        sound_check = QCheckBox("Enable notification sound", dialog)
        sound_check.setChecked(self.notification_sound)
        sound_check.setEnabled(self.notification_enabled)
        
        # Connect signals
        notify_check.toggled.connect(lambda x: setattr(self, 'notification_enabled', x))
        notify_check.toggled.connect(sound_check.setEnabled)
        sound_check.toggled.connect(lambda x: setattr(self, 'notification_sound', x))
        
        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(dialog.accept)
        
        # Add widgets to layout
        layout.addWidget(notify_check)
        layout.addWidget(sound_check)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def toggle_window_visibility(self):
        """Toggle window visibility"""
        if self.isVisible():
            self.hide()
        else:
            self.show_normal()
    
    def show_normal(self):
        """Restore window from minimized or hidden state"""
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized)
        self.activateWindow()
    
    def on_tray_click(self, reason):
        """Handle tray icon clicks"""
        if reason == QSystemTrayIcon.Trigger:  # Single click
            self.toggle_window_visibility()
        elif reason == QSystemTrayIcon.DoubleClick:
            self.toggle_fullscreen()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def closeEvent(self, event):
        """Handle window close event"""
        if hasattr(self, 'tray_icon') and self.tray_icon.isVisible():
            self.hide()
            event.ignore()