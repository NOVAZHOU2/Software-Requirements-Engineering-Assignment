from selenium import webdriver
import time
import re
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


driver = webdriver.Chrome()

def extract_salary_from_text(url):
    driver.get(url)
    time.sleep(5)

    page_text = driver.find_element("tag name", "body").text

    match = re.search(r"(\d+\.?\d*)万[-–](\d+\.?\d*)万", page_text)
    if match:
        low_salary = float(match.group(1)) * 10000
        high_salary = float(match.group(2)) * 10000
        avg_salary = (low_salary + high_salary) / 2
        return avg_salary
    else:
        print(f"未找到薪资信息，链接: {url}")
        return None

with open("job_links3.txt", "r") as file:
    job_links = [line.strip() for line in file]

salary_ranges = {
    "5000-10000": 0,
    "10000-15000": 0,
    "15000-20000": 0,
    "20000-25000": 0,
    "25000-30000": 0,
    "30000+": 0
}

for url in job_links:
    avg_salary = extract_salary_from_text(url)
    if avg_salary:
        if 5000 <= avg_salary < 10000:
            salary_ranges["5000-10000"] += 1
        elif 10000 <= avg_salary < 15000:
            salary_ranges["10000-15000"] += 1
        elif 15000 <= avg_salary < 20000:
            salary_ranges["15000-20000"] += 1
        elif 20000 <= avg_salary < 25000:
            salary_ranges["20000-25000"] += 1
        elif 25000 <= avg_salary < 30000:
            salary_ranges["25000-30000"] += 1
        else:
            salary_ranges["30000+"] += 1

driver.quit()

salary_labels = list(salary_ranges.keys())
job_counts = list(salary_ranges.values())

plt.figure(figsize=(10, 6))
plt.bar(salary_labels, job_counts, color='skyblue')
plt.xlabel("薪资区间 (元)")
plt.ylabel("工作数量")
plt.title("不同薪资区间的工作数量分布")
plt.show()


