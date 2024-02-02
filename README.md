(![Vq3qKv4-removebg-preview (1)](https://github.com/aritespit/aritespit/assets/64483224/0ab01a40-0851-43cc-bb61-2523434e7056)
)


# Yeni Medya Çağında İçerik Keşfi ve Dinamik Haberleştirme

A brief description of what this project does and who it's for


## Run Locally

Clone the project

```bash
  git clone https://github.com/aritespit/aritespit
```

Go to the project directory

```bash
  cd aritespit
```

Install dependencies

```bash
  pip install -r requirements.txt
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

Start the app

```bash
  python app.py
```


## Running Tests

You can scrape the data manually with the following scripts:

1) To collect twitter data manually execute,
```bash
  python scrapers/tweet_scrap.py
```
2) To collect Anadolu Ajansı data manually execute,
```bash
  python scrapers/aa_scraper.py
```

