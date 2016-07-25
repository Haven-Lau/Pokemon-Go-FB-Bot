#!/usr/bin/python
# -*- coding: utf-8 -*-

import flask
from flask import Flask, render_template, request
import requests
import json
import math
import time
from datetime import datetime

app = Flask(__name__)

API_URL = 'http://<POKEMONGO MAP ADDRESS GOES HERE>/raw_data' # PokemonGo Map from AHAAAAAAA
PAGE_ACCESS_TOKEN = '' # Facebook page api token
post_message_url = 'https://graph.facebook.com/v2.7/me/messages?access_token=' + PAGE_ACCESS_TOKEN

vegan_mode = {}
last_called = {}
shit_list = set(['Pidgey', 'Rattata', 'Zubat', 'Raticate', 'Pidgeotto', 'Drowzee','Raticate','Spearow'])

rarity_list = [set(['Caterpie','Weedle','Ekans','Sandshrew','Nidoran','Geodude','Poliwag','Mankey','Venomoth','Paras','Gastly','Krabby','Voltorb','Goldeen','Magikarp']),
               set(['Bulbasaur','Slowpoke','Bellsprout','Horsea','Charmander','Metapod','Kakuna','Oddish','Arbok','Psyduck','Persian','Diglet','Golbat','Meowth','Jigglypuff','Vulpix','Magnemite','Clefairy','Sandslash','Pikachu','Growlith','Machoke','Tentacool','Graveler','Ponyta','Magneton','Doduo','Koffing','Hitmonlee','Cubone','Exeggcute','Electrode','Drowzee','Haunter','Shellder','Grimer','Rhyhorn','Staryu','Jynx']),
               set(['Butterfree','Pidgeot','Abra','Machop','Fearow','Nidorina','Nidorino','Wigglytuff','Gloom','Parasect','Dugtrio','Kabuto','Golem','Tentacruel','Machamp','Kadabra','Poliwhirl','Chansey','Primeape','Squirtle','Golduck','Dratini','Seel','Dodrio','Cloyster','Scyther','Hypno','Seadra','Seaking','Starmie','Eevee']),
               set(['Beedrill','Weepinbell','Pinsir','Snorlax','Mr. Mime','Farfetch\'d','Onix','Exeggutor','Muk','Arcanine','Rapidash','Rhydon','Kingler','Magmar','Flareon','Jolteon','Tangela','Gyarados','Lapras','Vaporeon','Kabutops','Ivysaur','Charmeleon','Wartortle','Porygon','Omanyte','Dragonair','Raichu','Nidoqueen','Nidoking','Vileplume','Gengar','Marowak','Dewgong','Kangaskhan','Victreebel','Electrabuzz','Alakazam','Poliwrath','Venomoth','Aerodactyl','Venusaur','Charizard','Clefable','Tauros','Omastar','Dragonite','Ditto','Articuno','Zapdos','Moltres','Mewtwo','Mew'])]

