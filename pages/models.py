from django.db import models



class Contact(models.Model):
    
    name = models.CharField(max_length=300, null=True, blank=True, editable = False)
    message = models.TextField(null=True, blank=True, editable = False)
    email = models.CharField(max_length=300, null=True, blank=True, editable = False)
    

    class Meta:
        verbose_name_plural = "Contact messages"

    def __str__(self):
        return self.name



class Subscribers(models.Model):
    
    email = models.CharField(max_length=300, null=True, blank=True, editable = False)
    

    class Meta:
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email

