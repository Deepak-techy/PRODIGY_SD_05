import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

url = "https://www.flipkart.com/search?q=android+mobile+under+30000&as=on&as-show=on&otracker=AS_Query_HistoryAutoSuggest_1_2_na_na_na&otracker1=AS_Query_HistoryAutoSuggest_1_2_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=android+mobile+under+30000&requestId=5f338ca4-923f-4534-bd19-3346c51c85bc&as-searchtext=an"

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
]

headers = {
    'User-Agent': random.choice(user_agents),
    'Referer': 'https://www.flipkart.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive'
}

flipkart_data = {
    'Title' : [],
    'Original Price' : [],
    'Discounted Price' : [],
    'Discount %' : [],
    'Ratings' : []
}

count = 0
max_entries = 24

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    titles = soup.find_all("div", class_="KzDlHZ")
    for title in titles:
        flipkart_data['Title'].append(title.string)

    org_prices = soup.find_all("div", class_="yRaY8j ZYYwLA")
    for org_price in org_prices:
        flipkart_data['Original Price'].append(org_price.text)

    dis_prices = soup.find_all("div", class_="Nx9bqj _4b5DiR")
    for dis_price in dis_prices: 
        flipkart_data['Discounted Price'].append(dis_price.string)

    dis_percentages = soup.find_all("div", class_="UkUFwK")
    for dis_percentage in dis_percentages:
        dis_percent = dis_percentage.string.split()[0].strip()
        if count < max_entries:
            flipkart_data['Discount %'].append(dis_percent)
            count+=1

    ratings = soup.find_all("span", class_="Wphh3N")
    for rating in ratings:
        if rating:
            rating_text = rating.text.strip()
            rating_info = rating_text.split("&")[0].strip()
            rating = rating_info.split()[0]
            flipkart_data['Ratings'].append(rating)

    df = pd.DataFrame.from_dict(flipkart_data)
    df.to_csv("flipkart mobile data.csv", index=False)

    print("Data stored in csv file successfully!!!")

except requests.exceptions.RequestException as err:
    print("An Error occured: ",err)







