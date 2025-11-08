#!/usr/bin/python3
"""
1-top_ten
Queries the Reddit API and prints the titles of the first 10 hot posts.
"""
import requests

# Use a specific and custom User-Agent
HEADERS = {
    # REPLACE with your actual Reddit/GitHub username
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def top_ten(subreddit):
    """
    Prints the titles of the first 10 hot posts for a given subreddit.
    Prints None if the subreddit is invalid.
    """
    # Request up to 10 items
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            allow_redirects=False,
            timeout=5
        )

        if response.status_code == 200:
            # Safely navigate the JSON structure
            data = response.json().get('data', {})
            posts = data.get('children', [])

            if posts:
                # Iterate and print the title of each post
                for post in posts:
                    print(post.get('data', {}).get('title'))
            # If posts is an empty list, a valid subreddit might just be empty.
            # We don't print anything extra here unless it's an error case.
            
        else:
            # Invalid subreddit or error
            print("None")

    except requests.RequestException:
        # Handle connection errors
        print("None")
