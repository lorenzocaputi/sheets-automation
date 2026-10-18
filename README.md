# sheets-automation

A Python script I wrote in 2023 that builds the Google Sheets needed to bulk-upload print-on-demand T-shirt designs, one niche at a time. The repository is archived and no longer maintained.

Given a niche phrase such as "i like cats and maybe 3 people", the script creates a spreadsheet with two worksheets. The first, APOD, has one row for each variant in a reference list of hobbies, jobs, years or drinks, kept in a separate spreadsheet called "POD-lists", together with the file name of each design. The second, FU, has the same 60 rows in the format the bulk-upload tool expects: image path, language, title, description, tags, product type and colour. The spreadsheet is then shared with the Google account set in the configuration.

## Run it

It needs a Google Cloud service account with the Sheets and Drive APIs enabled, its JSON key, and a "POD-lists" spreadsheet shared with that service account.

```sh
pip install -r requirements.txt
# set credentials_file and google_account in src/main.py (or config/settings.py)
python -m src.main
```

`automation.py` is the original single-file version of the same script.
