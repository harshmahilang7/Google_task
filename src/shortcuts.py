from PyQt5.QtWidgets import QAction
from PyQt5.Qt import QKeySequence

def setup_shortcuts(window):
    # New Task (Ctrl+N)
    new_task = QAction(window)
    new_task.setShortcut(QKeySequence("Ctrl+N"))
    new_task.triggered.connect(
        lambda: window.browser.page().runJavaScript("""
            document.querySelector('div[role="button"]').click();
        """)
    )
    window.addAction(new_task)
    
    # Refresh (F5)
    refresh = QAction(window)
    refresh.setShortcut(QKeySequence("F5"))
    refresh.triggered.connect(window.browser.reload)
    window.addAction(refresh)
    
    # Fullscreen (F11)
    fullscreen = QAction(window)
    fullscreen.setShortcut(QKeySequence("F11"))
    fullscreen.triggered.connect(window.toggle_fullscreen)
    window.addAction(fullscreen)