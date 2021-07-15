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
            Song.resetPlayedStatus()
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
        winningChoice = Choice.objects.filter(votes=highestVoteCount['votes__max'])[0]

        # Play the song
        spotifyUser.playSong(winningChoice.song.song_id, currentStatus.targetDevice)
        currentStatus.refreshChoices()

        # Reset all guest vote status
        Guest.objects.all().update(hasVoted=False)

        while (PlayStatus.objects.get(pk=1).isPlaying):
            currentStatus.currentSong = winningChoice.song.name
            currentStatus.save()
            songLength = timezone.timedelta(milliseconds=winningChoice.song.length)
            songEndTime = timezone.now() + songLength
            voteEndTime = songEndTime - timezone.timedelta(seconds=constants.VOTE_TRANSITION_SECONDS) # TODO This could be 0
            currentStatus.songEndTime = songEndTime
            currentStatus.save()

            # print("Waiting for voting to end...", end="")
            while (timezone.now() < voteEndTime and PlayStatus.objects.get(pk=1).isPlaying):
                # print(".", end="", flush=True)
                time.sleep(constants.THREAD_POLL_RATE_SECONDS)

            # Select the song to play
            highestVoteCount = Choice.objects.aggregate(Max('votes'))
            winningChoice = Choice.objects.filter(votes=highestVoteCount['votes__max'])[0]
            spotifyUser.enqueueSong(winningChoice.song.song_id, currentStatus.targetDevice)

            # Stop the voting here
            Choice.objects.all().update(voteEnabled=False)

            # Synchronize server playtime with Spotify
            print("Song end time: " + str(songEndTime))
            songProgress = spotifyUser.querySpotifyForSongProgressMS()
            if (songProgress):
                songTimeLeft = songLength - timezone.timedelta(milliseconds=int(songProgress))
                songEndTime = timezone.now() + songTimeLeft
                currentStatus.songEndTime = songEndTime
                currentStatus.save()
            print("New song end time: " + str(songEndTime))

            # print("\nVoting finished, waiting for song to end...", end="")
            while (timezone.now() < songEndTime and PlayStatus.objects.get(pk=1).isPlaying):
                # print(".", end="")
                time.sleep(constants.THREAD_POLL_RATE_SECONDS)

            currentStatus.refreshChoices()
            Guest.objects.all().update(hasVoted=False)
            # Restart the voting here

    def startVotingThread(self):
        if (not self.isPlaying):
            t = threading.Thread(target=self.startVoteLoop, daemon=True)
            self.isPlaying = True
            self.save()
            t.start()

    def stopVotingThread(self):
        currentStatus = PlayStatus.objects.get(pk=1)
        if (currentStatus.isPlaying):
            currentStatus.isPlaying = False
            currentStatus.votingProcess = -1
            currentStatus.save()