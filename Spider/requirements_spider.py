from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import numpy as np
from PIL import Image
driver = webdriver.Chrome()
stopwords = set(['的', '和', '有', '与', '在', '为', '等', '及', '对', '或', '是', '与'])

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    words = jieba.lcut(text)
    words = [word for word in words if word not in stopwords and len(word) > 1]
    return ' '.join(words)

def extract_job_requirements(urls):
    requirements = []
    for url in urls:
        driver.get(url)
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(), '要求') or contains(text(), '资格')]")
                )
            )

            job_requirements_elements = driver.find_elements(By.XPATH,
                                                             "//*[contains(text(), '要求') or contains(text(), '资格')]/following-sibling::*")
            job_requirements = "\n".join([element.text for element in job_requirements_elements if element.text])
            if job_requirements:
                requirements.append(clean_text(job_requirements))

        except Exception as e:
            print(f"在页面 {url} 中无法找到相关要求内容: {e}")

    return requirements


with open("job_links.txt", "r") as file:
    job_links = [line.strip() for line in file]

job_requirements = extract_job_requirements(job_links)


with open("cleaned_job_requirements.txt", "w", encoding="utf-8") as f:
    for requirement in job_requirements:
        f.write(requirement + "\n")

def extract_keywords(texts):
    vectorizer = TfidfVectorizer(max_features=50)
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.sum(axis=0).A1
    keywords = dict(zip(feature_names, scores))
    return keywords

keywords = extract_keywords(job_requirements)
mask_image = np.array(Image.open("img.png"))

def create_wordcloud(keywords):
    wordcloud = WordCloud(
        font_path='simhei.ttf',
        background_color='white',
        mask=mask_image,
        width=1600,
        height=1600,
        min_font_size = 2
    ).generate_from_frequencies(keywords)

    plt.figure(figsize=(20, 20))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()


create_wordcloud(keywords)



