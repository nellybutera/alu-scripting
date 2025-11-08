#!/usr/bin/python3
"""
2-recurse
Recursively queries the Reddit API
and returns a list of titles for all
hot articles.
"""
import requests


HEADERS = {
    # REPLACE with your actual Reddit/GitHub username
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and
    returns a list containing the titles
    of all hot articles for a given subreddit.
    Handles pagination via the 'after'
    parameter.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): The list accumulating post titles.
        It defaults to None
        to avoid issues with mutable default arguments, but is
        initialized to [] on the first call.
        after (str): The 'after' pagination token returned
        by the API.

    Returns:
        list: A list of hot article titles, or None
        if the subreddit is invalid.
    """
    # Initialize hot_list on the first call
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)

    # Parameters for the request
    # (limit=100 is the max per request)
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            allow_redirects=False,  # Required: Do not follow redirects
            timeout=5
        )

        if response.status_code != 200:
            # Base case: Invalid subreddit or API error (e.g., 404)
            return None

        # Safely extract data
        data = response.json().get('data')
        if not data:
            return None

        new_after = data.get('after')
        children = data.get('children', [])

        # Collect titles from the current page
        for post in children:
            title = post.get('data', {}).get('title')
            if title:
                hot_list.append(title)

        if new_after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, new_after)

    except requests.RequestException:
        return None
