import requests

def count_words(subreddit, word_list, count_dict=None, after=None):
    if count_dict is None:
        count_dict = {}
    
    # Construct the URL
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    if after:
        url += f"?after={after}"

    # Set the User-Agent to avoid too many requests
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Make the request to Reddit API
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Parse titles
            for post in data['data']['children']:
                title = post['data']['title'].lower().split()
                for word in word_list:
                    word_lower = word.lower()
                    count = title.count(word_lower)
                    if count > 0:
                        if word_lower in count_dict:
                            count_dict[word_lower] += count
                        else:
                            count_dict[word_lower] = count
            # Check if there's a next page
            after = data['data'].get('after')
            if after:
                count_words(subreddit, word_list, count_dict, after)
        else:
            return

    except Exception as e:
        return

    # Base case: when there are no more pages to fetch, print the result
    if after is None:
        # Filter and sort the results
        sorted_words = sorted(count_dict.items(), key=lambda item: (-item[1], item[0]))
        for word, count in sorted_words:
            print(f"{word}: {count}")
