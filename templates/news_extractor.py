import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_news_articles(query, num_articles=10):
    """
    Fetches news articles related to a given query from Bing News.
    
    Parameters:
    query (str): Company name to search for.
    num_articles (int): Number of articles to fetch.
    
    Returns:
    list: A list of dictionaries containing title, link, and summary.
    """

    search_url = f"https://www.bing.com/news/search?q={query}&FORM=HDRSC6"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise error for failed requests
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    articles = []
    news_cards = soup.find_all("div", class_="news-card", limit=num_articles)  # Adjust based on site structure

    for card in news_cards:
        title_tag = card.find("a")
        summary_tag = card.find("div", class_="snippet")
        
        if title_tag and summary_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag["href"]
            summary = summary_tag.get_text(strip=True)
            
            articles.append({
                "title": title,
                "link": link,
                "summary": summary
            })

    return articles

if __name__ == "__main__":
    company_name = input("Enter company name: ")
    news_articles = get_news_articles(company_name)
    
    if news_articles:
        df = pd.DataFrame(news_articles)
        print(df)
        df.to_csv(f"{company_name}_news.csv", index=False)
        print(f"News articles saved as {company_name}_news.csv")
    else:
        print("No articles found!")
