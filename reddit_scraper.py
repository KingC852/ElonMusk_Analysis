import praw
import concurrent.futures
import time
import logging
import pandas as pd
from prawcore.exceptions import RequestException, ResponseException, ServerError
import os
from tqdm import tqdm

# Configure logging to track the script's progress and errors
logging.basicConfig(
    filename='reddit_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Set up Reddit API credentials (replace with your own credentials if needed)
reddit = praw.Reddit(
    client_id='gf0i0xGSFFGYwhIpTkGqZw',
    client_secret='ZxuFuxn5sAAEDljDrj-mHt2v2gRBQA',
    user_agent='python:my_reddit_app:v1.0 (by u/Gold-Celebration-132)'
)

# Function to fetch post titles and comments from a specified subreddit
def fetch_post_data(subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts_data = []
        seen_ids = set()
        for post in subreddit.top(limit=200):
            if post.id not in seen_ids:
                seen_ids.add(post.id)
                # Collect post details including title, score, and URL
                post_data = {
                    'title': post.title,
                    'score': post.score,
                    'url': post.url,
                    'comment1': None, 'comment2': None, 'comment3': None, 'comment4': None, 'comment5': None,
                    'comment6': None, 'comment7': None, 'comment8': None, 'comment9': None, 'comment10': None,
                    'comment11': None, 'comment12': None, 'comment13': None, 'comment14': None, 'comment15': None,
                    'comment16': None, 'comment17': None, 'comment18': None, 'comment19': None, 'comment20': None
                }
                # Retrieve the top 20 comments from the post
                post.comments.replace_more(limit=0)
                top_comments = post.comments.list()[:20]
                for idx, comment in enumerate(top_comments):
                    post_data[f'comment{idx + 1}'] = comment.body
                posts_data.append(post_data)
        logging.info(f'Successfully retrieved posts data from {subreddit_name}')
        return posts_data
    except (RequestException, ResponseException, ServerError) as e:
        logging.error(f'Error retrieving posts data from {subreddit_name}: {e}')
        return []

# Main function to scrape data from multiple subreddits and save to a CSV file
if __name__ == '__main__':
    subreddits = ['elonmusk']  # List of subreddits to scrape
    all_posts_data = []

    # Use a ThreadPoolExecutor to scrape subreddits concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_subreddit = {executor.submit(fetch_post_data, sub): sub for sub in subreddits}
        for future in concurrent.futures.as_completed(future_to_subreddit):
            subreddit = future_to_subreddit[future]
            logging.info(f'Completed fetching data for {subreddit}')
            try:
                posts_data = future.result()
                all_posts_data.extend(posts_data)
            except Exception as e:
                logging.error(f'Error processing {subreddit}: {e}')
            time.sleep(1)  # Pause to adhere to API rate limits

    # Save the scraped data to a CSV file
    df = pd.DataFrame(all_posts_data)
    df.to_csv('reddit_posts_data.csv', index=False)
    logging.info('Saved data to reddit_posts_data.csv')