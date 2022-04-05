import requests
from bs4 import BeautifulSoup
import re




def get_url(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.select("h2 > a")
    urls = []
    for a in pagination:
        if a["href"][-3:] != "rss":
            url = "https://weworkremotely.com" + a["href"]
            urls.append(url)
    return urls


def extract_job(html):
    urls = html.find_all("a", attrs={'href': re.compile("^/remote-jobs/")})
    for url in urls:
        url = url.get("href")
        url = "https://weworkremotely.com" + url
    titles = html.find_all("span", {"class": "title"})
    for title in titles:
        title = title.text
    companies = html.find_all("span", {"class": "company"})
    for company in companies:
        company = company.text

    return {"title": title, "company": company, "url": url}


def extract_jobs(urls):
    jobs = []

    for url in urls:
        print("Scrapping wwr page : " + url)
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.select("ul > li.feature")
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={word}"
    urls = get_url(url)
    jobs = extract_jobs(urls)
    return jobs
