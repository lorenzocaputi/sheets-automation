"""
Google Sheets Manager - Handles authentication and sheet operations
"""
import logging
from typing import List, Dict, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import Config
from src.constants import APOD_HEADERS, FU_HEADERS, FU_WORKSHEET, DEFAULT_WORKSHEET_SIZE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SheetsManager:
    """Manages Google Sheets operations including authentication and data manipulation"""
    
    def __init__(self, config: Config):
        """
        Initialize the SheetsManager with configuration
        
        Args:
            config (Config): Configuration object containing credentials and settings
        """
        self.config = config
        self.client = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.config.credentials_file, 
                scopes=self.config.scope
            )
            self.client = gspread.authorize(creds)
            logger.info("Successfully authenticated with Google Sheets API")
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets API: {e}")
            raise
    
    def create_spreadsheet(self, title: str) -> gspread.Spreadsheet:
        """
        Create a new Google Spreadsheet
        
        Args:
            title (str): Title of the spreadsheet
            
        Returns:
            gspread.Spreadsheet: Created spreadsheet object
        """
        try:
            spreadsheet = self.client.create(title)
            spreadsheet.share(self.config.google_account, perm_type='user', role='writer')
            logger.info(f"Created spreadsheet: {title}")
            return spreadsheet
        except Exception as e:
            logger.error(f"Failed to create spreadsheet '{title}': {e}")
            raise
    
    def setup_apod_worksheet(self, spreadsheet: gspread.Spreadsheet, data: List[List[str]]):
        """
        Setup the APOD (Artwork Print On Demand) worksheet
        
        Args:
            spreadsheet: The spreadsheet to modify
            data: List of rows to add to the worksheet
        """
        try:
            worksheet = spreadsheet.sheet1
            worksheet.append_row(APOD_HEADERS)
            worksheet.append_rows(data)
            logger.info("APOD worksheet setup completed")
        except Exception as e:
            logger.error(f"Failed to setup APOD worksheet: {e}")
            raise
    
    def setup_fu_worksheet(self, spreadsheet: gspread.Spreadsheet, data: List[List[str]]):
        """
        Setup the FU (Flying Upload) worksheet
        
        Args:
            spreadsheet: The spreadsheet to modify
            data: List of rows to add to the worksheet
        """
        try:
            fu_worksheet = spreadsheet.add_worksheet(
                FU_WORKSHEET, 
                DEFAULT_WORKSHEET_SIZE, 
                DEFAULT_WORKSHEET_SIZE
            )
            fu_worksheet.append_row(FU_HEADERS)
            fu_worksheet.append_rows(data)
            logger.info("FU worksheet setup completed")
        except Exception as e:
            logger.error(f"Failed to setup FU worksheet: {e}")
            raise
    
    def get_pod_list_data(self, list_name: str) -> List[List[str]]:
        """
        Get data from POD lists spreadsheet
        
        Args:
            list_name (str): Name of the worksheet to read from
            
        Returns:
            List[List[str]]: Data from the specified worksheet
        """
        try:
            list_sheet = self.client.open(self.config.pod_lists_sheet).worksheet(list_name)
            data = list_sheet.get_all_values()
            logger.info(f"Retrieved {len(data)} rows from '{list_name}' list")
            return data
        except Exception as e:
            logger.error(f"Failed to get POD list data from '{list_name}': {e}")
            raise
    
    def get_worksheet_data(self, spreadsheet: gspread.Spreadsheet, 
                          worksheet_name: str, cell_range: str) -> List[List[str]]:
        """
        Get data from a specific worksheet and range
        
        Args:
            spreadsheet: The spreadsheet to read from
            worksheet_name: Name of the worksheet
            cell_range: Cell range to read (e.g., 'A2:B61')
            
        Returns:
            List[List[str]]: Data from the specified range
        """
        try:
            if worksheet_name == 'Sheet1':
                worksheet = spreadsheet.sheet1
            else:
                worksheet = spreadsheet.worksheet(worksheet_name)
            
            data = worksheet.get_values(cell_range)
            logger.info(f"Retrieved data from {worksheet_name} range {cell_range}")
            return data
        except Exception as e:
            logger.error(f"Failed to get data from {worksheet_name} range {cell_range}: {e}")
            raise
