from flask import Flask, render_template, request, jsonify
from langchain.chains.llm import LLMChain
from langchain.llms.openai import OpenAI
from langchain.prompts.prompt import PromptTemplate
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
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
    
    
class News(db.Model):
    __tablename__ = 'news'
    index = db.Column(db.Integer, primary_key=True)
    Link = db.Column(db.Text)
    Content = db.Column(db.Text)
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tweets')
def tweets():
    entries = Tweet.query.all()
    return render_template('tweets.html', entries=entries)

@app.route('/news')
def news():
    entries = News.query.all()
    return render_template('news.html', entries=entries)

# used for creating news from tweets
@app.route('/generate_from_tweet', methods=['POST'])
def generate_news():
    summary = None
    if request.method == 'POST':
        text = request.form.get('text')
        summary = None

        if text:
            llm = OpenAI(api_key="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")

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

    entries = Tweet.query.all()

    return render_template('tweets.html', entries=entries, summary=summary)


# used for creating tweets from news
@app.route('/generate_from_news', methods=['POST'])
def generate_tweets():
    summary = None
    if request.method == 'POST':
        text = request.form.get('text')
        summary = None

        if text:
            llm = OpenAI(api_key="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")

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

    return render_template('news.html', entries=entries, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
