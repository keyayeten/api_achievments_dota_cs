from django.db import models


class User(models.Model):
    """
    tasks structure
    tasks = {
        task_id: {
            current_progress: integer value,
            target_progress: integer value,
        },
        '''
    }
    """
    steam_id = models.CharField(max_length=100, blank=True, null=True)
    dota_id = models.CharField(max_length=100, blank=True, null=True)
    winline_id = models.CharField(max_length=100)
    twitch_id = models.JSONField(default=dict, blank=True, null=True)
    tasks = models.JSONField(default=dict, blank=True, null=True)
    current_task = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.steam_id
