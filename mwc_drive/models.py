from django.db import models
from django.contrib.auth.models import User

import httplib2, datetime
from apiclient.discovery import build
from oauth2client.django_orm import Storage


from oauth2client.django_orm import FlowField, CredentialsField, Storage

class DriveAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()

	user = models.ForeignKey(User)

	def format_size(self, bytes):
		size = int(bytes)
		if size < 1024:
			return bytes + " bytes"
		elif size < 1024**2:
			size = size/1024
			return str(size) + " KB"
		elif size < 1024**3:
			size = size/1024**2
			return str(size) + " MB"
		else:
			size = size/1024**3
			return str(size) + " GB"


	def reformat_metadata(self, metadata_list):
		for element in metadata_list:
			element['name'] = element.pop('title')
			element['icon'] = element.pop('mimeType')
			element['size'] = self.format_size(element['quotaBytesUsed'])
			# DELETE SENTENCE BELOW WHEN WE ADD JQUERY TO MAKE THE API CALL
			# EXPLANATION: THE FOLDER IS GOING TO HAVE A GOOGLE DRIVE CLASS
			element['path'] = element['id']
		return metadata_list

	def files_for_parent(self, metadata_list, path_id):
		files = []
		path = path_id.split('/')[-1:]
		for element in metadata_list:
			for parent in element['parents']:
				if parent['id'] == path[0] and \
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

		then = datetime.datetime.now()
		quota_info = drive_service.about().get().execute()
		print "First google response time" , datetime.datetime.now() - then
		files_list = drive_service.files().list().execute()['items']
		print "Total google response time" , datetime.datetime.now() - then
		if path == '/':
			files_list = self.files_in_root(files_list)
		else:
			files_list = self.files_for_parent(files_list, path)
		files_list = self.reformat_metadata(files_list)

		data = {	'bytesTotal':	int(quota_info['quotaBytesTotal']),
					'bytesUsed':	int(quota_info['quotaBytesUsed']) +
									int(quota_info['quotaBytesUsedAggregate']) +
									int(quota_info['quotaBytesUsedInTrash']),
					'contents': files_list,
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