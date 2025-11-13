"""
Data Processor - Handles data transformation and processing for POD automation
"""
import logging
from typing import List, Dict, Tuple
from config.settings import Config
from src.constants import DEFAULT_ROWS_COUNT, IMAGE_EXTENSION

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes and transforms data for Google Sheets automation"""
    
    def __init__(self, config: Config):
        """
        Initialize the DataProcessor with configuration
        
        Args:
            config (Config): Configuration object
        """
        self.config = config
    
    def process_apod_data(self, pod_list_data: List[List[str]], niche: str) -> List[List[str]]:
        """
        Process data for APOD worksheet
        
        Args:
            pod_list_data: Raw data from POD lists
            niche: The niche phrase to append to file names
            
        Returns:
            List[List[str]]: Processed data ready for APOD worksheet
        """
        try:
            processed_data = []
            for row in pod_list_data:
                if row:  # Skip empty rows
                    new_row = row.copy()
                    new_row.append(f"{row[0]} {niche}")
                    processed_data.append(new_row)
            
            logger.info(f"Processed {len(processed_data)} rows for APOD worksheet")
            return processed_data
        except Exception as e:
            logger.error(f"Failed to process APOD data: {e}")
            raise
    
    def process_fu_data(self, file_names: List[List[str]], var1_values: List[List[str]], 
                       niche: str, broad_niche: str) -> List[List[str]]:
        """
        Process data for FU (Flying Upload) worksheet
        
        Args:
            file_names: List of file names from APOD worksheet
            var1_values: List of VAR1 values from APOD worksheet
            niche: The niche phrase
            broad_niche: The broad niche category
            
        Returns:
            List[List[str]]: Processed data ready for FU worksheet
        """
        try:
            processed_data = []
            standard_description = self.config.standard_description.format(broad_niche=broad_niche)
            
            rows_to_process = min(len(file_names), len(var1_values), DEFAULT_ROWS_COUNT)
            
            for i in range(rows_to_process):
                if file_names[i] and var1_values[i]:
                    file_name = file_names[i][0]
                    var1 = var1_values[i][0]
                    
                    row = [
                        f"{file_name}{IMAGE_EXTENSION}",  # Image Path
                        self.config.get('default_language', 'EN'),  # Language
                        f"{niche} funny {var1}",  # Title
                        f"{var1} {standard_description}",  # Description
                        self.config.get('default_tags', 'WEB SCRAPING'),  # Tags
                        self.config.get('default_type', 'man, woman youth'),  # Type
                        self.config.get('default_color', 'black')  # Color
                    ]
                    processed_data.append(row)
            
            logger.info(f"Processed {len(processed_data)} rows for FU worksheet")
            return processed_data
        except Exception as e:
            logger.error(f"Failed to process FU data: {e}")
            raise
    
    def validate_niche_parameters(self, niche: str, broad_niche: str, 
                                 list_name: str) -> Tuple[bool, str]:
        """
        Validate the input parameters for niche processing
        
        Args:
            niche: The specific niche phrase
            broad_niche: The broad category
            list_name: The list name to use from POD lists
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not niche or not niche.strip():
            return False, "Niche cannot be empty"
        
        if not broad_niche or not broad_niche.strip():
            return False, "Broad niche cannot be empty"
        
        if not list_name or not list_name.strip():
            return False, "List name cannot be empty"
        
        return True, ""
    
    def generate_spreadsheet_title(self, niche: str) -> str:
        """
        Generate a standardized spreadsheet title
        
        Args:
            niche: The niche phrase
            
        Returns:
            str: Formatted spreadsheet title
        """
        return f"AUTOMATION.{niche}"
