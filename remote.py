import requests
from bs4 import BeautifulSoup
import re

def extract_job(html):
  urls=[]
  titles=[]
  companies = []
  job_list = []
  url_raw = html.find_all("tr", attrs={'data-href': re.compile("^/remote-jobs/")})
  for url in url_raw:
    url = url.get("data-href")
    url = "https://remoteok.com" + url
    urls.append(url)
  title_raw =  html.find_all("h2", {"itemprop":"title"})
  for title in title_raw:
     title = title.text
     title = title.replace("\n","")
     titles.append(title)
  companies_raw =  html.find_all("h3", {"itemprop":"name"})
  for company in companies_raw:
     company = company.text
     company = company.replace("\n","")
     companies.append(company)
  for i in range(len(urls)):
    job_dict = {}
    for i in range(len(urls)):
      job_dict["title"] = titles[i]
      job_dict["company"] = companies[i]
      job_dict["url"] = urls[i]
    job_list.append(job_dict)
  return job_list


def extract_jobs(URL,header):
  print(f"Scrapping remote page")
  jobs = []
  result = requests.get(URL,headers = header)
  soup = BeautifulSoup(result.text, "html.parser")
  results = soup.select("table",{"id":"jobsboard"})
  for result in results:
    job = extract_job(result)
    jobs.append(job)
  return jobs


def get_jobs(word):
    URL = f"https://remoteok.io/remote-dev+{word}-jobs"
    header = {'user-agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
    jobs = extract_jobs(URL,header)
    return jobs