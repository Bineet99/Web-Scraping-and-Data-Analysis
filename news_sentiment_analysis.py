import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
import matplotlib.pyplot as plt

#Scrape Headlines from Hindustan Times
def scrape_hindustantimes():
    url = 'https://www.hindustantimes.com/india-news'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('h3', class_='hdg3')  # Verified class for headlines
    headlines = [h.get_text(strip=True) for h in articles]
    print("Headlines found:", len(headlines))
    return headlines

#Analyze Sentiment
def analyze_sentiment(headlines):
    polarity_scores = []
    sentiments = []

    for headline in headlines:
        blob = TextBlob(headline)
        polarity = blob.sentiment.polarity
        polarity_scores.append(polarity)

        if polarity > 0:
            sentiments.append('Positive')
        elif polarity < 0:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    return polarity_scores, sentiments

#Main function
def main():
    headlines = scrape_hindustantimes()
    if not headlines:
        print(" No headlines scraped. Try later or check the URL.")
        return

    polarity_scores, sentiments = analyze_sentiment(headlines)

    df = pd.DataFrame({
        'Headline': headlines,
        'Polarity': polarity_scores,
        'Sentiment': sentiments
    })
    print("\n Sample Data:\n")
    print(df.head())

    df.to_csv("hindustantimes_sentiment.csv", index=False)
    print("\nData saved to hindustantimes_sentiment.csv")

    if not df.empty:
        df['Sentiment'].value_counts().plot(kind='bar', color=['green', 'red', 'gray'])
        plt.title("Sentiment Distribution of India News")
        plt.xlabel("Sentiment")
        plt.ylabel("Number of Headlines")
        plt.show()
    else:
        print("No data to plot.")
if __name__ == '__main__':
    main()
