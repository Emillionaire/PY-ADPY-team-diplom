import pprint
import re
cook_book = {}

with open('rec.txt', encoding='utf-8') as f:
    while True:
        try:
            meals = []
            i = f.readline().strip()
            lines = int(f.readline().strip())
            keys = ['ingredient_name', 'quantity', 'measure']
            values = [f.readline().strip() for _ in range(lines)]
            for value in values:
                meals.append(dict(zip(keys, value.split(' | '))))
            #   meals.append(dict(zip(keys, (re.split(r'(\d+)', value)))))
            #   оставлю для истории, это на случай, если явных разделителей нет
            cook_book[i] = meals
            i = f.readline().strip()
        except:
            break

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    one_ingredient = {}
    keys = ['measure', 'quantity']
    all_ingridients = []
    for i in dishes:
        for ingredient in cook_book[i]:
            a = int(list(ingredient.values())[1])*person_count
            values = [list(ingredient.values())[2], a]
            if list(ingredient.values())[0] not in all_ingridients:
                all_ingridients.append(ingredient['ingredient_name'])
                one_ingredient = dict(zip(keys, values))
                shop_list[list(ingredient.values())[0]] = one_ingredient

            else:
                shop_list[list(ingredient.values())[0]]['quantity'] += a

#(shop_list[list(ingredient.values())[0]]['quantity'] - количество продукта



    pprint.pprint(shop_list)

get_shop_list_by_dishes(['Утка по-пекински', 'Омлет'], 2)

