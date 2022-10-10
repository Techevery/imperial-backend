from django.db import models

# Create your models here.



class Flat(models.Model):
    name = models.CharField(max_length=100)
    number_of_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_living_rooms = models.PositiveIntegerField(null=True, blank=True)
    number_of_kitchens = models.PositiveIntegerField(null=True, blank=True)
    number_of_toilets = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    test_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Property(models.Model):
    property_image = models.ImageField(blank=True, null=True, upload_to='uploads/properties')
    property_name = models.CharField(max_length=100)
    address = models.TextField()
    flats = models.ManyToManyField(Flat,blank=True)


    def __str__(self):
        return str(self.property_name)


