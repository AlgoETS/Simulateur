from django.db import models

class News(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    published_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Market News"
