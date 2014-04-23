from django.db import models

# Create your models here.
class DropboxAccount(models.Model):

    account_uid = models.CharField(max_length=60)
    email = models.EmailField()
    token = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    
    def __unicode__(self):
        return "Service: %s | User: %s" %(self.service, self.service_email,)