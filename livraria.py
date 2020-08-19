import requests
from bs4 import BeautifulSoup
# Import MongoClient from pymongo so we can connect to the database
from pymongo import MongoClient

if __name__ == '__main__':
    # Instantiate a client to our MongoDB instance
    db_client = MongoClient()
    libreria = db_client.libreria
    libreria = libreria.posts


    response = requests.get("https://www.livraria-ec.com/juvenil")
    soup = BeautifulSoup(response.content, "lxml")

    post_titles = soup.find_all("a", class_="_34sIs")

    extracted = []
    for post_title in post_titles:
        extracted.append({
            'title' : post_title.text,
            'link'  : "https://www.livraria-ec.com/juvenil" + post_title['href']
        })

    for post in extracted:
        if db_client.libreria.libreria.find_one({'link': post['link']}) is None:
            print("Found a new listing at the following url: ", post['link'])
            db_client.libreria.libreria.insert(post)