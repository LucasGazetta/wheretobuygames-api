from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

def create_search_url(game_name):
    search_term = "+".join(game_name.split())
    return f"https://store.steampowered.com/search/?term={search_term}"

def create_search_url_epic(game_name):
    search_term = "%20".join(game_name.split())
    return f"https://store.epicgames.com/browse?q={search_term}"

def create_search_url_nuuvem(game_name):
    search_term = "+".join(game_name.split())
    return f"https://www.nuuvem.com/br-pt/catalog/page/1/search/{search_term}"

def scrape_steam_search(game_name):
    url = create_search_url(game_name)
    print(f"URL da Steam: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('a', class_='search_result_row')
    if not first_item:
        return "Nenhum resultado encontrado"

    title_tag = first_item.find('span', class_='title')
    title = title_tag.text if title_tag else "Título não encontrado"

    price_tag = first_item.find('div', class_='discount_final_price')
    price = price_tag.text if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price}

def scrape_epic_search(game_name):
    url = create_search_url_epic(game_name)
    print(f"URL da Epic: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    results_container = soup.find('div', class_='css-sbt18p')
    if not results_container:
        return "Nenhum container encontrado"

    first_item = soup.find('li', class_='css-lrwy1y')

    if not first_item:
        return "Nenhum resultado encontrado"

    title_tag = first_item.find('div', class_='css-rgqwpc')
    title = title_tag.text if title_tag else "Título não encontrado"

    price_tag = first_item.find('span', class_='css-119zqif')
    price = price_tag.text if price_tag else "Preço não encontrado"

    return {'title': title, 'price': price}

def scrape_nuuvem_search(game_name):
    url = create_search_url_nuuvem(game_name)
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')

    first_item = soup.find('div', class_='product__available')

    if not first_item:
        return "Nenhum resultado encontrado"

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

    return {'title': title, 'price': price}

def game_search_view(request, game_name):
    steam_results = scrape_steam_search(game_name)
    epic_results = scrape_epic_search(game_name)
    nuuvem_results = scrape_nuuvem_search(game_name)
    
    combined_results = {
        'steam': steam_results,
        'epic': epic_results,
        'nuuvem': nuuvem_results
    }

    return JsonResponse(combined_results)