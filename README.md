<p align="center">
  <img src="static/images/imgur.png" alt="Resim Açıklaması">
</p>

# Instant Content Tracking and Reporting in the New Media Age
New media has become one of the most important resources for media organizations today. As the ArıTespit team, we have developed an artificial intelligence-supported project that allows instant content monitoring and reporting of accounts determined by journalists in the new media. Our project also facilitates the work of journalists by converting news texts into new media content.

## Group Members

- Berfin Duman [berfinduman](https://www.github.com/berfinduman)
- Can Günyel [cangunyel](https://www.github.com/cangunyel)
- Oğuz Ali Arslan [oguzaliarslan](https://www.github.com/oguzaliarslan)
- Ömer Bera Dinç [Supomera](https://www.github.com/Supomera)
  
## Run Locally
Step by step [Instruction](https://github.com/aritespit/aritespit/blob/main/deployment.md)

## Presentation
Presentation can be accessed from the following [link](https://www.canva.com/design/DAF7pu5hD7g/fGEsAxh9rn0sDVb0XHBSpA/edit?utm_content=DAF7pu5hD7g)

## Demo
### Problem 1
This project keeps the instant shares of reliable sources (ministers, state institutions...) in new media in a database and produces news from selected contents. In this way, we make it easier for reporters to follow the content in new media. A demo video for this problem is shown below.

https://github.com/aritespit/aritespit/assets/73332933/baf19403-237a-4f82-8a81-24e396a812d7

The database is shown on the left side. Followed accounts can be managed by the button (shown first in the video). There is a color coding that indicates submitted news. If any news is submitted, it turns the tweet block to green from yellow. After submitting news, new commands can be given by "Komut Gir" button. Also submitted news can be shown afterwards with "Haberi Görüntüle" button. Last but not least, if there is a picture on the tweet there is an icon to see that picture. 

### Problem 2
This project also transforms existing news into a new media format. We help reporters working in the new media team to find interesting spots, especially for X, with our suggestions. A demo video for this problem is shown below as well.

https://github.com/aritespit/aritespit/assets/73332933/83f098ae-5288-4716-9bbd-e0b6a87fa269

Interfaces of X > news, and news > X are similar. Here using "Özetle" button, suggestions are being made. 

## State of Art
Unedited news examples were needed for our project, and since we couldn't find this data in any available source and the hackathon didn't provide it, we had to start without a dataset. In the absence of a dataset, using a Language Model (LLM) would be the most suitable approach. After experimenting with Mistral models with different quantizations, StableLM, and LLaMa, and spending time on them, we conducted trials with GPT3.5 and ChatGPT4 provided by the hackathon. Since we achieved the most favorable results for our goal with GPT3.5, we continued our work on this model.

Normally, we evaluate the success of models based on metrics such as F1 score, precision, recall, etc. with the help of test datasets. However, in the case of Language Models (LLMs), this approach is not applicable. Instead, we decided on the success of the models by considering Inference Speed as a numerical magnitude and assessing the relevance of the outputs to the purpose and the way the media sector operates. 

![image](https://github.com/aritespit/aritespit/assets/73332933/0246c24e-ed60-42c6-90c5-47fe03fb21a0)

We help reporters working in the new media team to find interesting spots, especially for X, with our suggestions.

## Future Enhancements

**Model Fine Tuning**:  Enhancing the accuracy of our LLM model to produce results more aligned with news formats and Turkish language rules by fine-tuning it with reduced hardware requirements using Parameter-efficient Fine-tuning (Peft) and Low-Rank Adaptation (Lora) methods.

**Subscription Package Development**:  Introducing subscription packages tailored to different fields, enabling our system to exclusively gather content in specified areas and generate news utilizing field-specific terminology.
