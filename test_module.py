from modules import *
from crafting_graph import *

if __name__ == '__main__':
    #item_id = get_item_id('Ovibos Milk')
   #price_dict = fetch_item_price(item_id, 30)
   #print(get_recipe_id("not an item!"))
    root = fetch_recipe_data(get_recipe_id("Baked Eggplant"), get_recipe_id, fetch_item_price, get_item_id)
    Ingredient.print_tree(root)
    dictify = root.to_dict_quantity()
    dictify_price = root.to_dict_price()
    print("----")
    print(dictify)
    print("----")
    print(dictify_price)
    target_item = 'Baked Eggplant'
    groceries_list = find_cheapest_way(dictify_price, target_item, verbose=True)
    #get_item_name(35593)