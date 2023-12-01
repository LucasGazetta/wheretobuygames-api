from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import json

def create_search_url(game_name):
    search_term = "+".join(game_name.split())
    return f"https://store.steampowered.com/search/?term={search_term}"

def create_search_url_epic(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://store.epicgames.com/browse?q={search_term}"

def create_search_url_nuuvem(game_name):
    search_term = "+".join(game_name.split())
    return f"https://www.nuuvem.com/br-pt/catalog/page/1/search/{search_term}"

def create_search_url_gmg(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://www.greenmangaming.com/pt/search/?query={search_term}"

def create_search_url_gog(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://www.gog.com/en/games?query={search_term}"
    
def create_search_url_instant_gaming(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://www.instant-gaming.com/pt/pesquisar/?q={search_term}"

def create_search_url_eneba(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://www.eneba.com/store/all?text={search_term}"

def scrape_steam_search(game_name):
    url = create_search_url(game_name)
    print(f"URL da Steam: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('a', class_='search_result_row')
    if not first_item:
        return "Not Found"

    title_tag = first_item.find('span', class_='title')
    title = title_tag.text if title_tag else "Título não encontrado"

    price_tag = first_item.find('div', class_='discount_final_price')
    price = price_tag.text if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_epic_search(game_name):
    url = create_search_url_epic(game_name)
    print(f"URL da Epic: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results_container = soup.find('div', class_='css-sbt18p')
    if not results_container:
        return "Not Found"

    first_item = soup.find('li', class_='css-lrwy1y')

    if not first_item:
        return "Not Found"

    title_tag = first_item.find('div', class_='css-rgqwpc')
    title = title_tag.text if title_tag else "Título não encontrado"

    price_tag = first_item.find('span', class_='css-119zqif')
    price = price_tag.text if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_nuuvem_search(game_name):
    url = create_search_url_nuuvem(game_name)
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('div', class_='product__available')

    if not first_item:
        return "Not Found"

    title_tag = first_item.find('h3', class_='product-title')
    title = title_tag.text if title_tag else "Título não encontrado"

    price_integer_tag = first_item.find('span', class_='integer')
    print(price_integer_tag)
    price_decimal_tag = first_item.find('span', class_='decimal')
    print(price_integer_tag.string)
    
    if price_integer_tag and price_decimal_tag:
        price_integer = price_integer_tag.string
        price_decimal = price_decimal_tag.string
        price = f"R${price_integer}{price_decimal}"
    else:
        price = "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_gmg_search(game_name):
    url = create_search_url_gmg(game_name)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('li', class_='ais-Hits-item')
    if not first_item:
        return "Not Found"

    title_tag = first_item.find('p', class_='prod-name')
    title = title_tag.text.strip() if title_tag else "Título não encontrado"

    price_tag = first_item.find('span', class_='current-price')
    price = price_tag.text.strip() if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_gog_search(game_name):
    url = create_search_url_gog(game_name)
    print(f"URL da GOG: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('product-tile', class_='ng-star-inserted')
    if not first_item:
        return "Not Found"

    title_tag = first_item.find('div', class_='product-tile__title')
    title = title_tag.text.strip() if title_tag else "Título não encontrado"

    price_tag = first_item.find('span', class_='final-value')
    price = price_tag.text.strip() if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_instant_gaming_search(game_name):
    url = create_search_url_instant_gaming(game_name)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('div', class_='item')
    if not first_item:
        return "Not Found"

    title_tag = first_item.find('span', class_='title')
    title = title_tag.text.strip() if title_tag else "Título não encontrado"

    price_tag = first_item.find('div', class_='price')
    price = price_tag.text.strip() if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def scrape_eneba_search(game_name):
    url = create_search_url_eneba(game_name)
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('div', class_='pFaGHa')
    if not first_item:
        return "Not Found"

    title_tag = first_item.find('span', class_='YLosEL')
    title = title_tag.text.strip() if title_tag else "Título não encontrado"

    price_tag = first_item.find('span', class_='L5ErLT')
    price = price_tag.text.strip() if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price, 'url': url}

def game_search_view(request, game_name):
    steam_results = scrape_steam_search(game_name)
    epic_results = scrape_epic_search(game_name)
    nuuvem_results = scrape_nuuvem_search(game_name)
    gmg_results = scrape_gmg_search(game_name)
    gog_results = scrape_gog_search(game_name)
    ig_results = scrape_instant_gaming_search(game_name)
    eneba_results = scrape_eneba_search(game_name)
    
    combined_results = {
        'Steam': steam_results,
        'Epic Games': epic_results,
        'Nuuvem': nuuvem_results,
        'Green Man Gaming': gmg_results,
        'GoG': gog_results,
        'Instant Gaming': ig_results,
        'Eneba': eneba_results
    }

    return JsonResponse(combined_results)
