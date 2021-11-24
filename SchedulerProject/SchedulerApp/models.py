from django.db import models


class Member(models.Model):
	name = models.CharField(max_length=200,null=True,blank=True)
	resume = models.FileField(upload_to="resume",blank = True)
	email = models.EmailField(max_length=200, null=True)
	def __str__(self):
		return self.name

class Interview(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	members = models.ManyToManyField(Member)
	def __str__(self):
		return str(self.id)
