
Clone the project

```bash
  git clone https://github.com/aritespit/aritespit
```

Go to the project directory

```bash
  cd aritespit
```


Enter your environmental variables for MySQL connection in ".env" file:

```bash
DB_HOST=<your DB_HOST>
DB_USER=<your DB_USER>
DB_PASSWORD=<your DB_PASSWORD>
```
Install dependencies

```bash
  pip install -r requirements.txt
```
## Run Locally
Execute the script to create the database
```bash
  python create_db.py 
```

Start the app

```bash
  python app.py
```


## Running Tests

You can scrape the data manually with the following scripts:

1) To collect Twitter data manually execute,
```bash
  python scrapers/tweet_scrap.py
```
2) To collect Anadolu Ajansı data manually execute,
```bash
  python scrapers/aa_scraper.py
```
