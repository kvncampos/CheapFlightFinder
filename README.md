# Flight Deal Notifier

This Python script leverages Google Sheets and a Flight Search API to find and notify you about flight deals.

## Prerequisites

Make sure you have the following set up before running the script:

- **Google Sheets API Key:** Obtain a Google Sheets API key and set it as the `SHEETY_API_KEY` environment variable.
- **Google Sheets Endpoint:** Set the URL of your Google Sheets endpoint as the `SHEETY_SPREADSHEET` environment variable.
- **Flight Search API Key:** Obtain an API key from a flight search service and set it as the `FLIGHT_SEARCH_API_KEY` environment variable.
- **Notification Configuration:** Set up your notification preferences such as `CELL_NUMBER`, `PROVIDER`, `GMAIL`, and `GMAIL_APP_PASS` as environment variables.

## How to Run

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```
2. Run the Script:
```bash
python main.py
```

## What the Script Does

    Get Google Sheet Data:
        Fetch flight data from the configured Google Sheets.

    Fetch Flight API Data:
        Use the Flight Search API to get detailed information about the flights.

    Data Validation for Only Deals:
        Transform the flight data and filter for deals.

    Send SMS Text for Any Deals:
        Notify about flight deals via SMS.

## Notes

    The script uses the DataManager, FlightSearch, FlightData, and NotificationSender classes to achieve its functionality.
    Ensure that your environment variables are correctly set before running the script.


Feel free to customize it further based on additional details you want to provide or any specific instructions for users.
