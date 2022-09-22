s = "Тебе предстоит:  Разработка веб-приложений и сервисов на платформе .NET с применением языка C#; Интеграция системы с другими внутренними проектами.  Мы будем рады рассмотреть твою кандидатуру, если у тебя есть:​​​​​​​  Отличные знания C#, ASP.NET MVC, ASP.NET WebAPI, ASP.NET Core (BCL, асинхронность, современные фреймворки и библиотеки); Опыт проектирования и разработки многопоточных многоуровневых систем, в особенности, в .NET; Опыт разработки веб-сервисов, Windows Service Хороший опыт использования MS SQL Server и NoSQL; Знания методологий разработки, ООП, принципов SOLID паттернов проектирования и рефакторинга; Понимание и знание тонкостей ключевых интернет архитектур, технологий, протоколов и форматов, таких как TCP/IP, HTTP, AJAX, XML, JSON, WSDL, REST и т.п. Опыт работы с системами контроля версий исходного кода (Git); Опыт написания интеграционных и unit-тестов.  Что мы предлагаем:​​​​​​​  Непосредственное участие в разработке уникальных продуктов; работа в современной гибкой среде, где есть возможность самостоятельно принимать решения; дружеская открытая атмосфера, где приветствуется инициативность и поощряется нестандартный подход; развитие через новые и сложные задачи; постоянное саморазвитие и обучение; Beefree — гибкий рабочий график и возможность работать удаленно — планируй свое время сам; полис добровольного медицинского страхования, обслуживаемый в лучших клиниках города; служебная сотовая связь."
from nlp_rake import Rake
import nltk
from nltk.corpus import stopwords
# nltk.download("stopwords")


stops = list(set(stopwords.words("russian")))
adverbs = [x.replace("\n", "") for x in open("data/adverbs.txt", encoding="utf-8").readlines()]
adjective = [x.replace("\n", "") for x in open("data/adjective.txt", encoding="utf-8").readlines()]
stops.append(adverbs)
stops.append(adjective)

import pymorphy2
morph = pymorphy2.MorphAnalyzer()

s = " ".join([morph.normal_forms(w)[0] for w in s.split()])
print(s)


rake = Rake(stopwords=stops, max_words=3)
print(rake.apply(s)[:10])

import yake
extractor = yake.KeywordExtractor (
    lan="ru",      # язык
    n=3,           # максимальное количество слов в фразе
    dedupLim=0.3,  # порог похожести слов
    top=10         # количество ключевых слов
)

print(sorted(extractor.extract_keywords(s), key=lambda x: x[1]))

from summa import keywords
text_clean = ""
# уберем стоп-слова
for i in s.split():
    if i not in stops:
        text_clean += i + " "
print(keywords.keywords(text_clean, language="russian").split("\n"))

