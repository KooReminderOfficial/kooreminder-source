from django.db import models

# Create your models here.
class Alarm(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=64)
    repeat = models.CharField(max_length=8)
    sound = models.CharField(max_length=255)

    def __str__(self):
        return 'Alarm:\ttime: {}\n     \ttitle: {}\n      \trepeat: {}\n      \tsound: {}'.format(self.time, self.title, self.repeat, self.sound)
    
    def to_json(self):
        return f'{{\n\t"time": "{self.time}",\n\t"title": "{self.title}",\n\t"repeat": "{self.repeat}",\n\t"sound": "{self.sound}"\n}}'


class Settings(models.Model):
    setting_id = models.CharField(max_length=16)
    value = models.BooleanField()

    def __str__(self):
        return f'{self.setting_id} : {self.value}'