from scrapers.tweet_backbone import Twitter_Scraper
import os
import pandas as pd
def scrape_tweets():
    USER_UNAME = "aritespit" 
    USER_PASSWORD = "AnadoluArilari" 

    scraper = Twitter_Scraper(
        username=USER_UNAME,
        password=USER_PASSWORD,
    )
    scraper.login()

    try: 
        with open("scrapers/twitter_handles.txt", 'r') as file:
            twitter_handles = file.read().split('\n')
    except FileNotFoundError:
        with open("twitter_handles.txt", 'r') as file:
            print("path error")
            twitter_handles = file.read().split('\n')

    scraper.scrape_tweets(
        max_tweets=10,
        scrape_usernames=twitter_handles
    )

    scraper.driver.close()
    scraper.temp_driver.close()

def read_and_save():
    folder_path = 'tweets/' if os.path.isdir('tweets/') else 'twitter_scraper/tweets/'
    folder_name = os.listdir(folder_path)

    datasets = []
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            df = pd.read_csv(folder_path + file)
            print(f'df handle: {df["Handle"].unique()} | folder name: {file.split(".")[0]}')
            df = df[df['Handle'] == f'{file.split(".")[0]}']
            datasets.append(df)

    combined_dataset = pd.concat(datasets)
    columns_to_keep = ['index', 'Name', 'Handle', 'Timestamp', 'Content']
    columns_to_drop = [col for col in combined_dataset.columns if col not in columns_to_keep]
    combined_dataset.drop(columns=columns_to_drop, inplace=True)
    combined_dataset.to_csv('data/combined_tweets.csv', index=False)

def get_tweets():
    return pd.read_csv('data/combined_tweets.csv')


if __name__ == "__main__":
    scrape_tweets()
    read_and_save()