<p align="center">
  <img src="static/images/imgur.png" alt="Resim Açıklaması">
</p>

# Instant Content Tracking and Reporting in the New Media Age
New media has become one of the most important resources for media organizations today. As the ArıTespit team, we have developed an artificial intelligence-supported project that allows instant content monitoring and reporting of accounts determined by journalists in the new media. Our project also facilitates the work of journalists by converting news texts into new media content.


## Run Locally

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

## State of Art
Unedited news examples were needed for our project, and since we couldn't find this data in any available source and the hackathon didn't provide it, we had to start without a dataset. In the absence of a dataset, using a Language Model (LLM) would be the most suitable approach. After experimenting with Mistral models with different quantizations, StableLM, and LLaMa, and spending time on them, we conducted trials with ChatGPT3.5 and ChatGPT4 provided by the hackathon. Since we achieved the most favorable results for our goal with ChatGPT3.5, we continued our work on this model.

Normally, we evaluate the success of models based on metrics such as F1 score, precision, recall, etc. with the help of test datasets. However, in the case of Language Models (LLMs), this approach is not applicable. Instead, we decided on the success of the models by considering Inference Speed as a numerical magnitude and assessing the relevance of the outputs to the purpose and the way the media sector operates. 

![image](https://github.com/aritespit/aritespit/assets/73332933/0246c24e-ed60-42c6-90c5-47fe03fb21a0)
