import requests

url = "https://superheroapi.com/api/2619421814940190/search/"

heroes = {}

def get_intelligence(names):
    for name in names:
        name_url = url+name
        resp = requests.get(name_url).json()
        heroes[resp['results'][0]['name']] = resp['results'][0]['powerstats']['intelligence']
    sorted_heroes = sorted(heroes.items(), key=lambda x: x[1])
    return(sorted_heroes)

def smartest_hero(names):
    sorted_heroes = get_intelligence(names)
    print(f'Самый умный герой - {sorted_heroes[0][0]}')


if __name__ == '__main__':
    smartest_hero(['Hulk', 'Captain_America', 'Thanos'])
