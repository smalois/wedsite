from django.db import models

from guest.models import Guest
from music.models import Song, SpotifyUser
from choicepoll.models import Choice
from django.db.models import Max
from django.utils import timezone

import random
import subprocess
import time

import multiprocessing
import os
import signal

VOTE_TRANSITION_SECONDS = 30
CROSSFADE_LENGTH_SECONDS = 5
THREAD_POLL_RATE_SECONDS = .5

class PlayStatus(models.Model):
    isPlaying = models.BooleanField(default=False)
    votingProcess = models.IntegerField(default=-1)
    #currentSong = models.ForeignKey("music.Song", on_delete=models.CASCADE)

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
        spotifyUser.playSong(winningChoice.song.song_id)
        currentStatus.refreshChoices()

        # Reset all guest vote status
        Guest.objects.all().update(hasVoted=False)

        while (True):
            songLength = timezone.timedelta(milliseconds=winningChoice.song.length)
            songEndTime = timezone.now() + songLength
            voteEndTime = songEndTime - timezone.timedelta(seconds=VOTE_TRANSITION_SECONDS) # TODO This could be 0

            # print("Waiting for voting to end...", end="")
            while (timezone.now() < voteEndTime):
                # print(".", end="", flush=True)
                time.sleep(THREAD_POLL_RATE_SECONDS)

            # Select the song to play
            highestVoteCount = Choice.objects.aggregate(Max('votes'))
            winningChoice = Choice.objects.filter(votes=highestVoteCount['votes__max'])[0]
            spotifyUser.enqueueSong(winningChoice.song.song_id)

            # Stop the voting here
            Choice.objects.all().update(voteEnabled=False)

            # Synchronize server playtime with Spotify
            print("Song end time: " + str(songEndTime))
            songTimeLeft = songLength - timezone.timedelta(milliseconds=int(spotifyUser.querySpotifyForSongProgressMS()))
            songEndTime = timezone.now() + songTimeLeft
            print("New song end time: " + str(songEndTime))

            # print("\nVoting finished, waiting for song to end...", end="")
            while (timezone.now() < songEndTime):
                # print(".", end="")
                time.sleep(THREAD_POLL_RATE_SECONDS)

            currentStatus.refreshChoices()
            Guest.objects.all().update(hasVoted=False)
            # Restart the voting here

    def startVotingThread(self):
        p = multiprocessing.Process(target=self.startVoteLoop)
        self.isPlaying = True
        p.start()
        self.save()

    def stopVotingThread(self):
        currentStatus = PlayStatus.objects.get(pk=1)
        try:
            if (currentStatus.votingProcess != -1):
                spotifyUser = SpotifyUser.objects.get(pk=1)
                spotifyUser.stopSong()
                os.kill(currentStatus.votingProcess, signal.SIGTERM)
            currentStatus.isPlaying = False
            currentStatus.votingProcess = -1
            currentStatus.save()
        except ProcessLookupError:
            currentStatus.isPlaying = False
            currentStatus.votingProcess = -1
            currentStatus.save()

        

