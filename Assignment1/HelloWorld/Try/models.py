from django.db import models


class Album(models.Model):
	title = models.CharField(max_length=100)
	content = models.CharField(max_length=250)


	def __str__(self):
		return self.title + '-'+ self.content
# Create your models here.
class ID(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name