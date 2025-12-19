import requests
import json
import os

SOURCE_API_URL = "https://ttdevasthanams.ap.gov.in/cms/api/universal-latest-updates?populate=*"

def fetch_updates():
    """Fetch updates from the TTD internal API."""
    try:
        print(f"Fetching updates from {SOURCE_API_URL}...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(SOURCE_API_URL, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        return None

def parse_updates(raw_data):
    """Parse the raw JSON response into a simplified list of updates."""
    updates = []
    try:
        if not raw_data or 'data' not in raw_data:
            return []
        
        main_data = raw_data['data'][0]
        attributes = main_data.get('attributes', {})
        update_list = attributes.get('update', [])
        
        for item in update_list:
            update = {
                'id': item.get('id'),
                'message': item.get('data'),
                'cta': item.get('cta'),
                'link': item.get('redirectionLink')
            }
            updates.append(update)
            
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing data structure: {e}")
        
    return updates

def get_latest_updates():
    """Convenience function to fetch and parse updates."""
    raw_data = fetch_updates()
    if raw_data:
        return parse_updates(raw_data)
    return []
