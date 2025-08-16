"""
Script to check for the latest Mackie USB driver from the Mackie website.

- Fetches driver list from Mackie's file explorer API.
- Compares known driver version to the latest available.
- Notifies user if a newer driver is available and provides download link.
- Handles connection errors gracefully.

Usage:
    python script.py
"""

import requests
import re

# Configuration
KNOWN_DRIVER = "Mackie_USB_Driver_v4_47_0.zip"
API_URL = "https://mackie.com/file-explorer.json?folder=19783"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def extract_version(filename):
    """Extract version tuple from filename using regex"""
    match = re.search(r'v(\d+)_(\d+)_(\d+)', filename)
    return tuple(map(int, match.groups())) if match else (0, 0, 0)

def main():
    try:
        # Configure request with timeout and headers
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current_version = extract_version(KNOWN_DRIVER)
        latest = None

        # Process items with error handling
        for item in data.get("content", []):
            if not (fname := item.get("label")):
                continue
            
            if (version := extract_version(fname)) > current_version:
                latest = item
                current_version = version

        print(f"Latest driver found: {version}")

        if latest:
            print(f"New driver available: {latest['label']}")
            print(f"Download URL: {latest['link']}")
        else:
            print(f"Ratsi, unfortunately you already have the latest driver version {KNOWN_DRIVER}. Mackie is so lamer.")

    except requests.exceptions.RequestException as e:
        print(f"Connection error: {str(e)}")
        print("Verify the URL is correct and your internet connection")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
