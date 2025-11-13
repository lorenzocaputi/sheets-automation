"""
Main entry point for Google Sheets POD Automation
"""
import logging
import sys
from typing import Optional
from config.settings import Config
from src.sheets_manager import SheetsManager
from src.data_processor import DataProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PODAutomation:
    """Main class for Print On Demand Google Sheets automation"""
    
    def __init__(self, config: Optional[Config] = None):
        """
        Initialize the POD Automation system
        
        Args:
            config: Optional configuration object. If None, uses default config.
        """
        self.config = config or Config()
        self.sheets_manager = SheetsManager(self.config)
        self.data_processor = DataProcessor(self.config)
    
    def create_pod_spreadsheet(self, niche: str, broad_niche: str, list_name: str) -> str:
        """
        Create a complete POD spreadsheet with APOD and FU worksheets
        
        Args:
            niche: The specific niche phrase (e.g., "i like cats and maybe 3 people")
            broad_niche: The broad category (e.g., "cats")
            list_name: Name of the list to use from POD-lists (e.g., "hobbies")
            
        Returns:
            str: URL or ID of the created spreadsheet
        """
        # Validate input parameters
        is_valid, error_msg = self.data_processor.validate_niche_parameters(
            niche, broad_niche, list_name
        )
        if not is_valid:
            raise ValueError(error_msg)
        
        logger.info(f"Starting POD automation for niche: '{niche}'")
        
        try:
            # Step 1: Create the spreadsheet
            title = self.data_processor.generate_spreadsheet_title(niche)
            spreadsheet = self.sheets_manager.create_spreadsheet(title)
            
            # Step 2: Get source data from POD lists
            pod_list_data = self.sheets_manager.get_pod_list_data(list_name)
            
            # Step 3: Process and setup APOD worksheet
            apod_data = self.data_processor.process_apod_data(pod_list_data, niche)
            self.sheets_manager.setup_apod_worksheet(spreadsheet, apod_data)
            
            # Step 4: Get data from APOD worksheet for FU processing
            file_names = self.sheets_manager.get_worksheet_data(spreadsheet, 'Sheet1', 'b2:b61')
            var1_values = self.sheets_manager.get_worksheet_data(spreadsheet, 'Sheet1', 'a2:a61')
            
            # Step 5: Process and setup FU worksheet
            fu_data = self.data_processor.process_fu_data(
                file_names, var1_values, niche, broad_niche
            )
            self.sheets_manager.setup_fu_worksheet(spreadsheet, fu_data)
            
            logger.info(f"Successfully created POD spreadsheet: {title}")
            return spreadsheet.url
            
        except Exception as e:
            logger.error(f"Failed to create POD spreadsheet: {e}")
            raise


def main():
    """Main function to run the automation"""
    try:
        # Example configuration - users should modify these values
        custom_config = Config({
            'google_account': 'lorenzo.caputi@liceotasso.edu.it',  # Update with your email
            'credentials_file': '../sheetsAPI.json'  # Update path if needed
        })
        
        # Initialize automation
        automation = PODAutomation(custom_config)
        
        # Example usage - modify these values for your niche
        niche = 'i like cats and maybe 3 people'
        broad_niche = 'cats'
        list_name = 'hobbies'  # Available: hobbies, jobs, years, drinks
        
        # Create the spreadsheet
        spreadsheet_url = automation.create_pod_spreadsheet(niche, broad_niche, list_name)
        
        print(f"POD spreadsheet created successfully!")
        print(f"Spreadsheet URL: {spreadsheet_url}")
        print(f"Shared with: {custom_config.google_account}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
