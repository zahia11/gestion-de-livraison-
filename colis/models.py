from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=8, blank=False, null=False)

    def __str__(self):
        return self.user.username
    
class Colis(models.Model):
    STATUS_CHOICES = (
        ('en cours', 'Pending'),
        ('livré', 'Accpted'),
        ('annulé', 'Refused'), )
    default_user = User.objects.get(pk=1)
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, blank=True , default=default_user.id)
    code = models.BigAutoField(primary_key=True)  
    nom_produits = models.CharField(max_length=100)
    nom_destinataire = models.CharField(max_length=100)
    adr_destinataire = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    num_destinataire = models.CharField(max_length=100)
    prix = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en cours')  
    date_distribution = models.DateTimeField(null=True, blank=True) 
    date_envoi = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nom_produits} - {self.nom_destinataire}"


