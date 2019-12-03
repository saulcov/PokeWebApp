# PokeWebApp
## About
This is a web application that was created in response to a data mining course project, in which we are suppose to showcase three fundamental components to data mining: textual search, classification, and image captioning. For my choice of a data, I chose to use the PokeAPI containing highly detailed data related to the Pokémon franchise, a franchise that  I grew up with. This project consists of three phases:

Phase I : To develop search feature based on a textual component in the data.

Phase II  : To develop a classifier feature based on multiple numerical attributes in the data.

Phase III : To develop an image recognition system feature based on an image component in the data.

In order to begin the development of the application, I began by exploring the PokeAPI and planning different ways in which I could extract the relevant data that I would be using. 

## Phase I
In order to implement phase I, I needed to create a file MakeData.py that would scrape data from the PokeAPI and store it in an object-database. Upon running this file a pokedex class object containing all the retrived data from the API, is stored as a pickle as data/pokedex_national.pickle. 
