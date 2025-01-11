import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
from newspaper import Article
import time

# Define the RSS feed URL for Elon Musk news
rss_url = "https://news.google.com/rss/search?q=Elon+Musk&hl=en-US&gl=US&ceid=US:en"

# Parse the RSS feed using the feedparser library
feed = feedparser.parse(rss_url)

# Define the time range to filter articles from the past 6 months
six_months_ago = datetime.now() - timedelta(days=6 * 30)

# Function to parse the publication date from the RSS entry
def parse_pub_date(entry):
    try:
        return datetime(*entry.published_parsed[:6])
    except AttributeError:
        return None

# Extract and filter articles published within the defined time range
articles = []
for entry in feed.entries:
    pub_date = parse_pub_date(entry)
    if pub_date and pub_date >= six_months_ago:
        # Remove HTML tags from the summary text
        soup = BeautifulSoup(entry.summary, 'html.parser')
        summary_text = soup.get_text()
        articles.append({
            'Title': entry.title,
            'Link': entry.link,
            'Published': pub_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Summary': summary_text
        })

# Create a pandas DataFrame from the list of articles
df = pd.DataFrame(articles)

# Save the DataFrame to a CSV file
csv_file = "elon_musk_news.csv"
df.to_csv(csv_file, index=False)

# Function to extract the full content of an article from a given URL
def extract_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        # Check if the article text is empty
        if len(article.text) < 10:
            raise Exception("Article text is empty")
        return article.text
    except Exception as e:
        print(f"Failed to extract content from {url}: {e}")
        return None

# Apply the content extraction function to each article's link
df['Content'] = df['Link'].apply(extract_content)

# Save the updated DataFrame with article content to a new CSV file
csv_file_with_content = "elon_musk_news_with_content.csv"
df.to_csv(csv_file_with_content, index=False)

# Print confirmation messages indicating the number of saved articles
print(f"Saved {len(df)} articles with content to {csv_file_with_content}")
print(f"Saved {len(df)} articles to {csv_file}")
