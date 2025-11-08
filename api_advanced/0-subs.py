#!/usr/bin/python3
"""
0-subs
Queries the Reddit API and returns the number of subscribers for a given subreddit.
Returns 0 if the subreddit is invalid.
"""
import requests

# Use a specific and custom User-Agent to comply with Reddit API rules
HEADERS = {
    # REPLACE with your actual Reddit/GitHub username
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def number_of_subscribers(subreddit):
    """
    Queries the Reddit API and returns the number of subscribers for a given subreddit.
    Returns 0 if the subreddit is invalid or an error occurs.
    """
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            allow_redirects=False,  # Required to ensure redirects aren't followed
            timeout=5
        )

        # Check for successful response (status 200)
        if response.status_code == 200:
            # Use .get() for safe dictionary access
            data = response.json().get('data', {})
            # Return the subscriber count, defaulting to 0 if key is missing
            return data.get('subscribers', 0)
        else:
            # Handle non-200 status codes (e.g., 404, or redirect due to invalid name)
            return 0

    except requests.RequestException:
        # Handle network issues, connection errors, timeouts, etc.
        return 0
