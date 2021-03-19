from django.db import models

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    song = models.ForeignKey("music.Song", on_delete=models.CASCADE, default=0)
    votes = models.IntegerField(default=0)
    voteEnabled = models.BooleanField(default=True)