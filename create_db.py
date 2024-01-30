import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

def get_credentials():
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_database = os.getenv("DB_DATABASE")
    print(db_host)
    return db_host, db_port, db_user, db_password, db_database

def create_db():
    db_host, db_port, db_user, db_password, db_database = get_credentials()

    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database='mysql'
        )
        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS anadoluajansi;")
        print("Database 'anadoluajansi' created.")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

def save_to_db(df, table_name):
    db_host, db_port, db_user, db_password, db_database = get_credentials()

    try:
        engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}')

        if table_name=="tweets":
            additional_columns = {'is_generated': 0, 'news': ""}
        else:
            additional_columns = {'summary': ""}
        df = df.assign(**additional_columns)

        df.to_sql(table_name, con=engine, if_exists='replace')

        engine.dispose()

        print(f"DataFrame saved to '{table_name}' table in the 'anadoluajansi' database with additional columns.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    create_db()
    df_news = pd.read_csv('data/aa_news.csv')
    df_tweets = pd.read_csv('data/combined_dataset.csv')
    save_to_db(df_news, 'news')
    save_to_db(df_tweets, 'tweets')
