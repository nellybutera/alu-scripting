#!/usr/bin/python3
"""
Recursively queries the Reddit API and prints a sorted count of given keywords.
"""
import requests

HEADERS = {
    'User-Agent': 'alx_api_advanced_project/1.0 by your_username'
}


def count_words(subreddit, word_list, after=None, counts=None):
    """
    Recursively queries the Reddit API, parses hot article titles,
    and prints sorted count of given keywords (case-insensitive).

    Args:
        subreddit (str): subreddit name.
        word_list (list): list of keywords to count.
        after (str): token for pagination.
        counts (dict): dictionary to store cumulative word counts.
    """
    if counts is None:
        # Initialize counts dictionary (case-insensitive merge of duplicates)
        counts = {}
        for word in word_list:
            key = word.lower()
            counts[key] = counts.get(key, 0)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    params = {'limit': 100}
    if after:
        params['after'] = after

    try:
        res = requests.get(url, headers=HEADERS,
                           params=params, allow_redirects=False,
                           timeout=5)
        if res.status_code != 200:
            return

        data = res.json().get('data', {})
        children = data.get('children', [])
        next_after = data.get('after')

        # Go through all post titles
        for post in children:
            title = post.get('data', {}).get('title', '').lower().split()
            for w in title:
                # Count only exact matches ignoring punctuation endings
                for key in counts.keys():
                    if w == key:
                        counts[key] += 1

        if next_after:
            # Recursive call to next page
            return count_words(subreddit, word_list, next_after, counts)
        else:
            # Base case: all posts fetched
            # Filter and sort results
            filtered = {k: v for k, v in counts.items() if v > 0}
            sorted_counts = sorted(filtered.items(),
                                   key=lambda x: (-x[1], x[0]))
            for word, cnt in sorted_counts:
                print(f"{word}: {cnt}")

    except requests.RequestException:
        return
