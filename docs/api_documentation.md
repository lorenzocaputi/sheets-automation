# API Documentation

This document provides detailed information about the classes, methods, and functions available in the Google Sheets POD Automation tool.

## Core Classes

### PODAutomation

The main class that orchestrates the entire automation process.

```python
class PODAutomation:
    """Main class for Print On Demand Google Sheets automation"""
```

#### Constructor

```python
def __init__(self, config: Optional[Config] = None)
```

**Parameters:**
- `config` (Config, optional): Configuration object. If None, uses default configuration.

**Example:**
```python
from config.settings import Config
from src.main import PODAutomation

config = Config({'google_account': 'user@example.com'})
automation = PODAutomation(config)
```

#### Methods

##### create_pod_spreadsheet

```python
def create_pod_spreadsheet(self, niche: str, broad_niche: str, list_name: str) -> str
```

Creates a complete POD spreadsheet with APOD and FU worksheets.

**Parameters:**
- `niche` (str): The specific niche phrase (e.g., "i like cats and maybe 3 people")
- `broad_niche` (str): The broad category (e.g., "cats")  
- `list_name` (str): Name of the list to use from POD-lists (e.g., "hobbies")

**Returns:**
- `str`: URL of the created spreadsheet

**Raises:**
- `ValueError`: If input parameters are invalid
- `Exception`: If spreadsheet creation fails

**Example:**
```python
url = automation.create_pod_spreadsheet(
    niche="i love coffee and hate mornings",
    broad_niche="coffee",
    list_name="drinks"
)
```

---

### SheetsManager

Handles all Google Sheets API operations including authentication and data manipulation.

```python
class SheetsManager:
    """Manages Google Sheets operations including authentication and data manipulation"""
```

#### Constructor

```python
def __init__(self, config: Config)
```

**Parameters:**
- `config` (Config): Configuration object containing credentials and settings

#### Methods

##### create_spreadsheet

```python
def create_spreadsheet(self, title: str) -> gspread.Spreadsheet
```

Creates a new Google Spreadsheet and shares it with the configured account.

**Parameters:**
- `title` (str): Title of the spreadsheet

**Returns:**
- `gspread.Spreadsheet`: Created spreadsheet object

##### setup_apod_worksheet

```python
def setup_apod_worksheet(self, spreadsheet: gspread.Spreadsheet, data: List[List[str]])
```

Sets up the APOD (Artwork Print On Demand) worksheet with headers and data.

**Parameters:**
- `spreadsheet`: The spreadsheet to modify
- `data`: List of rows to add to the worksheet

##### setup_fu_worksheet

```python
def setup_fu_worksheet(self, spreadsheet: gspread.Spreadsheet, data: List[List[str]])
```

Sets up the FU (Flying Upload) worksheet with headers and data.

**Parameters:**
- `spreadsheet`: The spreadsheet to modify
- `data`: List of rows to add to the worksheet

##### get_pod_list_data

```python
def get_pod_list_data(self, list_name: str) -> List[List[str]]
```

Retrieves data from POD lists spreadsheet.

**Parameters:**
- `list_name` (str): Name of the worksheet to read from

**Returns:**
- `List[List[str]]`: Data from the specified worksheet

##### get_worksheet_data

```python
def get_worksheet_data(self, spreadsheet: gspread.Spreadsheet, worksheet_name: str, cell_range: str) -> List[List[str]]
```

Gets data from a specific worksheet and range.

**Parameters:**
- `spreadsheet`: The spreadsheet to read from
- `worksheet_name` (str): Name of the worksheet
- `cell_range` (str): Cell range to read (e.g., 'A2:B61')

**Returns:**
- `List[List[str]]`: Data from the specified range

---

### DataProcessor

Handles data transformation and processing for POD automation.

```python
class DataProcessor:
    """Processes and transforms data for Google Sheets automation"""
```

#### Constructor

```python
def __init__(self, config: Config)
```

**Parameters:**
- `config` (Config): Configuration object

#### Methods

##### process_apod_data

```python
def process_apod_data(self, pod_list_data: List[List[str]], niche: str) -> List[List[str]]
```

Processes data for APOD worksheet by appending niche to filenames.

**Parameters:**
- `pod_list_data`: Raw data from POD lists
- `niche` (str): The niche phrase to append to file names

**Returns:**
- `List[List[str]]`: Processed data ready for APOD worksheet

##### process_fu_data

```python
def process_fu_data(self, file_names: List[List[str]], var1_values: List[List[str]], niche: str, broad_niche: str) -> List[List[str]]
```

Processes data for FU (Flying Upload) worksheet.

**Parameters:**
- `file_names`: List of file names from APOD worksheet
- `var1_values`: List of VAR1 values from APOD worksheet  
- `niche` (str): The niche phrase
- `broad_niche` (str): The broad niche category

**Returns:**
- `List[List[str]]`: Processed data ready for FU worksheet

##### validate_niche_parameters

