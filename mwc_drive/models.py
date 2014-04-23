from django.db import models

# Create your models here.

class DriveAccount(models.Model):
    account_uid = models.CharField(max_length=60)
    display_name = models.CharField(max_length=60)


class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()

class CredentialsModel(models.Model):
    drive_account = models.ForeignKey(DriveAccount)
    user = models.ForeignKey(User)
    credential = CredentialsField()


    def __unicode__(self):
        return "id: %s /n credential: %s" %(self.id, self.credential)