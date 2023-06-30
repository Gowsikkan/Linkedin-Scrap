from turtle import pos
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup 
import requests
import time
import pandas as pd
import getpass

# Get Webdriver path, username and password
PATH ="C:/Users/HP/Documents/Scrapping/chromedriver.exe"
USERNAME = input("Enter Username: ")
PASSWORD = getpass.getpass("Enter your password: ")

# Use driver to open the link
driver = webdriver.Chrome()

driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)

# Use login credentials to login
email=driver.find_element(By.ID,"username")
email.send_keys(USERNAME)
password=driver.find_element(By.ID,"password")
password.send_keys(PASSWORD)
time.sleep(3)
password.send_keys(Keys.RETURN)


def url(page_link):
    driver.get(page_link)
    time.sleep(40)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    profile_cards = soup.find_all('li', class_='reusable-search__result-container')
    
    profile_url=[]
    for link in profile_cards:
        profile_link = link.find('a', class_="app-aware-link") 
        if profile_link:
            profile_url.append(profile_link['href'])

    return(profile_url)
    
        
def datas(profile_url,data):
    
    for url in profile_url:
        company_name = ''  
        position_name=''
        phone_number=''
        email_id=''
    
        url_without_query = url.split('?')[0]
        details_url = url_without_query + '/details/experience'
        driver.get(details_url)
        time.sleep(5)
        
        name = url[url.rfind('/') + 1:url.rfind('?')]
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(5)

        company_section = soup.find('span', {'class': 't-14 t-normal'})
        position_section = soup.find('div', {'class': 'display-flex full-width'})

        if company_section is not None:
            company_name = company_section.find('span').text.strip()
        
        if position_section is not None:
            position_name = position_section.find('span').text.strip()


        info_url = url_without_query + '/overlay/contact-info/'
        driver.get(info_url)
        time.sleep(3)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        time.sleep(5)

        email_section = soup.find('section', {'class': 'pv-contact-info__contact-type ci-email'})
        phone_section=soup.find('section',{'class':'pv-contact-info__contact-type ci-phone'})

        if email_section is not None:
            email_id=email_section.find('a',{'class':"pv-contact-info__contact-link link-without-visited-state t-14"}).text.strip()
        time.sleep(5)

        if phone_section is not None:
            phone_number=phone_section.find('span',{'class':'t-14 t-black t-normal'}).text.strip()
        time.sleep(5)

        data.append([name,company_name,position_name,phone_number,email_id,url])
    return data

def to_excel(data):
    column_names = ['Name', 'Company', 'Position', 'Phone_Number','Email','Url']
    df = pd.DataFrame(data, columns=column_names)
    excel_file_path = 'C:/Users/HP/Documents/Scrapping/output.xlsx'
    df.to_excel(excel_file_path, index=False)


if __name__ == "__main__":
    data=[]
    for i in range(1,10):
        page_link="https://www.linkedin.com/search/results/people/?keywords=coimbatore%20institute%20of%20technology&origin=SWITCH_SEARCH_VERTICAL&page={}&searchId=48f08485-80da-416d-a9b8-33cc9422efd0&sid=K%3BD".format(i)         
        response = requests.get(page_link)
        if response.status_code == 200:
            urls=url(page_link)
            data=datas(urls,data) 
        else:
            print(f"Error accessing page: {page_link}")
            break
    to_excel(data)
    print("Data saved to Excel file:", 'C:/Users/HP/Documents/Scrapping/output.xlsx')