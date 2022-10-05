from urllib import request
import requests
from secrets import USER_ID, ACCESS_TOKEN, DISCOVER_WEEKLY_PLAYLIST_ID
from datetime import date
from twilio.rest import Client



class SaveSongs:

    def __init__(self):
        self.user_id = USER_ID
        self.access_token = ACCESS_TOKEN
        self.playlist_id = DISCOVER_WEEKLY_PLAYLIST_ID
        self.tracks = ""
        self.in_weekly = {}
        self.date_today = date.today().strftime("%b %d")



    def find_songs(self):
        dicovered_uris = []
        SPOTIFY_URL = f'https://api.spotify.com/v1/playlists/{DISCOVER_WEEKLY_PLAYLIST_ID}/tracks?' 

        # get items of discover weekly playlist
        response = requests.get(
            SPOTIFY_URL+'fields=items(track(id%2Curi%2Cartist%2Cname))',
            headers={
            "Accept": "application/json",
             "Content-Type": "application/json",
             "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        )
        discovered = response.json()

        # songs in your discover weekly
        self.in_weekly = discovered

       
        
             # save the spotify uris to a array
             # for item in discovered['items']:
             # dicovered_uris.append(item["track"]["uri"])

        # create comma seperated list 
        for item in discovered['items']:
            self.tracks += (item["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]

        self.add_songs()

        


    def create_playlist(self):
        query = f'https://api.spotify.com/v1/users/{USER_ID}/playlists'

        response_playlist = requests.post(
            query,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            json={
              "name":  "Discover Weekly Playlist - " + self.date_today,
              "description": "Your Discover Weekly Playlist before it's gone forever and ever",
              "public": False
            } 
        )

        response_playlist = response_playlist.json()
        
    
        return response_playlist['id']

    
    def  find_top_track(self):
        discover_ids = ""

        # get ids of all tracks
        for item in self.in_weekly['items']:
            discover_ids += (item["track"]["id"] + ",")
        discover_ids = discover_ids[:-1]
    
        # get several tracks 
        query = "https://api.spotify.com/v1/tracks?"
        response = requests.get(
            query + "market=US&" + "ids=" + discover_ids,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        )
        responses = response.json()

        # responses = responses['tracks']['popularity']
        responses = responses['tracks']

        popularity = []
       # compare popularity values
        for it in responses:
            popularity.append(it['popularity'])
        max_pop_val = max(popularity)

        # index of most popular song
        max_index = popularity.index(max_pop_val)

        popular_song_name = responses[max_index]["name"]
        return popular_song_name


    def send_message(self):


        most_pop_track = self.find_top_track()
    
        client = Client("AC7fab959d573161273f3cd2a4db93ce01","f62f53eb09f8d6623b560de23c1853eb")
        my_msg = client.messages.create(
            to="+17789037209",
            from_="+17432008422",
            body= "Your " + self.date_today + " Discover Weekly Playlist has been saved! This weeks most popular track is: \n\n"+ most_pop_track 
            + ".\n\nHappy listening :)",
            )
        print(my_msg.body) 






    #      add songs to a created playlist, you have access to the tracks you need to add
    #      you can call other function to get the playlist id for witch you want to add songs too
    def add_songs(self):

        # get the id of the playlist you want to add too 
        playlist_id = self.create_playlist()
        query = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?'

        # make a request to the api
        response = requests.post(
            query + 'uris=' + self.tracks,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        )
        self.send_message()
    



CreateYourWeekly = SaveSongs()
CreateYourWeekly.find_songs()
