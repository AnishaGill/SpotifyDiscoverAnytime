import requests
from secrets import ACCESS_TOKEN, USER_ID, DISCOVER_WEEKLY_PLAYLIST_ID
from datetime import date

class SaveSongs:

    def __init__(self):
        self.user_id = USER_ID
        self.access_token = ACCESS_TOKEN
        self.playlist_id = DISCOVER_WEEKLY_PLAYLIST_ID
        self.tracks = ""



    def find_songs(self):
        dicovered_uris = []
        SPOTIFY_URL = f'https://api.spotify.com/v1/playlists/{DISCOVER_WEEKLY_PLAYLIST_ID}/tracks?' 

        # get items of discover weekly playlist
        response = requests.get(
            SPOTIFY_URL+'fields=items(track(uri%2Cartist%2Cname))',
            headers={
            "Accept": "application/json",
             "Content-Type": "application/json",
             "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        )
        discovered = response.json()
        
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
        date_today = date.today().strftime("%b %d")

        response_playlist = requests.post(
            query,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {ACCESS_TOKEN}"
            },
            json={
              "name":  "Discover Weekly Playlist " + date_today,
              "description": "Your Discover Weekly Playlist before it's gone forever and ever",
              "public": False
            } 
        )

        response_playlist = response_playlist.json()
        
    
        return response_playlist['id']




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
 

CreateYourWeekly = SaveSongs()
CreateYourWeekly.find_songs()












