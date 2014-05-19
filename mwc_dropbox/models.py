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
		files_list = client.metadata(path)['contents']
		quota_info = client.account_info()['quota_info']

		if path != '/':	#It's faster to check path once time than check in loop
			for item in files_list:
				item['name'] = item['path'].split(path, 1)[-1][1:]
		else:
			for item in files_list:
				item['name'] = item['path'][1:]

		data = {	'bytes_total': quota_info['quota'],
					'bytes_used': quota_info['normal'] + quota_info['shared'],
					'contents': files_list,
					'display_name': self.display_name,
					'parent': path,
					'service_class': 'dropbox',
					'service_name': 'dropbox',
					'uid': self.uid,
					'username': self.email
					
				}
		return data