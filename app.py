from flask import Flask, render_template, request, jsonify, redirect, url_for
from langchain.chains.llm import LLMChain
from langchain.llms.openai import OpenAI
from langchain.prompts.prompt import PromptTemplate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from scrapers import aa_scraper
from create_db import *
from scrapers import tweet_scrap
import os

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_database = os.getenv("DB_DATABASE")

app = Flask(__name__)
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
    return render_template('index.html')


# creating news from tweets
@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    """
    App route for the news page. Loads the news from the database and displays them, and allows the user to generate a summary for a news article. 
    Additionally allows the user to refresh the news articles and generate a new summary with user feedback.
    """
    # print(index)
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", api_key="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", temperature=0.1)
    entries = Tweet.query.all()
    summary = None
    index = None
    with open('scrapers/twitter_handles.txt', 'r') as f:
        accounts = [line.strip() for line in f.readlines() if line.strip()]
        if accounts == []:
            accounts = None
    if request.method == 'POST':
        person = request.form.get('name')
        text = request.form.get('text')
        index = request.form.get('index')
        generated_news = request.form.get('generated_news')
        display_no = request.form.get('display_no')
        feedback = request.form.get('feedback')
        accounts = request.form.get('accounts')
        if index:
            print(index)
        else:
            print(display_no)
        if generated_news:
            # Find the tweet based on the content
            tweet_to_update = Tweet.query.filter_by(index=index).first()
           
            if tweet_to_update:
                tweet_to_update.news = generated_news
                tweet_to_update.is_generated = 1
                db.session.commit()
        elif feedback:
            
            template="""
            You are a news assistant that turns the posts published by institutions, organizations or ministers on their social media accounts into news.
            There is a feedback given you for you to correct given text.
            
            ### Instruction:
            Replying in Turkish is a MUST, if your answer is going to be english translate it to Turkish
            
            Now text is : {text}
            Now feedback is: {feedback}
            """
            
            tweet_to_adjust = Tweet.query.filter_by(index=display_no).first()
            text=tweet_to_adjust.news
            prompt = PromptTemplate(input_variables=["text","feedback"], template=template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            response = llm_chain.generate([{"text": text, "feedback": feedback}])
            summary = response.generations[0][0].text
            print(text)
        elif accounts or accounts == "":
            print(f'before: {accounts}')
            accounts = [account.strip() for account in accounts.split('\n') if account.strip()]
            print(f'after: {accounts}')
            with open('scrapers/twitter_handles.txt', 'w') as f:
                f.write('\n'.join(accounts))
        
        elif display_no:
            tweet_to_display = Tweet.query.filter_by(index=display_no).first()
            summary = tweet_to_display.news   
        elif text:
            template = """
            You are a news assistant that turns the posts published by institutions, organizations or ministers on their social media accounts into news. 
            You need to understand the context and convert it into a news format. The news format includes a headline (title), and a body part for the newly generated full text of the news. 
            Body part has 3 paragraphs. First paragraph is the summary of tweet.
            Second paragraph must JUST write surname of the person if  text in parentheses indicates a person, second paragraph must JUST write full name of the ministry or organization if  text in parentheses indicates a ministry or organizational account. 
            Lastly, third paragraph gives tweet and its' explanation. 

            ### Instruction:
            The text in parentheses indicates which person, institution or organization gave the statement. 
            Create news that contains title, and body parts meanwhile news format defined above. 
            Replying in Turkish is a MUST, if your answer is going to be english translate it to Turkish
            
            Now your input is: {text}
            """
            text = (person + " " + text)
            prompt = PromptTemplate(input_variables=["text"], template=template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            response = llm_chain.generate([{"text": text}])
            summary = response.generations[0][0].text
    
    try:
        return render_template('tweets.html', entries=entries, summary=summary, index=index, display_no=display_no, accounts=accounts)
    except:
        index = None  # You can set a default value for index
        display_no = None  # You can set a default value for display_no

        return render_template('tweets.html', entries=entries, summary=summary, index=index, display_no=display_no, accounts=accounts)


# creating tweets from news
@app.route('/news', methods=['GET','POST'])
def news():

    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", api_key="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", temperature=0.1)
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

            template = """
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

            prompt = PromptTemplate(input_variables=["text"], template=template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            response = llm_chain.generate([{"text": text}])
            summary = response.generations[0][0].text

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
