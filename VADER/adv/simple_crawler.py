import requests
from bs4 import BeautifulSoup
import pandas as pd

# Get comment data for a single page
def get_reviews(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews = soup.find_all('div', class_='text show-more__control')
    data = [review.get_text() for review in reviews]
    return data

# Scrape comment data from multiple pages
def scrape_all_reviews(base_url, pages):
    all_reviews = []
    for i in range(pages):
        url = f"{base_url}&page={i+1}"
        reviews = get_reviews(url)
        all_reviews.extend(reviews)
    return all_reviews

# Main
if __name__ == '__main__':
    base_url = 'EXAMPLE'
    pages = 5  # example
    reviews = scrape_all_reviews(base_url, pages)

    # Save data to CSV file
    df = pd.DataFrame(reviews, columns=['Review'])
    df.to_csv('EXAMPLE.csv', index=False)
    print("Saved")
