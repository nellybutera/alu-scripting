#!/usr/bin/python3
"""
3-count
Recursively queries the Reddit API, parses article titles, and prints a
sorted count of given keywords.
"""
import requests
import re
from collections import Counter


# Use a specific and custom User-Agent
HEADERS = {
    # REPLACE with your actual Reddit/GitHub username
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries the Reddit API to fetch all hot articles, counts
    the occurrences of keywords in their titles, and prints the result.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): List of keywords to count.
        after (str): The 'after' pagination token for recursion. Defaults to None.
        counts (dict): Dictionary accumulating the word counts. Defaults to None.
    """
    # Initialization on the first call
    if counts is None:
        # Initialize counts and normalize word_list for pattern matching
        counts = Counter({word.lower(): 0 for word in word_list})

        # Compile regex pattern to find whole words, case-insensitive
        # \b ensures word boundaries, preventing 'java.' or 'javascript' from counting 'java'
        keywords_pattern = r'\b(' + '|'.join(
            re.escape(word.lower()) for word in word_list) + r')\b'

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
            # Base case: Invalid subreddit or API error
            return

        data = response.json().get('data')
        if not data:
            return

        new_after = data.get('after')
        children = data.get('children', [])

        # Process titles on the current page
        for post in children:
            title = post.get('data', {}).get('title', '')

            # Find all matching keywords in the title (case-insensitive)
            # Use the pre-compiled pattern if the function were restructured,
            # but for a self-contained recursive function, the pattern is
            # built only on the initial call (counts is None).
            found_words = re.findall(
                keywords_pattern,
                title,
                re.IGNORECASE
            )

            # Update the count for each found word
            for word in found_words:
                counts[word.lower()] += 1

        if new_after is None:
            # Base case: end of recursion, time to print results

            # Filter and prepare items for sorting
            counted_items = [(word, count) for word, count in counts.items()
                             if count > 0]

            # Sort: 1. Count (descending) 2. Word (alphabetical ascending)
            counted_items.sort(key=lambda item: (-item[1], item[0]))

            # Print results in the required format
            for word, count in counted_items:
                print("{}: {}".format(word, count))

            return
        else:
            # Recursive call with the next pagination token
            # Pass the accumulated counts
            return count_words(subreddit, word_list, new_after, counts)

    except requests.RequestException:
        # Base case: connection error (do nothing/print nothing as required)
        return
