from django.db import models
from django.contrib.auth.models import User

from dropbox.client import DropboxClient

from myWholeCloud.settings import SITE_URL

# Create your models here.
class DropboxAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()
	token = models.CharField(max_length=100)

	user = models.ForeignKey(User)

	
	def __unicode__(self):
		return self.email

	def get_free_space(self):
		client = DropboxClient(self.token)
		quota_info = client.account_info()['quota_info']
		free = 	quota_info['quota'] - quota_info['normal'] - \
				quota_info['shared']
		return free

	def get_path(self, path):
		client = DropboxClient(self.token)
		files_list = client.metadata(path)['contents']
		quota_info = client.account_info()['quota_info']

		if path != '/':	#It's faster to check path once time than check in loop
			path = path.replace("%20", " ")
			for item in files_list:
				item['name'] = item['path'].split(path, 1)[-1][1:]
				print path
				print item['name']

			path = "/" + path + "/"

		else:
			for item in files_list:
				item['name'] = item['path'][1:]

		parent_url = (SITE_URL + 'api/get_path/dropbox/%i' + path) %self.uid

		data = {	'bytes_total': quota_info['quota'],
					'bytes_used': quota_info['normal'] + quota_info['shared'],
					'contents': files_list,
					'display_name': self.display_name,
					'parent_url': parent_url,
					'service_class': 'dropbox',
					'service_name': 'dropbox',
					'uid': self.uid,
					'username': self.email
					
				}
		return data

	def upload_file(self, f, path='/'):
			client = DropboxClient(self.token)
			print f
			# put_file max size is 150MB
			client.put_file(path + f.name, f, overwrite=True, parent_rev=None)


