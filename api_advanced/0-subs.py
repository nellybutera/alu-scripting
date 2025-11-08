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
    Queries the Reddit API and returns the number 
    of subscribers for a given subreddit.
    Returns 0 if the subreddit is invalid or an error occurs.
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
