from django.db import models
from main.models import General
from django.contrib.auth import get_user_model

User = get_user_model()


class Scores(General):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_scores', verbose_name='کاربر مربوطه')
    score = models.IntegerField(default=1, verbose_name='مقدار امتیاز')
    description = models.TextField(verbose_name='توضیحات امتیاز')

    def __str__(self):
        return f'{self.user} - {self.score} '
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازات'
