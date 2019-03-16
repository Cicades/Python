from django.db import models

# Create your models here.

class RegionInfo(models.Model):
	name = models.CharField(max_length=50)
	parent = models.ForeignKey('self')
	def __str__(self):
		return self.name
		
	class Meta:
		db_table = 'region'