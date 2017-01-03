# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:51:26 2017
Creating a module that will output top stories on NPR's Politics page and summaries of each article. 
Will use bs4 and a text summarization module.
@author: Ibrahim Taher
"""

from bs4 import BeautifulSoup
import requests
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in

base_url = 'http://www.npr.org/sections/'

def get_section_page(section_url):
    """
    Gets the section page needed for printing headlines. Returns the html.
    """
    url = base_url + section_url
    #Request Page
    response = requests.get(url)
    html = response.text.encode('utf-8')
    return html

def parse_section_page(html):
    """
    Parses the headlines returned by html in get_section page().
    Will request url of each headline and return a summary using a text 
    summarization module.
    """
    soup=BeautifulSoup(html,'html.parser')
    headlines = soup.select('article')
    for headline in headlines:
        name = headline.find('img')
        if name==None:
            continue
        name=name.get('alt')#gets headline title
        print(name)
        print('')
        url=headline.find('a')
        url=url['href']#gets link to article
        response = requests.get(url)
        html = response.text.encode('utf-8')
        get_summary(html)

def get_summary(html):
    """
    Uses sumy, a python module for automatic summarization, to create a 5 
    sentence summary of articles on NPR politics page.
    """
    soup=BeautifulSoup(html,'html.parser')
    text=soup.find_all('p',{'class':None},{'dir':None})#finds article text
    s=''
    for line in text:
        #Removes About from text
        if line.get_text()=='The Two-Way is the place to come for breaking news, analysis and for stories that are just too interesting – or too entertaining – to pass up. Get in touch with your questions, comments and leads.':
            continue
        #Removes captions from text
        if 'hide caption' in line.get_text():
            continue
        s+=line.get_text()
    #Uses LexRankSummarizer to create 5 sentence summary of text.
    parser = PlaintextParser.from_string(s, Tokenizer('English'))
    summarizer=LexRankSummarizer()
    summary=summarizer(parser.document,5)
    for sentence in summary:
        print(sentence)
        
html=get_section_page('politics')
parse_section_page(html)



    
    