from flask import Flask, render_template, request, jsonify, redirect, url_for
from langchain.chains.llm import LLMChain
from langchain.llms.openai import OpenAI
from langchain.prompts.prompt import PromptTemplate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from scrapers import aa_scraper
from create_db import *
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
    __tablename__ = 'tweets'
    index = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))
    Handle = db.Column(db.String(255))
    Timestamp = db.Column(db.DateTime)
    Content = db.Column(db.Text)
    is_generated = db.Column(db.Boolean)
    news = db.Column(db.Text)
    
    
class News(db.Model):
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
    llm = OpenAI(model_name="gpt-3.5-turbo-instruct", api_key="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", temperature=0.1)
    entries = Tweet.query.all()
    summary = None
    index=None
    if request.method == 'POST':
        person = request.form.get('name')
        text = request.form.get('text')
        index = request.form.get('index')
        generated_news = request.form.get('generated_news')
        display_no = request.form.get('display_no')
        feedback = request.form.get('feedback')
        if generated_news:
            # Find the tweet based on the content
            tweet_to_update = Tweet.query.filter_by(index=index).first()
           
            if tweet_to_update:
                tweet_to_update.news = generated_news
                tweet_to_update.is_generated = 1
                db.session.commit()
        elif display_no:
            print(display_no)
            tweet_to_display = Tweet.query.filter_by(index=display_no).first()
            print(tweet_to_display)
            summary = tweet_to_display.news   
        elif feedback:
            print(index)
            template="""
            You are a news assistant that turns the posts published by institutions, organizations or ministers on their social media accounts into news.
            There is a feedback given you for you to correct given text.
            
            ### Instruction:
            Replying in Turkish is a MUST, if your answer is going to be english translate it to Turkish
            
            Now text is : {text}
            Now feedback is: {feedback}
            """
            tweet_to_adjust = Tweet.query.filter_by(index=index).first()
            text=tweet_to_adjust.news
            prompt = PromptTemplate(input_variables=["text","feedback"], template=template)
            llm_chain = LLMChain(llm=llm, prompt=prompt)
            response = llm_chain.generate([{"text": text, "feedback": feedback}])
            print(response)
            summary = response.generations[0][0].text
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
            print(response)
            summary = response.generations[0][0].text

    return render_template('tweets.html', entries=entries, summary=summary,index=index)

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
            print(summary_to_update)
            if summary_to_update:
                summary_to_update.summary = generated_summary
                db.session.commit()
        
        
        elif text:

            template = """
            You are an AI assistant for News Agency to shorten the longer news article into 3 bullet points. You are required to understand the context then create these bulletpoints. Your bulletpoints should contain important parts of the article, i.e. parts that contain numerical values or explain the text best.

            ### Instruction:
            Create three bulletpoints that summarize the important parts of the news article.
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
    df = aa_scraper.scrape()
    save_to_db(df, 'news') 
    return redirect(url_for('news'))

@app.route('/refresh_tweets', methods=['GET'])
def refresh_tweets():
    print("Not implemented yet")
    return redirect(url_for('tweets'))

if __name__ == '__main__':
    app.run(debug=True)
