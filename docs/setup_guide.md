# Google Sheets POD Automation - Setup Guide

This guide will walk you through the complete setup process for the Google Sheets POD Automation tool.

## Prerequisites

- Python 3.7 or higher
- Google account
- Google Cloud Platform account (free tier is sufficient)

## Step 1: Clone and Install

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lorenzocaputi/sheets-automation.git
   cd sheets-automation
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Google Cloud Setup

### Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note your project ID for later use

### Enable Required APIs

1. In the Google Cloud Console, navigate to **APIs & Services > Library**
2. Search for and enable the following APIs:
   - **Google Sheets API**
   - **Google Drive API**

### Create Service Account Credentials

1. Navigate to **APIs & Services > Credentials**
2. Click **Create Credentials > Service Account**
3. Fill in the service account details:
   - Name: `sheets-automation-service`
   - Description: `Service account for POD sheets automation`
4. Click **Create and Continue**
5. Skip the optional role assignment (click **Continue**)
6. Click **Done**

### Generate and Download Key File

1. In the **Credentials** page, find your newly created service account
2. Click on the service account email
3. Go to the **Keys** tab
4. Click **Add Key > Create New Key**
5. Select **JSON** format and click **Create**
6. Download the JSON file and save it as `sheetsAPI.json` in your project root

## Step 3: Create POD Lists Spreadsheet

1. **Create a new Google Spreadsheet** and name it `POD-lists`

2. **Create the following worksheets** with sample data:

### Worksheet: "hobbies"
```
reading
gaming
hiking
cooking
photography
gardening
```

### Worksheet: "jobs"
```
teacher
nurse
engineer
chef
artist
developer
```

### Worksheet: "years"
```
1980
1985
1990
1995
2000
2005
```

### Worksheet: "drinks"
```
coffee
tea
wine
beer
juice
water
```

3. **Share the spreadsheet** with your service account:
   - Click **Share** in the top-right corner
   - Add your service account email (found in the JSON credentials file)
   - Give **Editor** permissions
   - Click **Send**

## Step 4: Configuration

1. **Update the configuration** in `src/main.py`:
   ```python
   custom_config = Config({
       'google_account': 'your-actual-email@gmail.com',
       'credentials_file': 'sheetsAPI.json'  # or path to your JSON file
   })
   ```

2. **Verify your setup** by running the test:
   ```bash
   python src/main.py
   ```

## Step 5: Running Tests

Run the included tests to verify everything is working:

```bash
python -m pytest tests/ -v
```

Or run individual test files:

```bash
python tests/test_sheets_manager.py
```

## Troubleshooting

### Common Issues

**1. Authentication Error: "File not found"**
- Ensure the `sheetsAPI.json` file is in the correct location
- Check the file path in your configuration

**2. Permission Error: "The caller does not have permission"**
- Verify the service account email has access to the POD-lists spreadsheet
- Check that both Google Sheets API and Drive API are enabled

**3. Spreadsheet Not Found: "POD-lists"**
- Ensure the POD-lists spreadsheet exists
- Verify it's shared with your service account
- Check the exact spelling and case sensitivity

**4. Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using Python 3.7 or higher: `python --version`

### Debug Mode

Enable debug logging by modifying the logging level in `src/main.py`:

```python
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Verify Service Account Setup

You can verify your service account setup with this simple script:

```python
from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name('sheetsAPI.json', scopes=scope)
    client = gspread.authorize(creds)
    print("Authentication successful!")
    
    # Test access to POD-lists
    sheet = client.open('POD-lists')
    print(f"POD-lists spreadsheet found with {len(sheet.worksheets())} worksheets")
    
except Exception as e:
    print(f"Error: {e}")
```

## Environment Variables (Optional)

For production or shared environments, you can use environment variables:

```bash
export GOOGLE_ACCOUNT="your-email@gmail.com"
export GOOGLE_CREDENTIALS_FILE="path/to/credentials.json"
export POD_LISTS_SHEET="POD-lists"
```

Then modify your configuration:

```python
import os
from config.settings import Config

config = Config({
    'google_account': os.getenv('GOOGLE_ACCOUNT'),
    'credentials_file': os.getenv('GOOGLE_CREDENTIALS_FILE', 'sheetsAPI.json'),
    'pod_lists_sheet': os.getenv('POD_LISTS_SHEET', 'POD-lists')
})
```

## Security Best Practices

1. **Never commit credentials** to version control
   - The `.gitignore` file already excludes `*.json` files
   - Double-check before committing

2. **Use environment variables** in production
   - Store sensitive data in environment variables
   - Use secure secret management services

3. **Limit service account permissions**
   - Only grant necessary permissions
   - Regularly review and audit access

4. **Rotate credentials regularly**
   - Generate new service account keys periodically
   - Delete old, unused keys

## Next Steps

Once setup is complete, you can:

1. **Run the example**: `python src/main.py`
2. **Explore examples**: Check files in the `examples/` directory
3. **Read the API documentation**: See `docs/api_documentation.md`
4. **Customize for your needs**: Modify configurations and templates

