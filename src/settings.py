import json
import os

def load_settings():
    default_settings = {
        'theme': 'light',
        'notifications': True,
        'sound': True,
        'start_minimized': False
    }
    
    config_dir = os.path.join('config')
    os.makedirs(config_dir, exist_ok=True)
    
    settings_path = os.path.join(config_dir, 'settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            try:
                user_settings = json.load(f)
                return {**default_settings, **user_settings}
            except:
                return default_settings
    return default_settings

def save_settings(settings):
    config_dir = os.path.join('config')
    os.makedirs(config_dir, exist_ok=True)
    
    settings_path = os.path.join(config_dir, 'settings.json')
    with open(settings_path, 'w') as f:
        json.dump(settings, f, indent=2)