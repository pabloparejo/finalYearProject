from django.db import models
from django.contrib.auth.models import User

import httplib2, datetime
from apiclient.discovery import build
from oauth2client.django_orm import Storage

from myWholeCloud.settings import SITE_URL

from oauth2client.django_orm import FlowField, CredentialsField, Storage

class DriveAccount(models.Model):

	uid = models.IntegerField()
	display_name = models.CharField(max_length=200)
	email = models.EmailField()

	user = models.ForeignKey(User)

	# Important to expose the key 'icon' of the API
	mime_types =   {"application/vnd.ms-excel" : "xls",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" : "xlsx",
                    "text/xml" : "xml",
                    "application/vnd.oasis.opendocument.spreadsheet" : "ods",
                    "text/plain" : "csv",
                    "text/plain" : "tmpl",
                    'application/pdf': "pdf",
                    "application/x-httpd-php" : "php",
                    "image/jpeg" : "jpg",
                    "image/png" : "png",
                    "image/gif" : "gif",
                    "image/bmp" : "bmp",
                    "text/plain" : "txt",
                    "application/msword" : "doc",
                    "text/js" : "js",
                    "application/x-shockwave-flash" : "swf",
                    "audio/mpeg" : "mp3",
                    "application/zip" : "zip",
                    "application/rar" : "rar",
                    "application/tar" : "tar",
                    "application/arj" : "arj",
                    "application/cab" : "cab",
                    "text/html" : "html",
                    "text/html" : "htm",
                    "application/octet-stream" : "default",
                    "application/vnd.google-apps.folde" : "folder",
                    }

	def __unicode__(self):
		return self.email

	def delete_account(self):
		credentials = CredentialsModel.objects.get(drive_account=self.pk)
		credentials.delete()
		self.delete()

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


	def reformat_metadata(self, metadata_list, path):
		print path
		if path != '/' and path !='':
			for element in metadata_list:
				element['name'] = element.pop('title')
				element['icon'] = element.pop('mimeType')
				element['size'] = self.format_size(element['quotaBytesUsed'])
				element['path'] = '/' + element.pop('id')
		else:
			for element in metadata_list:
				element['name'] = element.pop('title')
				element['icon'] = element.pop('mimeType')
				element['size'] = self.format_size(element['quotaBytesUsed'])
				element['path'] = element.pop('id')
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

	def get_free_space(self):
		credentials_model = CredentialsModel.objects.get(drive_account=self.pk)
		credentials = credentials_model.credential
		http = httplib2.Http()
		http = credentials.authorize(http)
		drive_service = build('drive', 'v2', http=http)
		quota_info = drive_service.about().get().execute()

		free = 	int(quota_info['quotaBytesTotal']) - \
				int(quota_info['quotaBytesUsed']) - \
				int(quota_info['quotaBytesUsedAggregate']) - \
				int(quota_info['quotaBytesUsedInTrash'])

		return free

	def get_files(self, service):
		files_list = service.files().list(maxResults=1000).execute()
		while True:
			try:
				param = {}
				page_token = files_list['nextPageToken']
				if page_token:
					param['pageToken'] = page_token
					files = service.files().list(**param).execute()

					files_list['items'].append(files['items'])
					page_token = files.get('nextPageToken')
				if not page_token:
					break
			except:
				print 'An error occurred'
				break
		return files_list['items']


	def get_path(self, path):

		credentials_model = CredentialsModel.objects.get(drive_account=self.pk)
		credentials = credentials_model.credential
		http = httplib2.Http()
		http = credentials.authorize(http)
		drive_service = build('drive', 'v2', http=http)

		quota_info = drive_service.about().get().execute()

		files_list = self.get_files(drive_service)
		print files_list

		if path == '/' or path == '':
			files_list = self.files_in_root(files_list)
			path = ''
		else:
			files_list = self.files_for_parent(files_list, path)
		files_list = self.reformat_metadata(files_list, path)

		parent_url = (SITE_URL + 'api/path/google-drive/%i/' + path) %self.uid

		upload_url = (SITE_URL + 'api/upload/google-drive/%i/' + path) %self.uid

		data = {	'bytesTotal':	int(quota_info['quotaBytesTotal']),
					'bytesUsed':	int(quota_info['quotaBytesUsed']) +
									int(quota_info['quotaBytesUsedAggregate']) +
									int(quota_info['quotaBytesUsedInTrash']),
					'contents': files_list,
					'display_name': self.display_name,
					'parent_path': parent_url,
					'service_class': 'google-drive',
					'service_name': 'Google Drive',
					'uid': self.uid,
					'upload_path': upload_url,
					'username': self.email
					
				}

		return data

	def upload_file(self, f):
		credentials_model = CredentialsModel.objects.get(drive_account=self.pk)
		credentials = credentials_model.credential
		http = httplib2.Http()
		http = credentials.authorize(http)

		drive_service = build('drive', 'v2', http=http)

		media_body = MediaInMemoryUpload(f.name, mimetype='text/plain', resumable=True)
		body = {'description': 'A test document',
				'mimeType': 'text/plain',
				'title': f.name
			}

		f = drive_service.files().insert(body=body, media_body=media_body).execute()

class CredentialsModel(models.Model):
	drive_account = models.ForeignKey(DriveAccount, blank=True, null=True)
	user = models.ForeignKey(User)
	credential = CredentialsField()


	def __unicode__(self):
		return "id: %s /n credential: %s" %(self.id, self.credential)