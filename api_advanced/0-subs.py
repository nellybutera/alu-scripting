#!/usr/bin/python3
"""
0-subs
Finding sub count
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
    Finding sub count
    Returns 0 if invalid.
    """
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            allow_redirects=False,
            timeout=5
        )

        # Check for successful response (status 200)
        if response.status_code == 200:
            data = response.json().get('data', {})
            return data.get('subscribers', 0)
        else:
            return 0

    except requests.RequestException:
        return 0
