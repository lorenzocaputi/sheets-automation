"""
Unit tests for Google Sheets Manager

These tests demonstrate the testing structure and provide basic test cases
for the SheetsManager class functionality.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from src.sheets_manager import SheetsManager
from src.constants import APOD_HEADERS, FU_HEADERS


class TestSheetsManager(unittest.TestCase):
    """Test cases for SheetsManager class"""
    
    def setUp(self):
        """Set up test configuration"""
        self.test_config = Config({
            'google_account': 'test@example.com',
            'credentials_file': 'test_credentials.json',
            'scope': ['test_scope'],
            'pod_lists_sheet': 'test-pod-lists'
        })
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    @patch('src.sheets_manager.gspread')
    def test_authentication_success(self, mock_gspread, mock_credentials):
        """Test successful authentication"""
        # Mock the authentication process
        mock_creds = Mock()
        mock_credentials.from_json_keyfile_name.return_value = mock_creds
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        
        # Create SheetsManager instance
        manager = SheetsManager(self.test_config)
        
        # Verify authentication was called correctly
        mock_credentials.from_json_keyfile_name.assert_called_once_with(
            self.test_config.credentials_file,
            scopes=self.test_config.scope
        )
        mock_gspread.authorize.assert_called_once_with(mock_creds)
        self.assertEqual(manager.client, mock_client)
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    def test_authentication_failure(self, mock_credentials):
        """Test authentication failure handling"""
        # Mock authentication failure
        mock_credentials.from_json_keyfile_name.side_effect = Exception("Authentication failed")
        
        # Verify exception is raised
        with self.assertRaises(Exception) as context:
            SheetsManager(self.test_config)
        
        self.assertIn("Authentication failed", str(context.exception))
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    @patch('src.sheets_manager.gspread')
    def test_create_spreadsheet_success(self, mock_gspread, mock_credentials):
        """Test successful spreadsheet creation"""
        # Setup mocks
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        mock_spreadsheet = Mock()
        mock_client.create.return_value = mock_spreadsheet
        
        # Create manager and test spreadsheet creation
        manager = SheetsManager(self.test_config)
        title = "Test Spreadsheet"
        result = manager.create_spreadsheet(title)
        
        # Verify calls
        mock_client.create.assert_called_once_with(title)
        mock_spreadsheet.share.assert_called_once_with(
            self.test_config.google_account, 
            perm_type='user', 
            role='writer'
        )
        self.assertEqual(result, mock_spreadsheet)
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    @patch('src.sheets_manager.gspread')
    def test_setup_apod_worksheet(self, mock_gspread, mock_credentials):
        """Test APOD worksheet setup"""
        # Setup mocks
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        mock_spreadsheet = Mock()
        mock_worksheet = Mock()
        mock_spreadsheet.sheet1 = mock_worksheet
        
        # Test data
        test_data = [['var1', 'filename1'], ['var2', 'filename2']]
        
        # Create manager and test worksheet setup
        manager = SheetsManager(self.test_config)
        manager.setup_apod_worksheet(mock_spreadsheet, test_data)
        
        # Verify calls
        mock_worksheet.append_row.assert_called_once_with(APOD_HEADERS)
        mock_worksheet.append_rows.assert_called_once_with(test_data)
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    @patch('src.sheets_manager.gspread')
    def test_get_pod_list_data(self, mock_gspread, mock_credentials):
        """Test getting POD list data"""
        # Setup mocks
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        mock_sheet = Mock()
        mock_worksheet = Mock()
        mock_sheet.worksheet.return_value = mock_worksheet
        mock_client.open.return_value = mock_sheet
        
        test_data = [['item1'], ['item2'], ['item3']]
        mock_worksheet.get_all_values.return_value = test_data
        
        # Create manager and test data retrieval
        manager = SheetsManager(self.test_config)
        result = manager.get_pod_list_data('test_list')
        
        # Verify calls and result
        mock_client.open.assert_called_once_with(self.test_config.pod_lists_sheet)
        mock_sheet.worksheet.assert_called_once_with('test_list')
        mock_worksheet.get_all_values.assert_called_once()
        self.assertEqual(result, test_data)
    
    @patch('src.sheets_manager.ServiceAccountCredentials')
    @patch('src.sheets_manager.gspread')
    def test_get_worksheet_data(self, mock_gspread, mock_credentials):
        """Test getting worksheet data from specific range"""
        # Setup mocks
        mock_client = Mock()
        mock_gspread.authorize.return_value = mock_client
        mock_spreadsheet = Mock()
        mock_worksheet = Mock()
        mock_spreadsheet.sheet1 = mock_worksheet
        
        test_data = [['a1'], ['a2'], ['a3']]
        mock_worksheet.get_values.return_value = test_data
        
        # Create manager and test data retrieval
        manager = SheetsManager(self.test_config)
        result = manager.get_worksheet_data(mock_spreadsheet, 'Sheet1', 'A1:A3')
        
        # Verify calls and result
        mock_worksheet.get_values.assert_called_once_with('A1:A3')
        self.assertEqual(result, test_data)


class TestConfigIntegration(unittest.TestCase):
    """Test the integration between Config and SheetsManager"""
    
    def test_config_properties(self):
        """Test that config properties are accessible"""
        config = Config({
            'google_account': 'test@example.com',
            'credentials_file': 'test.json'
        })
        
        self.assertEqual(config.google_account, 'test@example.com')
        self.assertEqual(config.credentials_file, 'test.json')
        self.assertIsInstance(config.scope, list)
    
    def test_config_defaults(self):
        """Test that default configuration values are set"""
        config = Config()
        
        self.assertIsNotNone(config.scope)
        self.assertIsNotNone(config.pod_lists_sheet)
        self.assertIsNotNone(config.standard_description)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
