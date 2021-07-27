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

    def playSong(self, songId, deviceId):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        if deviceId != 'No device':
            print("No device selected")
            # FIXME
            # This won't work because device_id doesn't belong in the json section
            data = {"uris" : [music.PLAYSONG_URI + songId], "device_id" : deviceId}
        else:
            print("Default device")
            data = {"uris" : [music.PLAYSONG_URI + songId]}
        print("Playing: " + songId)
        response = requests.put(music.ENDPOINT_PLAYSONG, headers=header, json=data)
        if (response.ok): 
            song = Song.objects.get(song_id=songId)
            song.has_been_played = True
            song.save()

    def enqueueSong(self, songId, deviceId):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        if deviceId != 'No device':
            print("No device selected")
            data = {"uri" : (music.PLAYSONG_URI + songId), "device_id" : [deviceId]}
        else:
            print("Default device")
            data = {"uri" : (music.PLAYSONG_URI + songId)}
        print(str(data))
        response = requests.post(music.ENDPOINT_ENQUEUE, headers=header, params=data)
        if (response.ok):
            print("Adding song to queue: " + songId)
            song = Song.objects.get(song_id=songId)
            song.has_been_played = True
            song.save()
        else:
            print("failed")
            print(response.text)

    def stopSong(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        print("Stopping")
        response = requests.put(music.ENDPOINT_STOP, headers=header)
        if (response.ok):
            print("Successfully stopped playing music")
        else: 
            print("Failed to stop the music")

    def querySpotifyForSongProgressMS(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(music.ENDPOINT_GET_PLAYBACK_INFO, headers = header)
        jsonResponse = response.json()
        if (response.ok):
            return jsonResponse["progress_ms"]
        else:
            print("status code: " + str(response))
            return  None

    def getPlayStatusInfo(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        response = requests.get(music.ENDPOINT_GET_PLAYBACK_INFO, headers = header)
        jsonResponse = response.json()
        if (response.ok):
            song_id = jsonResponse["item"]["id"]
            song_name = jsonResponse["item"]["name"]
            song_duration = jsonResponse["item"]["duration_ms"]
            song_progress = jsonResponse["progress_ms"]
            ms_remaining = song_duration - song_progress
            song_end_time = timezone.now() + timezone.timedelta(milliseconds=ms_remaining)
            return (song_name, song_end_time)
        else:
            print("status code: " + str(response))
            return  (None, None)


    def getDevices(self):
        self.optionallyRefreshToken()
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
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
        header = {"Authorization": "Bearer " + SpotifyUser.objects.get(pk=1).access_token, "Accept": "application/json", "Content-Type": "application/json"}
        song_count = 0 

        while (song_count == 0) or ((song_count % 100) == 0):
            endpointURL = music.ENDPOINT_GET_PLAYLIST + music.PLAYLIST_ID + "/tracks" \
            + music.GETPLAYLIST_QUERY + music.GETPLAYLIST_LIMIT \
            + music.GETPLAYLIST_INDEX + str(song_count)
            response = requests.get(endpointURL, headers = header)
            jsonResponse = response.json()
            if (response.ok):
                for track in jsonResponse["items"]:
                    print(song_count)
                    print(track)
                    new_song = Song(song_id=track['track']['id'], 
                                    artist_name=track['track']['artists'][0]['name'],
                                    name=track['track']['name'], 
                                    length=track['track']['duration_ms'])
                    new_song.save()
                    song_count += 1
            else:
                song_count = -1
                print("status code: " + str(response.status_code))

    def optionallyRefreshToken(self):
        if SpotifyUser.objects.get(pk=1).expiration_date <= timezone.now():
            print("Auth token expired, refreshing now")
            header = {"Authorization": "Basic " + music.ENCODED_PAIR}
            data = {"grant_type":"refresh_token", "refresh_token": SpotifyUser.objects.get(pk=1).refresh_token}
            response = requests.post(music.ENDPOINT_TOKEN, data = data, headers = header)

            if (response.ok):
                access_token = response.json()["access_token"]
                scope = response.json()["scope"]
                expiration_date = timezone.now() + timezone.timedelta(seconds=int(response.json()["expires_in"]))

                playerAccount = SpotifyUser.objects.get(id=1)
                playerAccount.expiration_date = expiration_date
                playerAccount.access_token=access_token
                playerAccount.scope = scope
                playerAccount.save()
                print("Successful automatic token refresh")
            else:
                print("Unable to refresh token")
                print(response)

    def refreshToken(self):
        header = {"Authorization": "Basic " + music.ENCODED_PAIR}
        data = {"grant_type":"refresh_token", "refresh_token": SpotifyUser.objects.get(pk=1).refresh_token}
        response = requests.post(music.ENDPOINT_TOKEN, data = data, headers = header)

        if (response.ok):
            access_token = response.json()["access_token"]
            scope = response.json()["scope"]
            expiration_date = timezone.now() + timezone.timedelta(seconds=int(response.json()["expires_in"]))

            playerAccount = SpotifyUser.objects.get(id=1)
            playerAccount.expiration_date = expiration_date
            playerAccount.access_token=access_token
            playerAccount.scope = scope
            playerAccount.save()
            print("Successful manual token refresh")
        else:
            print("Unable to manually refresh token")
            print(response)

    def resetAllSongPlayedStatus(self):
        songs = list(Song.objects.all())
        for song in songs:
            song.has_been_played = False
        Song.objects.bulk_update(songs, ['has_been_played'])
        

    def __str__(self):
        return self.access_token[-5:]
