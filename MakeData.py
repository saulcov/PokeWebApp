## Preprocessing: Scraping data from PokeAPI and storing in an object-database
from math import ceil
import requests
import pickle
import json

def fetch(url):
    response = requests.get(url)
    return None if response.status_code != 200 else response.json()

class Pokemon(object):

    def __init__(self, url):
        data = fetch(url)
        self.name = self.get_name(data)
        self.idx = self.get_idx(data)
        self.genus = self.get_genus(data)
        self.descriptions = self.get_descriptions(data)
        self.color = self.get_color(data)
        self.steps = self.get_steps(data)
        self.catch_rate = self.get_catch_rate(data)
        self.egg_groups = self.get_egg_groups(data)
        self.genders = self.get_genders(data)
        data = fetch(data['varieties'][0]['pokemon']['url'])
        self.types = self.get_types(data)
        self.stats = self.get_stats(data)
        self.sprites = self.get_sprites(data)
        self.height = self.get_height(data)
        self.weight = self.get_weight(data)
        self.abilities = self.get_abilities(data)

    def get_name(self, data):
        return data['name'].capitalize()

    def get_idx(self, data):
        return data['id']

    def get_genus(self, data):
        for entry in data['genera']:
            if entry['language']['name'] == 'en':
                return entry['genus']

    def get_descriptions(self, data):
        Docs = []
        toReplace = {self.name.upper():self.name.capitalize(),'POKéMON':'pokémon','Pokémon':'pokémon','—':'', '-':' ','\xad':''}
        for entry in data['flavor_text_entries']:
            if entry['language']['name'] == 'en':
                for a, b in toReplace.items():
                    entry['flavor_text'] = entry['flavor_text'].replace(a, b)
                clean = ' '.join(entry['flavor_text'].split())
                if clean not in Docs:
                    Docs.append(clean)
        return Docs

    def get_color(self, data):
        return data['color']['name']

    def get_steps(self, data):
        return 255*(data['hatch_counter'] + 1) # counter -> steps

    def get_catch_rate(self, data):
        return ceil(1000*(data['capture_rate']/255))/10

    def get_egg_groups(self, data):
        return [entry['name'].capitalize() for entry in data['egg_groups']]

    def get_genders(self, data):
        rate = data['gender_rate']
        if rate != -1:
            return {'female':100*rate/8, 'male':100*(8 - rate)/8}
        else:
            return {'genderless':100}
        
    def get_types(self, data):
        return [ entry['type']['name'] for entry in data['types']]

    def get_stats(self, data):
        return { entry['stat']['name']:entry['base_stat'] for entry in data['stats'] }

    def get_sprites(self, data):
        return data['sprites']['front_default']

    def get_height(self, data):
        return data['height']/10 # decimetres -> meters

    def get_weight(self, data):
        return data['weight']/10 # hectograms -> kilograms

    def get_abilities(self, data):
        return [ entry['ability']['name'].capitalize() for entry in data['abilities'] ]

    def title(self):
        return [self.name, str(self.idx), self.genus] + self.egg_groups + self.types + self.abilities

    def document(self):
        return ' '.join(self.descriptions)

## example: 
#pk = Pokemon('https://pokeapi.co/api/v2/pokemon-species/1/')
#print(f'{list(pk.__dict__.keys())}\n\n{pk.__dict__}')

class Pokedex(dict):

    def __init__(self, url):
        data = fetch(url)
        for entry in data['pokemon_entries']:
            pokemon = Pokemon(entry['pokemon_species']['url'])
            self[pokemon.idx] = pokemon
            print(f'Scanning ID = {pokemon.idx:4} | pokemon: {pokemon.name:16}')

    def close(self, filename):
        with open(filename, 'wb') as pickle_out:
            pickle.dump(self, pickle_out)

if __name__ == "__main__":
    pk = Pokedex('https://pokeapi.co/api/v2/pokedex/1')
    pk.close('data/pokedex_national.pickle')
