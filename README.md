# Google Sheets POD Automation

A Python automation tool for generating Google Sheets files for Print On Demand (POD) designs. This tool creates structured spreadsheets with APOD (Artwork Print On Demand) and FU (Flying Upload) worksheets, designed to streamline the POD workflow.

## Features

- **Automated Spreadsheet Creation**: Creates Google Sheets with predefined templates
- **APOD Worksheet**: Generates artwork metadata with customizable niche targeting
- **FU Worksheet**: Creates upload-ready data for POD platforms
- **Configurable Templates**: Customizable descriptions, tags, and design parameters
- **Error Handling**: Comprehensive logging and error management
- **Modular Design**: Clean, maintainable code structure

## Prerequisites

- Python 3.7+
- Google Cloud Project with Sheets API enabled
- Service Account credentials (JSON file)
- Access to a "POD-lists" Google Spreadsheet with reference data

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lorenzocaputi/sheets-automation.git
   cd sheets-automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Sheets API**:
   - Create a Google Cloud Project
   - Enable the Google Sheets API
   - Create a Service Account and download the JSON credentials
   - Place the credentials file in your project directory
   - Share your "POD-lists" spreadsheet with the service account email

## Configuration

Create or modify the configuration in `src/main.py`:

```python
custom_config = Config({
    'google_account': 'your-email@gmail.com',
    'credentials_file': 'path/to/your/credentials.json'
})
```

### Available Configuration Options

- `credentials_file`: Path to Google Service Account JSON file
- `google_account`: Email to share created spreadsheets with
- `pod_lists_sheet`: Name of the reference spreadsheet (default: "POD-lists")
- `standard_description`: Template for product descriptions
- `default_language`: Default language code (default: "EN")
- `default_type`: Target demographic (default: "man, woman youth")
- `default_color`: Default design color (default: "black")

## Usage

### Basic Usage

```python
from config.settings import Config
from src.main import PODAutomation

# Configure the tool
config = Config({
    'google_account': 'your-email@gmail.com',
    'credentials_file': 'sheetsAPI.json'
})

# Initialize automation
automation = PODAutomation(config)

# Create a POD spreadsheet
spreadsheet_url = automation.create_pod_spreadsheet(
    niche="i like cats and maybe 3 people",
    broad_niche="cats", 
    list_name="hobbies"
)

print(f"Spreadsheet URL: {spreadsheet_url}")
```

### Running the Example

The main script includes an example that you can run directly:

```bash
python src/main.py
```

### Available List Names

The `list_name` parameter should match worksheets in your "POD-lists" spreadsheet:
- `hobbies`
- `jobs` 
- `years`
- `drinks`

## Project Structure

```
sheets-automation/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── setup.py                 # Package setup
├── .gitignore              # Git ignore rules
├── automation.py           # Original script (deprecated)
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration management
├── src/
│   ├── __init__.py
│   ├── main.py            # Main entry point and PODAutomation class
│   ├── sheets_manager.py   # Google Sheets API operations
│   ├── data_processor.py   # Data transformation logic
│   └── constants.py        # Constants and templates
├── examples/
│   ├── example_config.py   # Configuration examples
│   └── sample_usage.py     # Usage examples
├── docs/
│   ├── setup_guide.md      # Detailed setup instructions
│   └── api_documentation.md # API reference
└── tests/
    ├── __init__.py
    └── test_sheets_manager.py # Unit tests
```

## Generated Spreadsheet Structure

### APOD Worksheet
- **VAR1**: Variable content from POD lists
- **File Name**: Generated filename with niche

### FU Worksheet  
- **Image Path**: PNG filename for upload
- **Language**: Content language (default: EN)
- **Title**: Product title with niche and variable
- **Description**: Product description template
- **Tags**: Categorization tags
- **Type**: Target demographic
- **Color**: Design color

## Error Handling

The tool includes comprehensive error handling and logging:

- **Authentication errors**: Issues with Google API credentials
- **Spreadsheet errors**: Problems creating or accessing sheets
- **Data processing errors**: Issues with data transformation
- **Validation errors**: Invalid input parameters

Logs are output to console with timestamps and severity levels.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please:
- Open an issue on GitHub
- Check the documentation in the `docs/` folder
- Review the examples in the `examples/` folder

## Changelog

### v1.0.0
- Initial release with modular architecture
- APOD and FU worksheet support
- Configurable templates and settings
- Comprehensive error handling and logging
