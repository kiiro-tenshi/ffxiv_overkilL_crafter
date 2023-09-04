"""
Created on Fri Sep  1 01:47:18 2023

@author: Kiiro Tenshi
"""

import requests, json
from datetime import datetime, timezone, timedelta
import statistics
import constants
from ingredient import Ingredient

def get_item_id(item_name):
    '''to get item id as universalis need item id for the get request'''
    response = json.loads(requests.get(f'https://xivapi.com/search?string={item_name}').text)['Results']
    response = [x for x in response if x[constants.URL_TYPE] == constants.ITEM_TYPE]
    ids = {}
    for result in response:
        ids[result['Name']] = result['ID']
    item_id = ids[item_name]
    return str(item_id)

def get_item_name(item_id):
    '''There should only be one item per item_id, so a list is never returned from the request.'''
    if item_id == -1:
        return constants.ITEM_NONE
    response = json.loads(requests.get(f'https://xivapi.com/item/{item_id}').text)[constants.ENG_NAME]
    return str(response)

def get_recipe_id(item_name):
    '''this *does* assume the item name is correct or unexpected behaviour may occur!'''
    try:
        response = json.loads(requests.get(f'https://xivapi.com/search?string={item_name}').text)['Results']
        response = [x for x in response if x[constants.URL_TYPE] == constants.RECIPE_TYPE]
        ids = {}
        for result in response:
            ids[result['Name']] = result['ID']
        item_id = ids[item_name]
        return str(item_id)
    except:
        return str(-1)

def fetch_recipe_data(recipe_id, get_recipe_id_func, fetch_item_price_func, get_item_id_func):
    def fetch_recipe(recipe_id):
        response = json.loads(requests.get(f'https://xivapi.com/recipe/{recipe_id}?').text)
        return response

    def minimize_price(price_dict):
        min_average_price = float('inf')
        min_server = None

        for server, stats in price_dict.items():
            num_transaction = stats['num_transaction']
            average_price = stats['average_price']
            
            if num_transaction > 0 and average_price < min_average_price:
                min_average_price = average_price
                min_server = server

        result = (min_server, min_average_price) if min_server else None
        return result

    def build_tree(recipe_id, item_id, quantity, parent=None):
        response = fetch_recipe(recipe_id)
        recipe_name = response[constants.ENG_NAME]
        assert str(item_id) == str(response[constants.ITEM_ID_RECIPE])
        price = minimize_price(fetch_item_price_func(item_id, constants.TIME_UNIVERSALIS))  
        current_ingredient = Ingredient(recipe_id, item_id, quantity, price, recipe_name, parent=parent)
        #go through the list of ingredients and add them as children
        for i in range(constants.MAX_QUANTITY_INGREDIENTS):
            if response[constants.ITEM_INGREDIENT + str(i)] is not None:
                idx_ingredient_name = response[constants.ITEM_INGREDIENT + str(i)][constants.ENG_NAME]
                idx_recipe_id = get_recipe_id_func(idx_ingredient_name)
                idx_amount_ingredient = response[constants.AMOUNT_INGREDIENT + str(i)]
                # if no recipe, manually add the ingredient here.
                idx_item_id = get_item_id_func(response[constants.ITEM_INGREDIENT + str(i)][constants.ENG_NAME])
                idx_price = minimize_price(fetch_item_price_func(idx_item_id, constants.TIME_UNIVERSALIS))
                if int(idx_recipe_id) == -1: #no recipe, add the ingredient.
                    current_ingredient.add_child(idx_recipe_id, idx_item_id, idx_amount_ingredient, idx_price, idx_ingredient_name, parent=current_ingredient)
                else:
                    next_child = build_tree(idx_recipe_id, idx_item_id, idx_amount_ingredient, parent=current_ingredient)
                    current_ingredient.add_child_predefined(next_child) 
        return current_ingredient
    response = fetch_recipe(recipe_id)
    item_id = response[constants.ITEM_ID_RECIPE]
    root = build_tree(recipe_id, item_id, 1)
    return root

def fetch_item_price(item_id, time_window_minutes):
    world_list = ['Jenova', 'Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Midgardsormr', 'Sargatanas', 'Siren']
    price_dict = {}
    for world in world_list:
        try:
            response = requests.get(f'https://universalis.app/api/v2/history/{world}/{item_id}').text
            json_response = json.loads(response)
            if 'lastUploadTime' not in json_response:
                price_dict[world] = {'num_transaction': 0, 'average_price': 0}
            else:
                last_upload_time = datetime.fromtimestamp(json_response['lastUploadTime']/1000, timezone.utc)
                time_window = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)
                if last_upload_time < time_window:
                    price_dict[world] = {'num_transaction': 0, 'average_price': 0}
                else:
                    entries = sorted(json_response['entries'], key=lambda x: x['timestamp'], reverse=True)
                    num_transaction = len(entries)
                    prices = [entry['pricePerUnit'] for entry in entries]
                    median_price = statistics.median(prices)
                    mad_price = statistics.median([abs(price - median_price) for price in prices])
                    filtered_prices = [price for price in prices if abs(price - median_price) <= 3*mad_price]
                    average_price = statistics.mean(filtered_prices)
                    price_dict[world] = {'num_transaction': num_transaction, 'average_price': average_price}
        except:
                price_dict[world] = {'num_transaction': -1, 'average_price': 0}
    return price_dict

if __name__ == '__main__':
    #item_id = get_item_id('Ovibos Milk')
   #price_dict = fetch_item_price(item_id, 30)
   #print(get_recipe_id("not an item!"))
    root = fetch_recipe_data(get_recipe_id("Baked Eggplant"), get_recipe_id, fetch_item_price, get_item_id)
    Ingredient.print_tree(root)
    print("----")
    #get_item_name(35593)