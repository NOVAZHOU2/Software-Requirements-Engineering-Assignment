from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

def work(url, page_limit=10):
    links = []
    for page in range(1, page_limit + 1):
        page_url = f"{url}&p={page}"
        driver.get(page_url)
        time.sleep(3)
        job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/CC"]')
        for job_element in job_elements:
            href = job_element.get_attribute('href')
            if href:
                links.append(href)

    driver.quit()
    return links


if __name__ == "__main__":
    base_url1 = "https://www.zhaopin.com/sou/?jl=530&kw=数据分析"
    #base_url2 = "https://www.zhaopin.com/sou/jl530/kwA5K6G22TSLT0MNG8/p1"
    #base_url3 = "https://www.zhaopin.com/sou/jl530/kw9QJL9GBUPTQ0C/p1"
    job_links = work(base_url1, page_limit=15)
    with open("job_links3.txt", "w") as f:
        for link in job_links:
            f.write(link + "\n")

