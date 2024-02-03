
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
