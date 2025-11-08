#!/usr/bin/python3
"""
2-recurse
Recursively queries the Reddit API and returns a list of titles for all hot articles.
"""
import requests
import sys

# Use a specific and custom User-Agent
HEADERS = {
    # REPLACE with your actual Reddit/GitHub username
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively queries the Reddit API and returns a list containing the titles
    of all hot articles for a given subreddit.

    Args:
        subreddit (str): The name of the subreddit.
        hot_list (list): The list accumulating post titles. Defaults to None 
                         to correctly handle the mutable default argument.
        after (str): The 'after' parameter for pagination.
        
    Returns:
        list: A list of hot article titles, or None if the 
        subreddit is invalid.
    """
    if hot_list is None:
        hot_list = []
        
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            allow_redirects=False,
            timeout=5
        )

        if response.status_code != 200:
            # Base case: invalid subreddit or API error
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
            # Base case: no more pages to load
            return hot_list
        else:
            # Recursive call with the next pagination token
            return recurse(subreddit, hot_list, new_after)
    except requests.RequestException:
        # Base case: connection error
        return None
