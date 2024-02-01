from scrapperNEW import Twitter_Scraper
USER_UNAME = "" # elonmusk 
USER_PASSWORD = "" 
scraper = Twitter_Scraper(
    username=USER_UNAME,
    password=USER_PASSWORD,
)
scraper.login()

with open('twitter_handles.txt', 'r') as file:
    twitter_handles = file.read().split('\n')

scraper.scrape_tweets(
    max_tweets=10,
    scrape_usernames=twitter_handles
)

scraper.driver.close()
scraper.temp_driver.close()