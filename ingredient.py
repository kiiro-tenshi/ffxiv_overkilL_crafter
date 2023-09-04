class Ingredient:
    def __init__(self, recipe_id, item_id, quantity, price, name, parent=None):
        self.recipe_id = recipe_id #if no recipe id (as -1), it is a leaf node
        self.item_id = item_id # use as identifier
        self.quantity = quantity
        self.price = price
        self.name = name
        self.children = []
        self.parent = parent

    def add_child_predefined(self, child):
        if child is not None:  # Check if child is not None
            child.parent = self
            self.children.append(child)
        
    def add_child(self, recipe_id, item_id, quantity, price, name, parent):
        new_child = Ingredient(recipe_id, item_id, quantity, price, name, parent=self)
        self.children.append(new_child)

    def print_tree(self, indent=""): #DFS? idk
        if self.parent is None:
            parent = "Root"
        else:
            parent = self.parent.name
        print(f"{indent}{self.name}, Item ID: {self.item_id}, Recipe ID: {self.recipe_id}, Quantity: {self.quantity}, Price: {self.price}, Parent: {parent}\n")
        for child in self.children:
            child.print_tree(indent + "       ") 