```python
def validate_niche_parameters(self, niche: str, broad_niche: str, list_name: str) -> Tuple[bool, str]
```

Validates input parameters for niche processing.

**Parameters:**
- `niche` (str): The specific niche phrase
- `broad_niche` (str): The broad category
- `list_name` (str): The list name to use from POD lists

**Returns:**
- `Tuple[bool, str]`: (is_valid, error_message)

##### generate_spreadsheet_title

```python
def generate_spreadsheet_title(self, niche: str) -> str
```

Generates a standardized spreadsheet title.

**Parameters:**
- `niche` (str): The niche phrase

**Returns:**
- `str`: Formatted spreadsheet title (format: "AUTOMATION.{niche}")

---

### Config

Configuration management class that handles all settings and credentials.

```python
class Config:
    """Configuration class for the automation tool"""
```

#### Constructor

```python
def __init__(self, config_dict: Dict = None)
```

**Parameters:**
- `config_dict` (Dict, optional): Dictionary of configuration overrides

#### Properties

##### credentials_file
```python
@property
def credentials_file(self) -> str
```
Path to Google Service Account JSON file.

##### google_account
```python
@property  
def google_account(self) -> str
```
Email address to share created spreadsheets with.

##### scope
```python
@property
def scope(self) -> List[str]
```
List of Google API scopes required for operation.

##### pod_lists_sheet
```python
@property
def pod_lists_sheet(self) -> str
```
Name of the reference spreadsheet containing POD lists.

##### standard_description
```python
@property
def standard_description(self) -> str
```
Template string for product descriptions.

#### Methods

##### get
```python
def get(self, key: str, default=None)
```

Gets a configuration value with optional default.

**Parameters:**
- `key` (str): Configuration key
- `default`: Default value if key not found

**Returns:**
- Configuration value or default

##### update
```python
def update(self, key: str, value)
```

Updates a configuration value.

**Parameters:**
- `key` (str): Configuration key
- `value`: New value

---

## Constants

### Sheet Headers

```python
# APOD worksheet headers
APOD_HEADERS = ['VAR1', 'File Name']

# FU worksheet headers  
FU_HEADERS = ['Image Path', 'Language', 'Title', 'Description', 'Tags', 'Type', 'Color']
```

### Worksheet Names

```python
APOD_WORKSHEET = 'Sheet1'  # Default first sheet
FU_WORKSHEET = 'FU'        # Flying Upload worksheet
```

### Default Values

```python
DEFAULT_ROWS_COUNT = 60           # Default number of rows to process
DEFAULT_WORKSHEET_SIZE = 1000     # Default worksheet dimensions
IMAGE_EXTENSION = '.png'          # Default image file extension
```

---

## Configuration Options

### Required Settings

- `credentials_file`: Path to Google Service Account JSON credentials
- `google_account`: Email address to share spreadsheets with

### Optional Settings

- `scope`: Google API scopes (defaults to Sheets and Drive)
- `pod_lists_sheet`: Name of POD lists spreadsheet (default: "POD-lists")
- `standard_description`: Product description template
- `default_language`: Language code (default: "EN")
- `default_type`: Target demographic (default: "man, woman youth")
- `default_color`: Design color (default: "black")
- `default_tags`: Categorization tags (default: "WEB SCRAPING")

---

## Error Handling

The API uses comprehensive error handling with specific exception types:

### Common Exceptions

- `ValueError`: Invalid input parameters
- `Exception`: General operation failures (authentication, API calls, etc.)

### Error Messages

All error messages are logged with appropriate severity levels:
- `INFO`: Successful operations
- `ERROR`: Operation failures
- `DEBUG`: Detailed execution information

---

## Usage Examples

### Basic Usage

```python
from config.settings import Config
from src.main import PODAutomation

# Create configuration
config = Config({
    'google_account': 'user@example.com',
    'credentials_file': 'credentials.json'
})

# Initialize automation  
automation = PODAutomation(config)

# Create spreadsheet
url = automation.create_pod_spreadsheet(
    niche="i love hiking", 
    broad_niche="hiking",
    list_name="hobbies"
)
```

### Advanced Configuration

```python
# Custom configuration with all options
config = Config({
    'google_account': 'business@company.com',
    'credentials_file': 'service-account.json',
    'standard_description': 'Premium {broad_niche} design for enthusiasts!',
    'default_language': 'EN',
    'default_type': 'premium quality',
    'default_color': 'navy blue'
})
```

### Error Handling

```python
try:
    url = automation.create_pod_spreadsheet(niche, broad_niche, list_name)
    print(f"Success: {url}")
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Operation failed: {e}")
```

---

## Integration Notes

### Thread Safety

The classes are not thread-safe. Create separate instances for concurrent operations.

### Rate Limits

Google Sheets API has rate limits. The tool includes basic error handling but may require backoff strategies for high-volume usage.

### Memory Usage

Processing large datasets may require additional memory. Monitor resource usage for large POD list files.
