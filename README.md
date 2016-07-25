# PokemonGo Facebook Bot ![Python 2.7](https://img.shields.io/badge/python-2.7-blue.svg)


This bot builds on top of [PokemonGo Map](https://jz6.github.io/PoGoMap/) to provide mobile or desktop users an easy way to get a list of nearby pokemon (at a fixed location defined by the PokemonGo Map) by simply messaging the Facebook bot.

## Disclaimers
PLEASE DO NOTE THAT THIS BOT WAS MADE FOR FUN AND IS NOT MEANT TO BE SERIOUS, DO EXPECT SOME BUG AS IT WAS BUILT IN A COUPLE OF HOURS, AND PLEASE REPORT ANY BUGS YOU FIND!

## How to setup

Follow [PokemonGo Wiki](https://github.com/AHAAAAAAA/PokemonGo-Map/wiki) to setup the initial map. 

Simply create a new [facebook page](https://www.facebook.com/pages/create/?ref_type=bookmark), then add a new app in [Facebook Dev](https://developers.facebook.com/apps/).

Generate a new token in ![map](http://puu.sh/qejVW/230c0f46b5.png) 
And paste the token in bot.py as 'PAGE_ACCESS_TOKEN'

Set API_ URL in bot.py as the address to the PokemonGo Map /raw_data, e.g. if the url to the pokemongo map is abcdefg.ngrok.io, the API_ URL should be 'http://abcdefg.ngrok.io/raw_data'

Then simply run bot.py.

Tunnel port 80 using ngrok or equivalent tools, if port 80 has been used please modify 'port=80' in the bottom of the code into some other values.

Paste the tunneled url to ![map](http://puu.sh/qekAs/cb33647e8e.png), and add 'webhook' to the end. e.g. if the url of the tunnel is xxxx.ngrok.io, you should type in https://xxxx.ngrok.io/webhook

You should be good to go!

You will need to add people as 'testers' in the developer page under roles in order to use the bot. 

To generate a set of lat-lng to address mapping, uw_ locations.json needs to be edited, we got ours from our school's API. Geolocator code is included you just need to comment and uncomment the location_pokemon with the one you would like to use. We find Geolocator to be a little inaccurate and we sometimes run into request quota limit issues.

## Warnings

Using this software is against the ToS of the game. You can get banned, use this tool at your own risk.


## Contributions

This bot is entirely based on [PokemonGo Map](https://github.com/AHAAAAAAA/PokemonGo-Map/)


[Try the bot](https://www.facebook.com/wherethefckismypokemon/) -> I would still need to add you to the tester list, but just shoot the bot a message and I'll be notified.

[Youtube demo](https://www.youtube.com/watch?v=bMy2DJwmldA)

