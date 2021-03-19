from django.db import models
from django.utils import timezone

from . import constants as music

import requests

class Song(models.Model):
    song_id = models.CharField(max_length=32, primary_key=True)
    artist_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    length = models.IntegerField()
    has_been_played = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Device(models.Model):
    device_id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name

class SpotifyUser(models.Model):
    access_token = models.TextField(max_length=512)
    refresh_token = models.TextField(max_length=512, default="")
    expiration_date = models.DateTimeField(default=timezone.now)
    scope = models.CharField(max_length=256)

    def playSong(self, songId):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + self.access_token, "Accept": "application/json", "Content-Type": "application/json"}
        data = { "uris" : [music.PLAYSONG_URI + songId]}
        print("Playing: " + songId)
        response = requests.put(music.ENDPOINT_PLAYSONG, headers=header, json=data)

    # UNTESTED
    def enqueueSong(self, songId):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + self.access_token, "Accept": "application/json", "Content-Type": "application/json"}
        data = {"uri" : [music.PLAYSONG_URI + songId]}
        response = requests.post(music.ENDPOINT_ENQUEUE, headers=header, params=data)
        if (response.ok):
            print("Adding song to queue: " + songId)
        else:
            print("failed")
            print(response.text)

    def stopSong(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + self.access_token, "Accept": "application/json", "Content-Type": "application/json"}
        print("Stopping")
        response = requests.put(music.ENDPOINT_STOP, headers=header)
        if (response.ok):
            print("Successfully stopped playing music")
        else: 
            print("Failed to stop the music")

    def getDevices(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + self.access_token, "Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(music.ENDPOINT_GET_DEVICES, headers = header)
        jsonResponse = response.json()
        if (response.ok):
            Device.objects.all().delete()
            for device in jsonResponse["devices"]:
                deviceId = device["id"]
                name = device["name"]
                newDevice = Device(device_id=deviceId, name=name)
                newDevice.save()
        else:
            print("status code: " + str(response.status_code))

    def updatePlaylist(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + self.access_token, "Accept": "application/json", "Content-Type": "application/json"}
        endpointURL = music.ENDPOINT_GET_PLAYLIST + music.PLAYLIST_ID + music.GETPLAYLIST_QUERY
        print(endpointURL)
        response = requests.get(endpointURL, headers = header)
        jsonResponse = response.json()
        if (response.ok):
            for track in jsonResponse["tracks"]["items"]:
                new_song = Song(song_id=track['track']['id'], 
                                name=track['track']['name'], 
                                length=track['track']['duration_ms'])
                new_song.save()
        else:
            print("status code: " + str(response.status_code))

    def optionallyRefreshToken(self):
        if self.expiration_date <= timezone.now():
            header = {"Authorization": "Basic " + music.ENCODED_PAIR}
            data = {"grant_type":"refresh_token", "refresh_token": self.refresh_token}
            response = requests.post(music.ENDPOINT_TOKEN, data = data, headers = header)

            if (response.ok):
                access_token = response.json()["access_token"]
                scope = response.json()["scope"]
                expiration_date = timezone.now() + timezone.timedelta(seconds=int(response.json()["expires_in"]))

                playerAccount = SpotifyUser(id=1, access_token=access_token, refresh_token=self.refresh_token, scope=scope)
                playerAccount.save()


    def __str__(self):
        return self.access_token[-5:]
