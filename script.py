# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:24:38 2019

@author: mKrT4
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
import os
 
#open all quotes' topics
html_doc = urlopen('https://citaty.info/tema').read() 
soup = BeautifulSoup(html_doc, features="lxml")


#collect urls of all topics' pages
urls = []
for link in soup.find_all('a'):
    if '/tema/' in link.get('href') or '/category/' in link.get('href'):
        url = 'https://citaty.info' + link.get('href')
        urls.append(url)
        
#remain unique urls
urls = list(set(urls))

def processing(result):
    def author(result_set):
        for element in result_set:
            if "Автор цитаты" in str(element) or "Цитируемый персонаж" in str(element):
                return (element.string)
            
            
    def stroke(result_set):
        for each in result_set:
            a = str(each.p)
            for link in each.find_all('a'):
                a = a.replace(str(link), link.string)
            
            if a != 'None' : return(re.sub(r"\<(.|.*)\>", '', a).replace('\xa0', ' '))
            
                
    quotes = []
    for q in result.find_all('div', 'node__content'):
        quotes.append([stroke(q.find_all('div', 'field-item even last')), author(q.find_all('div', 'field-item even'))])

    return (pd.DataFrame(quotes, columns = ['quote', 'author']).drop_duplicates())
    
def save_to_file(dataframe, name):
    try:
        # Create target Directory
        os.mkdir(name)
        print("Directory ", name, " Created ") 
    except FileExistsError:
        pass
    
    for index, row in dataframe.iterrows():
        global count 
        
        quotation = row[0] + "\n\n" + row[1]
        path = os.path.join(name, str(count) + ".txt")
        with open(path, "w", encoding="ansi") as text_file:
            text_file.write(quotation)
        
        count += 1

for url in urls:
    count = 1
    for page in range(0, 50):
        try:
            topic = urlopen(url + '?sort_by=rating&page=' + str(page)).read()
            result = BeautifulSoup(topic, features="lxml")
            save_to_file(processing(result), url.split('/')[-1])
        except:
            pass
