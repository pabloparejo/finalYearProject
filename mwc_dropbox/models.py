from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DropboxAccount(models.Model):

	account_uid = models.CharField(max_length=60)
	email = models.EmailField()
	token = models.CharField(max_length=100)
	user = models.ForeignKey(User)

	
	def __unicode__(self):
		return "Service: Dropbox | User: %s" %(self.service_email)

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
					'parent': ['/path'],
					'uid': self.account_uid,
					'username': self.email, #Cambiar por nombre de usuario real
					'service_name': 'Dropbox'
				}
		return data