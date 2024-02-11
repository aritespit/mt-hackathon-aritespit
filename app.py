from flask import Flask, render_template, request, jsonify, redirect, url_for
from langchain.chains.llm import LLMChain
from langchain.prompts.prompt import PromptTemplate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from scrapers import aa_scraper
from create_db import *
from scrapers import tweet_scrap
import os
from openai import OpenAI
import random

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

class Tweet(db.Model):
    """
    Class that represents the tweets table in the database.
    """
    __tablename__ = 'tweets'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Handle = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    Content = db.Column(db.Text)
    tweet_id = db.Column(db.Text)
    is_generated = db.Column(db.Boolean)
    news = db.Column(db.Text)
    photo_link = db.Column(db.Text)
    
    
class News(db.Model):
    """
    Class that represents the news table in the database.
    """
    __tablename__ = 'news'
    index = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.Text)
    Content = db.Column(db.Text)
    summary = db.Column(db.Text)
    
@app.route('/')
def home():
    tweets = Tweet.query.all()
    news = News.query.all()
    with open('data/last_fetched_time_news.txt', 'r') as f:
        last_fetched_time_news = f.read()
    with open('data/last_fetched_time_tweets.txt', 'r') as f:
        last_fetched_time_tweets = f.read()
    return render_template('index.html', tweets=len(tweets), news=len(news), news_time=last_fetched_time_news, tweets_time=last_fetched_time_tweets)

# creating news from tweets
@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    """
    App route for the news page. Loads the news from the database and displays them, and allows the user to generate a summary for a news article. 
    Additionally allows the user to refresh the news articles and generate a new summary with user feedback.
    """
    # print(index)
    client = OpenAI(api_key="") #API key needed here
    entries = Tweet.query.all()
    summary = None
    index = None
    with open('scrapers/twitter_handles.txt', 'r') as f:
        accounts = [line.strip() for line in f.readlines() if line.strip()]
    if request.method == 'POST':
        person = request.form.get('name')
        text = request.form.get('text')
        index = request.form.get('index')
        etiket_no = request.form.get('etiket_no')
        generated_news = request.form.get('generated_news')
        display_no = request.form.get('display_no')
        feedback = request.form.get('feedback')
        accounts = request.form.get('accounts')
        if index:
            print(index)
        else:
            print(f'display no {display_no}')

            
        if accounts or accounts == "":
            print(f'before: {accounts}')
            accounts = [account.strip() for account in accounts.split('\n') if account.strip()]
            print(f'after: {accounts}')
            with open('scrapers/twitter_handles.txt', 'w') as f:
                f.write('\n'.join(accounts))
        
        if generated_news:
            # Find the tweet based on the content
            tweet_to_update = Tweet.query.filter_by(index=index).first()
           
            if tweet_to_update:
                tweet_to_update.news = generated_news
                tweet_to_update.is_generated = 1
                db.session.commit()

        elif etiket_no:
            # Find the tweet based on the content, extract the summary and create tags
            print(f'Etiket no: {etiket_no}')
            tweet_to_adjust = Tweet.query.filter_by(index=etiket_no).first()
            text=tweet_to_adjust.news
            print(text)

            template=[{"role":"system", 
                        "content":f"""Given the following news article text, extract and list the most relevant keywords. 
                        Focus on identifying terms that are significant to the content's overall meaning, including any notable names, places, subjects in the sentences. Keywords should be about
                        the news, it should be about the main topic of the news.
                        Do not make up stuff and do not provide meaningless words additionally provide the keywords in a bullet-point format for clarity. 
                        Keywords shouldn't be action verbs. Show top 3 keywordss."""},
                        {"role":"user",
                        "content": text}]
            
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=template,
            temperature=0,
            max_tokens=554,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )


            summary =  response.choices[0].message.content


        elif feedback:
            # find the tweet based on the content, adjust the summary based on the feedback
            tweet_to_adjust = Tweet.query.filter_by(index=display_no).first()
            text=tweet_to_adjust.news
            print(text)

            feedback_sys=[{"role":"system", 
                        "content":f"""You are a news assistant who turns the posts published by institutions, organizations or ministers on their social media accounts into news. 
                        Use the feedback given by the user and update the text, do not make up new stuff just apply the giveng feedback to you."""},
                        {"role":"system",
                        "content": feedback},
                        {"role":"user",
                        "content": text}]
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=feedback_sys,
            temperature=0,
            max_tokens=554,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )


            summary =  response.choices[0].message.content

        elif display_no:
            # Find the tweet based on the content
            tweet_to_display = Tweet.query.filter_by(index=display_no).first()
            summary = tweet_to_display.news   
        
        elif text:
            text = person + " " + text
            xtonews_input=[
                    {
                    "role": "system",
                    "content":             """You are a news assistant that turns the posts published by institutions, organizations or ministers on their social media accounts into news. 
                    You need to understand the context and convert it into a news format. The news format includes a headline (title), and a body part for the newly generated full text of the news. 
                    Body part has 3 paragraphs. First paragraph is the summary of tweet.
                    Second paragraph must JUST write surname of the person if  text in parentheses indicates a person, second paragraph must JUST write full name of the ministry or organization if  text in parentheses indicates a ministry or organizational account. 
                    Lastly, third paragraph gives tweet and its' explanation. 

                    ### Instruction:
                    The text in parentheses indicates which person, institution or organization gave the statement. 
                    Create news that contains title, and body parts meanwhile news format defined above. 
                    Replying in Turkish is a MUST, if your answer is going to be english translate it to Turkish\n"""
                    },
                    {
                    "role": "user",
                    "content": "(Enerji ve Tabii Kaynaklar Bakanı Alparslan Bayraktar) İran Cumhurbaşkanı Sayın İbrahim Reisi’nin Ankara ziyareti öncesi İran Petrol Bakanı Sayın Javad Owji ve beraberindeki heyet ile Bakanlığımızda bir araya geldik.\n\nDerin ilişkilere sahip olduğumuz İran ile enerji alanındaki iş birliğimizi daha da ileri taşıma konusundaki kararlılığımızı dile getirdik.\n\nÖzellikle doğal gaz alanında iş birliğimizi yeni dönemde daha geniş çerçevede ele alınması gerektiğini ifade ettik.\n"
                    },
                    {
                    "role": "assistant",
                    "content": "Bakan Bayraktar, İranlı mevkidaşı ile 'enerji işbirliğini' görüştü\n\nEnerji ve Tabii Kaynaklar Bakanı Alparslan Bayraktar, İran Petrol Bakanı Javad Owji ile iki ülkenin enerji işbirliğine dair konuları ele aldı.\n\n'Derin ilişkilere sahip olduğumuz İran ile enerji alanındaki işbirliğimizi daha da ileri taşıma konusundaki kararlılığımızı dile getirdik. Özellikle doğal gaz alanında işbirliğimizin yeni dönemde daha geniş çerçevede ele alınması gerektiğini ifade ettik.'"
                    },
                    {
                        "role":"user",
                        "content":text}
                ]
            
            response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=xtonews_input,
            temperature=0.2,
            max_tokens=554,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
            summary = response.choices[0].message.content
            mahrec = "(AA)"

            second = [#"X sosyal medya hesabından yaptığı paylaşımda şunları kaydetti:",
                    # "X sosyal medya hesabından yaptığı paylaşımda aşağıdaki ifadeleri kullandı:",
                    # "X sosyal medya platformunda paylaştığı gönderide şu sözleri yazdı:",
                    "X sosyal medya hesabından habere ilişkin paylaşım yapıldı.",
                    "X sosyal medya hesabından paylaşımda bulundu."]

            try: 
                paragraphs = summary.split('\n\n')

                first_paragraph = paragraphs[1] if paragraphs else ''

                random_second = random.choice(second)

                random_second = person + ", " + random_second

                result = f"\n\n {mahrec} - {first_paragraph} \n\n {random_second}"

                title = paragraphs[0] if paragraphs else ''
                last_paragraph = paragraphs[-1] if paragraphs else ''

                summary = title + result + "\n\n" + last_paragraph
            except: pass
    

    try:
        return render_template('tweets.html', entries=entries, summary=summary, index=index, display_no=display_no, accounts=accounts)
    except:
        index = None  # You can set a default value for index
        display_no = None  # You can set a default value for display_no

        return render_template('tweets.html', entries=entries, summary=summary, index=index, display_no=display_no, accounts=accounts)


