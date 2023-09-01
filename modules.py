"""
Created on Fri Sep  1 01:47:18 2023

@author: Kiiro Tenshi
"""

import requests, json
from datetime import datetime, timezone, timedelta
import statistics
import constants

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
    response = json.loads(requests.get(f'https://xivapi.com/search?string={item_name}').text)['Results']
    response = [x for x in response if x[constants.URL_TYPE] == constants.RECIPE_TYPE]
    ids = {}
    for result in response:
        ids[result['Name']] = result['ID']
    item_id = ids[item_name]
    return str(item_id)

def fetch_recipe_data(recipe_id):
    response = json.loads(requests.get(f'https://xivapi.com/recipe/{recipe_id}?').text)
    '''Notepad time, each mat may contain a subrecipe, so treat it as a tree rooted at the requested item and work down
    from there, if there is no result returned then assume it is a raw material and stop there'''
    ingredients_quantity = {}
    ingredients_cost = {}
    base_recipe_name = response[constants.ENG_NAME]
    recipe_data_cost = {}
    recipe_data_quantity = {}
    for i in range(constants.MAX_QUANTITY_INGREDIENTS):
        if response[constants.ITEM_INGREDIENT + str(i)] is not None:
            idx_item_id = response[constants.ITEM_INGREDIENT + str(i)][constants.ITEM_ID]
            item_name = response[constants.ITEM_INGREDIENT + str(i)][constants.ENG_NAME]
            item_price = fetch_item_price(idx_item_id, constants.TIME_UNIVERSALIS)
        else:
            idx_item_id = -1
            item_name = constants.ITEM_NONE
            item_price = -1  # Set a default price for missing items
        ingredients_quantity[item_name] = response[constants.AMOUNT_INGREDIENT + str(i)]
        ingredients_cost[item_name] = item_price
    recipe_data_cost[base_recipe_name] = ingredients_cost
    recipe_data_quantity[base_recipe_name] = ingredients_quantity
    
    return recipe_data_cost, recipe_data_quantity

'''
def fetch_recipe_recursive(recipe_id):
    # base case - raw mat nowhere to go

    # recursive case - we gonna go layer by layer in the tree, so for each node in this layer run this function
    # append the name cost dict for each separate item, see materials_dict for an example
'''

def fetch_item_price(item_id, time_window_minutes):
    world_list = ['Jenova', 'Adamantoise', 'Cactuar', 'Faerie', 'Gilgamesh', 'Midgardsormr', 'Sargatanas', 'Siren']
    price_dict = {}
    for world in world_list:
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
    return price_dict

if __name__ == '__main__':
    #item_id = get_item_id('Ovibos Milk')
   #price_dict = fetch_item_price(item_id, 30)
    fetch_recipe_data(get_recipe_id("Baked Eggplant"))
    get_item_name(35593)