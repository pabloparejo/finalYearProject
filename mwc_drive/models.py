from django.db import models
from django.contrib.auth.models import User

from oauth2client.django_orm import FlowField
from oauth2client.django_orm import CredentialsField

class DriveAccount(models.Model):
	account_uid = models.CharField(max_length=60)
	display_name = models.CharField(max_length=60)

	def get_path(self, path):
		data = {	'contents': [						
						{	'name': 'file_name',
							'last_modified': 'file_mod',
							'owner': 'file_owner ?',
							'self_link': 'file_link',
							'size': 'file_size',
							'type': 'file/folder'
						}
					],
					'parent': '/path',
					'uid': self.account_uid,
					'username': self.display_name,
					'service_name': 'Google Drive'
				}
		return data

class FlowModel(models.Model):
	id = models.ForeignKey(User, primary_key=True)
	flow = FlowField()

class CredentialsModel(models.Model):
	drive_account = models.ForeignKey(DriveAccount)
	user = models.ForeignKey(User)
	credential = CredentialsField()


	def __unicode__(self):
		return "id: %s /n credential: %s" %(self.id, self.credential)