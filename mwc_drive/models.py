from django.db import models
from django.contrib.auth.models import User

import httplib2
from apiclient.discovery import build
from oauth2client.django_orm import Storage


from oauth2client.django_orm import FlowField, CredentialsField, Storage

class DriveAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()

	user = models.ForeignKey(User)


	def reformat_metadata(self, metadata_list):
		for element in metadata_list:
			element['name'] = element.pop('title')
			element['icon'] = element.pop('mimeType')
		return metadata_list

	def files_for_parent(self, metadata_list, path_id):
		files = []
		for element in metadata_list:
			for parent in element['parents']:
				if parent['id'] == path_id and \
				not element.has_key('explicitlyTrashed'):
					files.append(element)
		return files

	def files_in_root(self, metadata_list):
		files = []
		for element in metadata_list:
			for parent in element['parents']:
				if parent['isRoot'] and \
				not element.has_key('explicitlyTrashed'):
					files.append(element)
					break
		return files

	def get_path(self, path):

		credentials_model = CredentialsModel.objects.get(drive_account=self.pk)
		credentials = credentials_model.credential
		http = httplib2.Http()
		http = credentials.authorize(http)
		drive_service = build('drive', 'v2', http=http)
		metadata_list = drive_service.files().list().execute()['items']
		if path == '/':
			metadata_list = self.files_in_root(metadata_list)
		else:
			metadata_list = self.files_for_parent(metadata_list, path_id)
		metadata_list = self.reformat_metadata(metadata_list)

		data = {	'contents': metadata_list,
					'display_name': self.display_name,
					'parent': path,
					'service_class': 'google-drive',
					'service_name': 'Google Drive',
					'uid': self.uid,
					'username': self.email
					
				}

		return data

	def __unicode__(self):
		return self.email

class FlowModel(models.Model):
	id = models.ForeignKey(User, primary_key=True)
	flow = FlowField()

class CredentialsModel(models.Model):
	drive_account = models.ForeignKey(DriveAccount, blank=True, null=True)
	user = models.ForeignKey(User)
	credential = CredentialsField()


	def __unicode__(self):
		return "id: %s /n credential: %s" %(self.id, self.credential)