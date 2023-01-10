import re
import requests
import bs4
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd


skills = ['NoSQL','SQL','MySQL','Spark','PySpark','CSS','HTML','Bootstrap','Dash','Plotly',' R ',
          'Tableau','Excel','GraphQL','Snowflake','ETL','Pytorch','PySpark','PyCharm','ETL','CRUD',
          'Tensorflow','AWS','Flask','Django','API','REST','Java','JavaScript','C#','C++','Azure']


#a range to sort the pagination on linkedin at the end of the url
page = range(0,975,25)

#create an empty list to store jobID numbers
jobID = []

for num in page:
  
    #this is the url provided when "python" is searched as the only keyword with remote only roles filtered. 
    newurl = f'https://www.linkedin.com/jobs/search/?currentJobId=3423339110&f_WT=2&keywords=python&refresh=true&start={num}'
    
    #make the request from linkedin
    r = requests.get(newurl)
    
    #parse the request and create first soup
    doc = BeautifulSoup(r.text, "html.parser")
    
    #find the class containing a job id
    box = doc.find_all('div',class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    
    #use regular expressions to find the text "jobPosting: + 10 numbers" inside the string format of the box
    for match in re.finditer('jobPosting:\d{10}',str(box)):
      
        #append each job id number to the jobID list after stripping the "jobPosting:" text
        jobID.append(match.group().replace('jobPosting:',''))
        
####################################################
#create an empty string to store the job descriptions        
bigsoup = ''

for num in jobID:
  
    #for every jobID in the JobID list, go to the individual job listing page.
    url = f'https://www.linkedin.com/jobs/view/{num}/'
    
    r = requests.get(url)
    doc = BeautifulSoup(r.text, "html.parser")
    
    #create the soup and find the description class
    description = str(doc.find_all('div',class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5'))
    
    #the bigsoup variable is one massive string containing every job description in the search results. 
    bigsoup += description        

#######################################################
#create an empty list to store the counts 
counts = []

for item in skills:
    counts.append(bigsoup.count(item))
    
pd.Series(counts,skills)
