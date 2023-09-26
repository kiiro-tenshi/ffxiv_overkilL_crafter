class Ingredient:
    def __init__(self, recipe_id, item_id, quantity, price, name, parent=None, amount_result=1):
        self.recipe_id = recipe_id #if no recipe id (as -1), it is a leaf node
        self.item_id = item_id # use as identifier
        self.quantity = quantity
        self.price = price
        self.name = name
        self.amount_result = amount_result
        self.children = []
        self.parent = parent

    def add_child_predefined(self, child):
        if child is not None: 
            child.parent = self
            self.children.append(child)
        
    def add_child(self, recipe_id, item_id, quantity, price, name, parent, amt_res=1):
        new_child = Ingredient(recipe_id, item_id, (self.quantity * quantity), price, name, parent=self, amount_result=amt_res)
        self.children.append(new_child)

    def print_tree(self, indent=""):
        if self.parent is None:
            parent = "Root"
        else:
            parent = self.parent.name
        print(f"{indent}{self.name}, Item ID: {self.item_id}, Recipe ID: {self.recipe_id}, Quantity: {self.quantity}, Price: {self.price}, Parent: {parent}\n")
        for child in self.children:
            child.print_tree(indent + "       ")

    def to_dict_quantity(self):
        result = {
            self.name: {
                child.name: child.quantity
                for child in self.children
            }
        }

        if self.children:
            for child in self.children:
                child_dict = {
                    subchild.name: subchild.quantity
                    for subchild in child.children
                }
                if child_dict:
                    result[child.name] = child_dict
        return result
    
    def to_dict_price(self):
        result = {
            self.name: {
                child.name: [child.price[0], child.price[1]*child.quantity]# [1] is the actual price, [0] is the server.
                for child in self.children
            }
        }

        if self.children:
            for child in self.children:
                child_dict = {
                    subchild.name: [subchild.price[0], subchild.price[1]*subchild.quantity]
                    for subchild in child.children
                }
                if child_dict:
                    result[child.name] = child_dict
        result['crafted_quantity'] = self.amount_result
        return result
    
    def to_dict_server(self):
        result = {
            self.name: {
                child.name: child.price[0] # [1] is the actual price, [0] is the server.
                for child in self.children
            }
        }

        if self.children:
            for child in self.children:
                child_dict = {
                    subchild.name: subchild.price[0]
                    for subchild in child.children
                }
                if child_dict:
                    result[child.name] = child_dict

        return result