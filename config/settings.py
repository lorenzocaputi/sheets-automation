"""
Configuration settings for Google Sheets Automation
"""
import os
from typing import List, Dict

# Default configuration
DEFAULT_CONFIG = {
    'credentials_file': '../sheetsAPI.json',
    'google_account': 'your-email@gmail.com',
    'scope': [
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ],
    'pod_lists_sheet': 'POD-lists',
    'standard_description': 'funny {broad_niche} shirt. Perfect birthday gift for dad, grandpa or a good friend.',
    'default_language': 'EN',
    'default_type': 'man, woman youth',
    'default_color': 'black',
    'default_tags': 'WEB SCRAPING'
}

class Config:
    """Configuration class for the automation tool"""
    
    def __init__(self, config_dict: Dict = None):
        self.config = DEFAULT_CONFIG.copy()
        if config_dict:
            self.config.update(config_dict)
    
    @property
    def credentials_file(self) -> str:
        return self.config['credentials_file']
    
    @property
    def google_account(self) -> str:
        return self.config['google_account']
    
    @property
    def scope(self) -> List[str]:
        return self.config['scope']
    
    @property
    def pod_lists_sheet(self) -> str:
        return self.config['pod_lists_sheet']
    
    @property
    def standard_description(self) -> str:
        return self.config['standard_description']
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def update(self, key: str, value):
        self.config[key] = value
