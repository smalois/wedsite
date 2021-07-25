from django.db import models

from guest.models import Guest
from music.models import Song, SpotifyUser
from choicepoll.models import Choice
from django.db.models import Max
from django.utils import timezone
from music import constants

import random
import time

import threading
import os


class PlayStatus(models.Model):
    isPlaying = models.BooleanField(default=False)
    votingProcess = models.IntegerField(default=-1)
    currentSong = models.CharField(max_length=200, default='No song')
    songEndTime = models.DateTimeField(default=timezone.now, blank=True)
    targetDevice = models.CharField(max_length=64, default='No device')

    def refreshChoices(self):
        items = Song.objects.filter(has_been_played=False)
        if (len(items) <= 4):
            SpotifyUser.resetAllSongPlayedStatus()
            items = Song.objects.filter(has_been_played=False)
        random_items = random.sample(list(items), 4)
        # MySQL doesn't like 0 index
        for i in range(1,5):
            newChoice = Choice(pk=i, song=random_items[i - 1], choice_text=random_items[i - 1].name)
            newChoice.voteEnabled = True
            newChoice.save()

    def startVoteLoop(self):
        pid = os.getpid()
        currentStatus = PlayStatus.objects.get(pk=1)
        spotifyUser = SpotifyUser.objects.get(pk=1)

        currentStatus.votingProcess = pid
        currentStatus.refreshChoices()
        currentStatus.save()

        # Select the song to play
        highestVoteCount = Choice.objects.aggregate(Max('votes'))
        first_song = Song.objects.get(song_id="7p6PJdqPyJLc9NeG5RcDk9")
        winningChoice = Choice(choice_text="First song", song=first_song, votes=1)

        # Play the song
        spotifyUser.playSong(winningChoice.song.song_id, currentStatus.targetDevice)
        currentStatus.refreshChoices()

        # Reset all guest vote status
        Guest.objects.all().update(hasVoted=False)

        while (PlayStatus.objects.get(pk=1).isPlaying):
            print("Starting the thread loop with song: " + winningChoice.song.name)
            currentStatus.currentSong = winningChoice.song.name
            songLength = timezone.timedelta(milliseconds=winningChoice.song.length)
            transition_timedelta = timezone.timedelta(seconds=constants.VOTE_TRANSITION_SECONDS) # TODO This could be 0
            currentStatus.songEndTime = timezone.now() + songLength
            currentStatus.save()

            print("Waiting for voting to end...", end="")
            while (timezone.now() < (PlayStatus.objects.get(pk=1).songEndTime - transition_timedelta) and PlayStatus.objects.get(pk=1).isPlaying):
                print(".", end="", flush=True)
                time.sleep(constants.THREAD_POLL_RATE_SECONDS)

            # Select the song to play
            highestVoteCount = Choice.objects.aggregate(Max('votes'))
            winningChoice = Choice.objects.filter(votes=highestVoteCount['votes__max'])[0]
            spotifyUser.enqueueSong(winningChoice.song.song_id, currentStatus.targetDevice)

            # Stop the voting here
            currentStatus.save()
            Choice.objects.all().update(voteEnabled=False)

            # Synchronize server playtime with Spotify
            print("Song end time: " + str(currentStatus.songEndTime))
            songProgress = spotifyUser.querySpotifyForSongProgressMS()
            if (songProgress):
                songTimeLeft = songLength - timezone.timedelta(milliseconds=int(songProgress))
                currentStatus.songEndTime = timezone.now() + songTimeLeft
                currentStatus.save()
            print("New song end time: " + str(currentStatus.songEndTime))

            print("\nVoting finished, waiting for song to end...", end="")
            while (timezone.now() < PlayStatus.objects.get(pk=1).songEndTime and PlayStatus.objects.get(pk=1).isPlaying):
                print(".", end="")
                time.sleep(constants.THREAD_POLL_RATE_SECONDS)

            currentStatus.refreshChoices()
            Guest.objects.all().update(hasVoted=False)
            # Restart the voting here

        print("Finished with this thread")

    def startVotingThread(self):
        if (not self.isPlaying):
            t = threading.Thread(target=self.startVoteLoop, daemon=True)
            self.isPlaying = True
            self.save()
            t.start()

    def resynchronize(self):
        currentStatus = PlayStatus.objects.get(pk=1)
        spotifyUser = SpotifyUser.objects.get(pk=1)
        name, endtime = spotifyUser.getPlayStatusInfo()
        print("Resynchronizing the following values:")
        if (name):
            print(name)
            currentStatus.currentSong = name
        if (endtime):
            print(endtime)
            currentStatus.songEndTime = endtime
        currentStatus.save()

    def stopVotingThread(self):
        currentStatus = PlayStatus.objects.get(pk=1)
        if (currentStatus.isPlaying):
            currentStatus.isPlaying = False
            currentStatus.votingProcess = -1
            currentStatus.save()