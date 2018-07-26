from django.db import models

class Bucket(models.Model):
    """This class represents the bucketlist model."""
    id=models.CharField(max_length=255,unique=True,primary_key=True)
    name = models.CharField(max_length=255, blank=False, unique=True)


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)