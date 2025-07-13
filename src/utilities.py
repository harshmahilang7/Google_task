import os
import sys
from PyQt5.QtCore import QStandardPaths

def resource_path(relative_path):
    """Get absolute path to resource"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_data_dir():
    """Get application data directory"""
    return QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)

def ensure_directory_exists(path):
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)