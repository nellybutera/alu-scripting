#!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts
listed for a given subreddit.
"""
import requests


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.

    If the subreddit is invalid, prints None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'alx_api_advanced_project/1.0 by your_username'}
    params = {'limit': 10}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=5
        )

        if response.status_code != 200:
            print(None)
            return

        data = response.json().get('data', {})
        posts = data.get('children', [])

        if not posts:
            print(None)
            return

        for post in posts:
            title = post.get('data', {}).get('title')
            if title:
                print(title)

    except requests.RequestException:
        print(None)
