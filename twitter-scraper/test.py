from scrapperNEW import Twitter_Scraper
USER_UNAME = "" # elonmusk 
USER_PASSWORD = "" 
scraper = Twitter_Scraper(
    username=USER_UNAME,
    password=USER_PASSWORD,
)
scraper.login()

scraper.scrape_tweets(
    max_tweets=10,
    scrape_usernames=["RTErdogan","aBayraktar1","superlig",]
)

scraper.driver.close()
scraper.temp_driver.close()