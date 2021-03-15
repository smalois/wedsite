from django.db import models

from guest.models import Guest
from music.models import Song, SpotifyUser
from choicepoll.models import Choice
from django.db.models import Max

import random
import subprocess
import time

import threading

class PlayStatus(models.Model):
    isPlaying = models.BooleanField(default=False)
    #currentSong = models.ForeignKey("music.Song", on_delete=models.CASCADE)

    def refreshChoices(self):
        items = Song.objects.all()
        random_items = random.sample(list(items), 4)
        # MySQL doesn't like 0 index
        for i in range(1,5):
            newChoice = Choice(pk=i, song=random_items[i - 1], choice_text=random_items[i - 1].name)
            newChoice.save()

    def startVoteLoop(self):
        self.refreshChoices()
        Guest.objects.all().update(hasVoted=False)
        while (self.isPlaying):
            highestVoteCount = Choice.objects.aggregate(Max('votes'))
            winningChoice = Choice.objects.filter(votes=highestVoteCount['votes__max'])[0]
            spotifyUser = SpotifyUser.objects.get(pk=1)

            spotifyUser.playSong(winningChoice.song.song_id)
            self.refreshChoices()
            Guest.objects.all().update(hasVoted=False)
            time.sleep(winningChoice.song.length / 1000)

    def startVotingThread(self):
        if (not self.isPlaying):
            votingThread = threading.Thread(target=self.startVoteLoop, daemon=True)
            print("Thread starting")
            votingThread.start()
            self.isPlaying = True
            self.save()

    def stopVotingThread(self):
        if (self.isPlaying):
            print("Thread stopped")
        self.isPlaying = False
        self.save()