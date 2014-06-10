from django.db import models
from django.contrib.auth.models import User

from dropbox.client import DropboxClient

from myWholeCloud.settings import SITE_URL

import re

# Create your models here.
class DropboxAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()
	token = models.CharField(max_length=100)

	user = models.ForeignKey(User)

	
	def __unicode__(self):
		return self.email

	def delete_account(self):
		print "Is disable_access_token() fixed yet?"
		#client = DropboxClient(self.token)
		#client.disable_access_token()  ---- This function is not working

		self.delete()


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

		if path != '/':
			path = '/' + path.replace("%20", " ")
			path_regex = re.compile(path, re.IGNORECASE)
			for item in files_list:
				item['name'] = path_regex.split(item['path'], 1)[-1][1:]
				item['path'] = '/' + item['name']
		else:
			for item in files_list:
				item['path'] = item['path'][1:]
				item['name'] = item['path']

		parent_url = (SITE_URL + 'api/path/dropbox/%i' + path) %self.uid
		upload_url = (SITE_URL + 'api/upload/dropbox/%i' + path) %self.uid

		data = {	'bytes_total': quota_info['quota'],
					'bytes_used': quota_info['normal'] + quota_info['shared'],
					'contents': files_list,
					'display_name': self.display_name,
					'parent_path': parent_url,
					'service_class': 'dropbox',
					'service_name': 'dropbox',
					'uid': self.uid,
					'upload_path': upload_url,
					'username': self.email
					
				}
		return data

	def upload_file(self, f, path='/'):
		client = DropboxClient(self.token)
		print f
		# put_file max size is 150MB
		client.put_file(path + f.name, f, overwrite=True, parent_rev=None)


