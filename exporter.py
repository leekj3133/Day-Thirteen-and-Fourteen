import csv

def save_to_file(jobs):
  file = open("jobs.csv", mode="w",encoding="utf-8")
  writer = csv.writer(file)
  writer.writerow(["Title","Compnay","Link"])
  for job in jobs:
    if type(job) is not list:
      writer.writerow(list(job.values()))
    else:
      writer.writerow(list(job))