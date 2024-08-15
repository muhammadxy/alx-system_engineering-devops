import requests
from collections import Counter
import sys

def count_words(subreddit, word_list, after=None, count=Counter()):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {'limit': 100, 'after': after}

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code != 200:
        return

    data = response.json().get('data', {})
    posts = data.get('children', [])
    after = data.get('after', None)
    
    for post in posts:
        title = post['data']['title']
        words_in_title = title.lower().split()
        
        for word in word_list:
            word_lower = word.lower()
            count[word_lower] += words_in_title.count(word_lower)
    
    if after:
        count_words(subreddit, word_list, after, count)
    else:
        # Sorting the count
        sorted_count = sorted(count.items(), key=lambda item: (-item[1], item[0]))
        for word, freq in sorted_count:
            if freq > 0:
                print(f"{word}: {freq}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = [x for x in sys.argv[2].split()]
        count_words(subreddit, word_list)
