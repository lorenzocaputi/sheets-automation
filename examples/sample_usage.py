"""
Sample usage examples for Google Sheets POD Automation

This file demonstrates various ways to use the POD automation tool
with different configurations and parameters.
"""

import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import Config
from src.main import PODAutomation


def example_1_basic_usage():
    """
    Example 1: Basic usage with default settings
    """
    print("=== Example 1: Basic Usage ===")
    
    # Configure with your credentials
    config = Config({
        'google_account': 'your-email@gmail.com',  # Replace with your email
        'credentials_file': 'sheetsAPI.json'       # Replace with your credentials file
    })
    
    # Initialize automation
    automation = PODAutomation(config)
    
    # Create a cat-themed spreadsheet
    try:
        spreadsheet_url = automation.create_pod_spreadsheet(
            niche="i like cats and maybe 3 people",
            broad_niche="cats",
            list_name="hobbies"
        )
        print(f"Spreadsheet created: {spreadsheet_url}")
    except Exception as e:
        print(f"Error: {e}")


def example_2_multiple_niches():
    """
    Example 2: Creating spreadsheets for multiple niches
    """
    print("\n=== Example 2: Multiple Niches ===")
    
    config = Config({
        'google_account': 'your-email@gmail.com',
        'credentials_file': 'sheetsAPI.json'
    })
    
    automation = PODAutomation(config)
    
    # Define multiple niche combinations
    niches = [
        {
            "niche": "i love coffee and hate mornings",
            "broad_niche": "coffee",
            "list_name": "drinks"
        },
        {
            "niche": "i'm a teacher and i need wine",
            "broad_niche": "teacher",
            "list_name": "jobs"
        },
        {
            "niche": "born in 1985 and still awesome",
            "broad_niche": "1985",
            "list_name": "years"
        }
    ]
    
    # Create spreadsheets for each niche
    for niche_data in niches:
        try:
            print(f"Creating spreadsheet for: {niche_data['niche']}")
            spreadsheet_url = automation.create_pod_spreadsheet(**niche_data)
            print(f"Created: {spreadsheet_url}")
        except Exception as e:
            print(f"Failed for '{niche_data['niche']}': {e}")


def example_3_custom_configuration():
    """
    Example 3: Using custom configuration and templates
    """
    print("\n=== Example 3: Custom Configuration ===")
    
    # Custom configuration with modified templates
    custom_config = Config({
        'google_account': 'your-email@gmail.com',
        'credentials_file': 'sheetsAPI.json',
        'standard_description': 'Premium {broad_niche} design. Perfect gift for {broad_niche} enthusiasts and lovers!',
        'default_language': 'EN',
        'default_type': 'premium quality',
        'default_color': 'navy blue',
        'default_tags': 'PREMIUM, CUSTOM_DESIGN'
    })
    
    automation = PODAutomation(custom_config)
    
    try:
        spreadsheet_url = automation.create_pod_spreadsheet(
            niche="i love hiking and fresh air",
            broad_niche="hiking",
            list_name="hobbies"
        )
        print(f"Custom spreadsheet created: {spreadsheet_url}")
    except Exception as e:
        print(f"Error: {e}")


def example_4_error_handling():
    """
    Example 4: Demonstrating error handling
    """
    print("\n=== Example 4: Error Handling ===")
    
    config = Config({
        'google_account': 'your-email@gmail.com',
        'credentials_file': 'sheetsAPI.json'
    })
    
    automation = PODAutomation(config)
    
    # Test with invalid parameters
    test_cases = [
        {
            "name": "Empty niche",
            "params": {
                "niche": "",
                "broad_niche": "cats",
                "list_name": "hobbies"
            }
        },
        {
            "name": "Empty broad niche",
            "params": {
                "niche": "i love cats",
                "broad_niche": "",
                "list_name": "hobbies"
            }
        },
        {
            "name": "Invalid list name",
            "params": {
                "niche": "i love cats",
                "broad_niche": "cats",
                "list_name": "invalid_list"
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            print(f"Testing: {test_case['name']}")
            automation.create_pod_spreadsheet(**test_case['params'])
            print("Unexpected success")
        except ValueError as e:
            print(f"Validation error caught: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def example_5_batch_processing():
    """
    Example 5: Batch processing with progress tracking
    """
    print("\n=== Example 5: Batch Processing ===")
    
    config = Config({
        'google_account': 'your-email@gmail.com',
        'credentials_file': 'sheetsAPI.json'
    })
    
    automation = PODAutomation(config)
    
    # Batch of gaming-related niches
    gaming_niches = [
        ("i pause my game to be here", "gaming", "hobbies"),
        ("i level up in real life", "gaming", "hobbies"),
        ("respawn point: coffee shop", "gaming", "hobbies"),
    ]
    
    successful_sheets = []
    failed_sheets = []
    
    for i, (niche, broad_niche, list_name) in enumerate(gaming_niches, 1):
        try:
            print(f"[{i}/{len(gaming_niches)}] Processing: {niche}")
            spreadsheet_url = automation.create_pod_spreadsheet(niche, broad_niche, list_name)
            successful_sheets.append({
                'niche': niche,
                'url': spreadsheet_url
            })
            print(f"Success!")
        except Exception as e:
            failed_sheets.append({
                'niche': niche,
                'error': str(e)
            })
            print(f"Failed: {e}")
    
    # Summary
    print(f"\nBatch Processing Summary:")
    print(f"Successful: {len(successful_sheets)}")
    print(f"Failed: {len(failed_sheets)}")
    
    if successful_sheets:
        print("\nSuccessful spreadsheets:")
        for sheet in successful_sheets:
            print(f"  - {sheet['niche']}: {sheet['url']}")
    
    if failed_sheets:
        print("\nFailed attempts:")
        for sheet in failed_sheets:
            print(f"  - {sheet['niche']}: {sheet['error']}")


if __name__ == "__main__":
    print("Google Sheets POD Automation - Usage Examples")
    print("=" * 50)
    
    # Note: These examples require valid credentials and POD-lists spreadsheet
    print("Note: Update the configuration with your actual Google account and credentials file before running!")
    print()
    
    # Run examples (uncomment the ones you want to test)
    
    # example_1_basic_usage()
    # example_2_multiple_niches() 
    # example_3_custom_configuration()
    # example_4_error_handling()
    # example_5_batch_processing()
    
    print("\nUncomment the example functions above to run them!")
    print("Make sure to update the configuration with your actual credentials first.")
