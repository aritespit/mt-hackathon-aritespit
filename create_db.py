import os
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, inspect, text
import sqlalchemy
import time
def get_credentials():
    """
    Function to get the database credentials from the .env file.
    """
    load_dotenv()

    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_database = os.getenv("DB_DATABASE")
    print(db_host)
    return db_host, db_port, db_user, db_password, db_database

def create_db():
    """
    Function that creates the database if it does not exist.
    """
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
    """
    Function that saves the DataFrame to the specified table in the database. Handles duplicates and adds additional columns.
    Args:
        df (DataFrame): the DataFrame to save
        table_name (str): the name of the table to save the DataFrame to
    """
    # get credentials
    db_host, db_port, db_user, db_password, db_database = get_credentials()

    try:
        engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}')           
        # add additional columns
        if table_name == "tweets":
            additional_columns = {'is_generated': 0, 'news': ""}
        else:
            additional_columns = {'summary': ""}
        df = df.assign(**additional_columns)
        # remove duplicates
        if sqlalchemy.inspect(engine).has_table(table_name):
            print("inner loop boop")
            query = text(f'SELECT DISTINCT Content FROM {table_name}')
            existing_records = pd.read_sql_query(query, con=engine.connect())
            df = df[~df['Content'].isin(existing_records['Content'])]
            print(len(df))
        # save to db
        if not df.empty:
            # append to table
            print(df.columns)
            df.to_sql(table_name, con=engine, if_exists='append', index=True)

            engine.dispose()
            # last fetched time to show it on frontend
            last_fetched_time = time.strftime('%Y-%m-%d %H:%M:%S')
            with open(f'data/last_fetched_time_{table_name}.txt', 'w') as file:
                file.write(last_fetched_time)
                print(last_fetched_time)

            print(f"DataFrame saved to '{table_name}'.")
        else:
            print("No new records to save.")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == '__main__':
    create_db()
    df_news = pd.read_csv('data/aa_news.csv')
    df_tweets = pd.read_csv('data/combined_tweets.csv')
    save_to_db(df_news, 'news')
    save_to_db(df_tweets, 'tweets')