rarity_names = ['Very common', 'Common', 'Uncommon', 'Rare']
'''
The core of the bot
'''
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':

        # Messages from user
        data = json.loads(request.data)
        if data is None:
            payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Map server seems to be down.. Informing haven'}})
            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
            return 'WTF'
        for entry in data['entry']:
            for message_entry in entry['messaging']:

                if 'message' in message_entry and 'text' in message_entry['message']:
                    text = message_entry['message']['text'] # Incoming Message Text
                    sender = message_entry['sender']['id'] # Sender ID
                    #######IRONIC MEMES##########
                    if abs(message_entry['timestamp']/1000 - time.time() ) > 15 : # 15 seconds timeout from facebook
                        continue

                    if 'fuck' in text.lower() or 'shit' in text.lower() or 'cunt' in text.lower():
                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Fuck you stop swearing you cunt'}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                    elif 'help' in text.lower():
                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Available commands: \nList - Display nearby pokemon \nVegan - Vegan mode \nBTW DON\'T SWEAR AT ME'}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)    
                    elif 'vegan' in text.lower():
                        if sender not in vegan_mode:
                            vegan_mode[sender] = True
                            payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Vegan mode activated'}})
                            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                            continue

                        if not vegan_mode[sender]:
                            vegan_mode[sender] = True
                            payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Vegan mode activated'}})
                            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                        else:
                            vegan_mode[sender] = False
                            payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Vegan mode de-activated'}})
                            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)

                    elif 'list' in text.lower():
                        if (sender in last_called and (message_entry['timestamp'] - last_called[sender] ) < 30000): # 30 seconds cooldown
                            cool_down = 30-(message_entry['timestamp'] - last_called[sender])/1000
                            payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Sorry, you are on a %s seconds cooldown' % str(cool_down)}})
                            status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                            continue
                        
                        last_called[sender] = message_entry['timestamp']
                        # Get raw data from pokemon map
                        r = requests.get(API_URL)
                        pokemons = json.loads(r.content)
                        pokemon_count = [0,0,0,0]
                        page_count = [0,0,0,0]
                        abs_page_count = [0,0,0,0]
                        list_of_element_list = [[[]],[[]],[[]],[[]]]

                        for pokemon in pokemons['pokemons']:
                            if pokemon['pokemon_name'] not in shit_list:
    
                                # Get time delta string and coordinates
                                time_delta_str = get_expire_time(pokemon['disappear_time'])
                                coordinate = str(pokemon['latitude']) +', '+ str(pokemon['longitude'])
    
                                # Approximate location name
                                location_pokemon = get_location(float(pokemon['latitude']), float(pokemon['longitude']))
                                
                                for index in range(0,4):
                                    # Append pokemon to element lists
                                    if pokemon['pokemon_name'] in rarity_list[index]:
                                        list_of_element_list[index][page_count[index]] = append_pokemon(sender, pokemon['pokemon_name'], pokemon['pokemon_id'], location_pokemon, coordinate, time_delta_str, list_of_element_list[index][page_count[index]])
                                        pokemon_count[index] += 1
                                        abs_page_count[index] += 1
                                    #  According to facebook documentation max elements in a payload is 10
                                    if pokemon_count[index] == 10:
                                        temp = []
                                        list_of_element_list[index].append(temp)
                                        page_count[index] += 1
                                        pokemon_count[index] = 0

                        for index in range(0,4):
                            # Fix case when number of items == 10
                            if (abs_page_count[index] % 10) == 0:
                                list_of_element_list[index].pop()
                                page_count[index] -= 1
                            print '%s page_count: %i' % (rarity_names[index], abs_page_count[index])
                            for pages in range(0,page_count[index]+1):
                                if list_of_element_list[index][page_count[index]]:
                                    if pages == 0:
                                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text':rarity_names[index]+' pokemon:'}})
                                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                                    else:
                                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text':'More ' +rarity_names[index]+ '...'}})
                                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                                    payload = json.dumps(get_payload(sender,list_of_element_list[index][pages])) 
                                    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)

                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text':'GOTTA CATCHEM ALL'}})
                        #payload = json.dumps({'recipient': {'id': sender}, 'message': {'text':str(pokemon_count)}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
                        
                    else:
                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': text}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)

                    if sender in vegan_mode and vegan_mode[sender]:
                        payload = json.dumps({'recipient': {'id': sender}, 'message': {'text': 'Haha anyways I\'m vegan'}})
                        status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=payload)
    elif request.method == 'GET': # For the initial verification
        return request.args.get('hub.challenge')
    return 'HI'


'''
Append pokemon as another element in the element list
'''
def append_pokemon(sender, pokemon_name, pokemon_id, location, coordinate, time_delta_str,element_list):
    message, subtitle = get_format_string(pokemon_name, location, time_delta_str).split(' - ')
    location = location.replace(' ', '+')
    direction_url = 'https://www.google.com/maps/dir/Current+Location/' + coordinate
    image_url = 'http://assets.pokemon.com/assets/cms2/img/pokedex/full/%03d.png' % pokemon_id
    wiki_url = 'http://www.pokemon.com/us/pokedex/%s' % pokemon_name
    element = {
                "title":message,
                "subtitle":subtitle,
                "image_url":image_url,
                "buttons":[
                  {
                    "type":"web_url",
                    "url":direction_url,
                    "title":"Get Direction"
                  },
                  {
                    "type":"web_url",
                    "url":wiki_url,
                    "title":"Pokemon Wiki"
                  }
                ]
              }
    element_list.append(element)
    return element_list

'''
Get time difference between current time and given time
return a formatted string
'''
def get_expire_time(expire_time):
    expire_time /= 1000
    time_delta = expire_time - time.time()
    str_time = datetime.fromtimestamp(expire_time).strftime('%I:%M:%S%p')
    m, s = divmod(time_delta, 60)
    return '%s (%dm%ds)' % (str_time, m, s)

'''
Return a well-formatted string that will be sent to user
'''
def get_format_string(pokemon_name, location, time_delta_str):
    return '%s near %s - Despawning at %s' % (pokemon_name, location, time_delta_str)

'''
Return the payload in json format
'''
def get_payload(sender, element_list):

    return {
      "recipient":{
        "id":sender
      },
      "message":{
        "attachment":{
          "type":"template",
          "payload":{
            "template_type":"generic",
            "elements":element_list
          }
        }
      }
    }

'''
Approximate the location by using pythagorean theorem
'''
def get_location(lat, log):
    with open('uw_locations.json') as locations:
        data = json.loads(locations.read())
        min_distance = 0.0
        min_location = ''
        for location in data:
            location_lat, location_log = data[location].split(',')
            location_lat, location_log = float(location_lat), float(location_log)
            if min_distance == 0.0 or math.sqrt((location_lat - lat) ** 2 + (location_log - log) ** 2) < min_distance:
                min_distance = math.sqrt((location_lat - lat) ** 2 + (location_log - log) ** 2)
                min_location = location
    return min_location

if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=80)
