from django.db import models

class Blog(models.Model):
	title = models.CharField(max_length=32)
	date = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
#	calories = models.DecimalField(max_digits=6, decimal_places=2) 