# creating tweets from news
@app.route('/news', methods=['GET','POST'])
def news():

    client = OpenAI(api_key="") #API key needed here
    index=None
    summary = None
    if request.method == 'POST':
        text = request.form.get('text')
        summary = None
        index = request.form.get('index')
        generated_summary = request.form.get('generated_summary')
        
        if generated_summary:
            # Find the tweet based on the content
            summary_to_update = News.query.filter_by(index=index).first()
            if summary_to_update:
                summary_to_update.summary = generated_summary
                db.session.commit()
        
        
        elif text:
            print("boop new architecture alert")

            news_to_x=f"""
            You are an AI assistant for News Agency to shorten the longer news article into 3 bullet points. You are required to understand the context then create these bulletpoints. Your bulletpoints should contain important parts of the article, i.e. parts that contain numerical values or explain the text best.

            ### Instruction:
            Create three bulletpoints that summarize the important parts of the news article.
            You should spread the W-H questions (What, When, Where, Who, Why, How) in the bulletpoints.
            Do it as thoroughly and detailed as you can while keeping the bulletpoints short.
            Always reply in Turkish; if your answer is not in Turkish, translate it.
            Keep the bulletpoints short.
            ### User Input: {text}
            ### Response: Your Answer
                        """
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                max_tokens=500,
                prompt=news_to_x,
                temperature=0.1
            )
            summary =  response.choices[0].text

    entries = News.query.all()

    return render_template('news.html', entries=entries, summary=summary,index=index)

@app.route('/refresh_news', methods=['GET'])
def refresh_news():
    """
    Function that refreshes the news articles by scraping the Anadolu Ajansi website and saving them to the database.
    """
    df = aa_scraper.scrape()
    save_to_db(df, 'news') 
    return redirect(url_for('news'))

@app.route('/refresh_tweets', methods=['GET'])
def refresh_tweets():
    """
    Function that refreshes the tweets by scraping Twitter and saving them to the database.
    """
    print("refresh tweet boop")
    tweet_scrap.scrape_tweets()
    tweet_scrap.read_and_save()
    df = tweet_scrap.get_tweets()
    save_to_db(df, 'tweets') 
    return redirect(url_for('tweets'))

if __name__ == '__main__':
    app.run(debug=True)