import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"})
    links = pagination.find_all("a")
    pages = []
    for page in links[:-1]:
        pages.append(int(page.text))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    job_id = html["data-jobid"]
    title = html.find("h2", {"class": "mb4 fc-black-800 fs-body3"}).a.string
    company_raw = html.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).text
    company_raw = ''.join(company_raw.splitlines())
    company_raw = company_raw.split(" • ")
    company = company_raw[0].strip()
    link = f'https://stackoverflow.com/jobs/{job_id}/?so=i&q=python&r=true'

    return {
        "title": title,
        "company": company,
        "url": link
    }


def extract_jobs(last_page,url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping So page : {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})

        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?r=true&q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page,url)
    return jobs