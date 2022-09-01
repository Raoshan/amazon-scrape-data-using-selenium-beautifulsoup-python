import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    '''Generate a url from search term'''

    template = 'https://www.amazon.com/s?k={}&crid=12YKQBK6PO1CX&sprefix=ultra%2Caps%2C657&ref=nb_sb_ss_ts-doa-p_3_5'
    search_term = search_term.replace(' ','+')

    #add term query to url
    url = template.format(search_term)

    #add page query to placeholder
    url +='&page={}'

    return url


'''Generalize the pattern'''
def extract_record(item):
    atag = item.h2.a
    description = atag.text.strip()
    print(description)
    url = "https://www.amazon.com"+atag.get('href')
    print(url)
    try:
        price_parent = item.find('span',class_="a-price")
        price = price_parent.find('span',class_="a-offscreen").text
        print(price)
    except AttributeError:
        return
    try:
        rating = item.i.text
        print(rating)
        review_count = item.find('span',{'class':'a-size-base'}).text
        print(review_count)
    except AttributeError:
        rating = ''
        review_count = ''    

    result = (description,url,price,rating,review_count)

    return result

def main(search_term):
    """Run main program routine"""
    #Startup the webdriver
    driver = webdriver.Chrome("F:\\Web Scraping\\selenium\\chromedriver.exe")

    records = []
    url = get_url(search_term) 

    for page in range(1,21):
        driver.get(url.format(page))  
        soup = BeautifulSoup(driver.page_source,'html.parser')
        # print(soup.prettify)
        results = soup.find_all('div', {'data-component-type':'s-search-result'}) 
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)    

    driver.close()   

    """Save the data in csv file"""
    with open("results.csv", 'w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['description','url','price','rating','review_count'])
        writer.writerows(records)

main('ultrawide monitor')