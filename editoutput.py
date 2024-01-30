
import random

input_text = "Merkez Bankası Başkanı Erkan, Asılsız Haberlere Tepki Gösterdi \n Türkiye Cumhuriyeti Merkez Bankası Başkanı Hafize Gaye Erkan, son günlerde kişisel hedeflemelere ve bankaya yönelik kasıtlı haberlere karşı sert bir tepki gösterdi. \n Erkan \n 'Son günlerde şahsım ve ailemi hedef almak suretiyle, Bankamıza yönelik güven bozucu, kasıtlı ve gerçeklerle bağdaşmayan haberler dolaşıma sokulmuştur. Amerika Birleşik Devletleri'nde ekonomi ve iş dünyasının önemli isimleriyle gerçekleştirdiğimiz ve son derece verimli geçen görüşmeler sırasında öğrendiğim bu asılsız iddialar karşısında şaşkınlığımı ve üzüntümü kamuoyu ile özellikle paylaşmak isterim. Şahsımı ve Bankamızı itham eden asılsız haberler asla kabul edilemez niteliktedir. Sorumlular hakkında gerekli yasal haklarımı kullanacağım."

# Split the text by \n
words = input_text.split('\n')

# Get words
first_word=words[-3]
second_word = words[-2]

# Words to be merged with
mahrec = "(AA)"

second = ["X sosyal medya hesabından yaptığı paylaşımda şunları kaydetti:",
          "X sosyal medya hesabından yaptığı paylaşımda aşağıdaki ifadeleri kullandı:",
          "X sosyal medya platformunda paylaştığı gönderide şu sözleri yazdı:",
          "X sosyal medya hesabından habere ilişkin paylaşım yapıldı.",
          "X sosyal medya hesabından paylaşımda bulundu."]

#Merge
firstparagraph = mahrec + first_word
secondparagraph = second_word + random.choice(second)


# Result Control
#print(firstparagraph)
#print(secondparagraph)
#Prompt for this arrangement given below.
"""
You are a news assistant that turns the posts published by institutions, organizations or ministers on their social media accounts into news. You need to understand the context and convert it into a news format. The news format includes a headline (title), and a body part for the newly generated full text of the news. Body part has 3 paragraphs. First paragraph is the summary of tweet. Second paragraph must JUST write surname of the person if  text in parentheses indicates a person, second paragraph must JUST write full name of the ministry or organization if  text in parentheses indicates a ministry or organizational account. Lastly, third paragraph gives tweet and its' explanation. 

### Instruction:
The text in parentheses indicates which person, institution or organization gave the statement. Create news that contains title, and body parts meanwhile news format defined above. Replying in Turkish is a MUST, if your answer is going to be english translate it to Turkish


Example Input: İran Cumhurbaşkanı Sayın İbrahim Reisi’nin Ankara ziyareti öncesi İran Petrol Bakanı Sayın Javad Owji ve beraberindeki heyet ile Bakanlığımızda bir araya geldik.

Derin ilişkilere sahip olduğumuz İran ile enerji alanındaki iş birliğimizi daha da ileri taşıma konusundaki kararlılığımızı dile getirdik.

Özellikle doğal gaz alanında iş birliğimizi yeni dönemde daha geniş çerçevede ele alınması gerektiğini ifade ettik.

Example Output:
Bakan Bayraktar, İranlı mevkidaşı ile "enerji işbirliğini" görüştü 

ANKARA (AA) - Enerji ve Tabii Kaynaklar Bakanı Alparslan Bayraktar, İran Petrol Bakanı Javad Owji ile iki ülkenin enerji işbirliğine dair konuları ele aldı. 

Bayraktar

"Derin ilişkilere sahip olduğumuz İran ile enerji alanındaki işbirliğimizi daha da ileri taşıma konusundaki kararlılığımızı dile getirdik. Özellikle doğal gaz alanında işbirliğimizin yeni dönemde daha geniş çerçevede ele alınması gerektiğini ifade ettik."
-------------------------------------------------------------------------------
Now your input is:

"""