from django.db import models
from django.contrib.auth.models import User

from dropbox.client import DropboxClient

# Create your models here.
class DropboxAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()
	token = models.CharField(max_length=100)

	user = models.ForeignKey(User)

	
	def __unicode__(self):
		return self.email

	def get_path(self, path):
		client = DropboxClient(self.token)
		metadata_list = client.metadata(path)['contents']

		for data in metadata_list:
			data['name'] = data['path'][1:] 
		data = {	'contents': metadata_list,
					'display_name': self.display_name,
					'parent': path,
					'service_class': 'dropbox',
					'service_name': 'dropbox',
					'uid': self.uid,
					'username': self.email
					
				}
		return data