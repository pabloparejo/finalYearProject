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
		return "Service: Dropbox | User: %s" %(self.service_email)

	def get_path(self, path):
		client = DropboxClient(self.token)
		metadata_list = client.metadata(path)['contents']

		#metadata_list = [{u'size': u'0 bytes', 'name': u'Adaba', u'rev': u'1962e03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Sun, 03 Nov 2013 12:03:27 +0000', u'path': u'/Adaba', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 103982}, {u'size': u'0 bytes', 'name': u'Aplicaciones', u'rev': u'2159603eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Wed, 12 Mar 2014 17:42:51 +0000', u'path': u'/Aplicaciones', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 136598}, {u'size': u'0 bytes', 'name': u'Camera uploads', u'rev': u'9cec03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Wed, 28 Nov 2012 16:23:10 +0000', u'path': u'/Camera uploads', u'is_dir': True, u'icon': u'folder_photos', u'root': u'dropbox', u'revision': 40172}, {u'size': u'32.2 KB', 'name': u'Captura de pantalla 2013-09-23 a la(s) 21.40.50.png', u'rev': u'129d103eff6f0', u'thumb_exists': True, u'bytes': 33000, u'modified': u'Mon, 23 Sep 2013 19:41:01 +0000', u'mime_type': u'image/png', u'path': u'/Captura de pantalla 2013-09-23 a la(s) 21.40.50.png', u'is_dir': False, u'icon': u'page_white_picture', u'root': u'dropbox', u'client_mtime': u'Mon, 23 Sep 2013 19:40:54 +0000', u'revision': 76241}, {u'size': u'69.4 KB', 'name': u'Captura de pantalla 2014-03-25 a la(s) 17.39.18.png', u'rev': u'21aaa03eff6f0', u'thumb_exists': True, u'bytes': 71062, u'modified': u'Tue, 25 Mar 2014 16:40:23 +0000', u'mime_type': u'image/png', u'path': u'/Captura de pantalla 2014-03-25 a la(s) 17.39.18.png', u'is_dir': False, u'icon': u'page_white_picture', u'root': u'dropbox', u'client_mtime': u'Tue, 25 Mar 2014 16:39:27 +0000', u'revision': 137898}, {u'size': u'0 bytes', 'name': u'carpeta', u'rev': u'2130f03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Sat, 08 Mar 2014 18:07:33 +0000', u'path': u'/carpeta', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 135951}, {u'size': u'0 bytes', 'name': u'ChuChuChuLi', u'rev': u'1b27503eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Sat, 16 Nov 2013 17:11:10 +0000', u'path': u'/ChuChuChuLi', u'is_dir': True, u'icon': u'folder_user', u'root': u'dropbox', u'revision': 111221}, {u'size': u'44.8 KB', 'name': u'CLASES.pdf', u'rev': u'8d5f03eff6f0', u'thumb_exists': False, u'bytes': 45875, u'modified': u'Tue, 06 Nov 2012 09:57:46 +0000', u'mime_type': u'application/pdf', u'path': u'/CLASES.pdf', u'is_dir': False, u'icon': u'page_white_acrobat', u'root': u'dropbox', u'client_mtime': u'Tue, 06 Nov 2012 09:57:54 +0000', u'revision': 36191}, {u'size': u'0 bytes', 'name': u'Corto - ecdlv', u'rev': u'1215f03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Mon, 17 Jun 2013 20:00:47 +0000', u'path': u'/Corto - ecdlv', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 74079}, {u'size': u'141.5 KB', 'name': u'Curriculum_Pablo_Parejo.docx', u'rev': u'2208c03eff6f0', u'thumb_exists': False, u'bytes': 144915, u'modified': u'Thu, 24 Apr 2014 18:43:07 +0000', u'mime_type': u'application/vnd.openxmlformats-officedocument.wordprocessingml.document', u'path': u'/Curriculum_Pablo_Parejo.docx', u'is_dir': False, u'icon': u'page_white_word', u'root': u'dropbox', u'client_mtime': u'Thu, 24 Apr 2014 18:43:03 +0000', u'revision': 139404}, {u'size': u'101.1 KB', 'name': u'Curriculum_Pablo_Parejo.pdf', u'rev': u'18b4d03eff6f0', u'thumb_exists': False, u'bytes': 103555, u'modified': u'Wed, 16 Oct 2013 11:47:38 +0000', u'mime_type': u'application/pdf', u'path': u'/Curriculum_Pablo_Parejo.pdf', u'is_dir': False, u'icon': u'page_white_acrobat', u'root': u'dropbox', u'client_mtime': u'Wed, 16 Oct 2013 11:47:36 +0000', u'revision': 101197}, {u'size': u'0 bytes', 'name': u'Curso iOS', u'rev': u'a8e903eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Thu, 29 Nov 2012 18:48:18 +0000', u'path': u'/Curso iOS', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 43241}, {u'size': u'0 bytes', 'name': u'cursosMejorandola', u'rev': u'21aab03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Tue, 25 Mar 2014 18:29:50 +0000', u'path': u'/cursosMejorandola', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 137899}, {u'size': u'0 bytes', 'name': u'Fonts', u'rev': u'122be03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Tue, 25 Jun 2013 16:48:21 +0000', u'path': u'/Fonts', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 74430}, {u'size': u'118.5 KB', 'name': u'Formas personalizadas sin t\xedtulo.csh', u'rev': u'2208603eff6f0', u'thumb_exists': False, u'bytes': 121364, u'modified': u'Wed, 23 Apr 2014 09:11:09 +0000', u'mime_type': u'text/x-csh', u'path': u'/Formas personalizadas sin t\xedtulo.csh', u'is_dir': False, u'icon': u'page_white', u'root': u'dropbox', u'client_mtime': u'Wed, 23 Apr 2014 09:11:05 +0000', u'revision': 139398}, {u'size': u'0 bytes', 'name': u'Fotos csur', u'rev': u'2190d03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Mon, 24 Mar 2014 22:59:32 +0000', u'path': u'/Fotos csur', u'is_dir': True, u'icon': u'folder_user', u'root': u'dropbox', u'revision': 137485}, {u'size': u'12 bytes', 'name': u'hola.txt', u'rev': u'215f003eff6f0', u'thumb_exists': False, u'bytes': 12, u'modified': u'Thu, 13 Mar 2014 12:28:07 +0000', u'mime_type': u'text/plain', u'path': u'/hola.txt', u'is_dir': False, u'icon': u'page_white_text', u'root': u'dropbox', u'client_mtime': u'Thu, 13 Mar 2014 12:28:07 +0000', u'revision': 136688}, {u'size': u'120.9 KB', 'name': u'icono.jpg', u'rev': u'11d6a03eff6f0', u'thumb_exists': True, u'bytes': 123785, u'modified': u'Sat, 27 Apr 2013 16:18:40 +0000', u'mime_type': u'image/jpeg', u'path': u'/icono.jpg', u'is_dir': False, u'icon': u'page_white_picture', u'root': u'dropbox', u'client_mtime': u'Sat, 27 Apr 2013 16:18:36 +0000', u'revision': 73066}, {u'size': u'7.1 MB', 'name': u'ML02.bin', u'rev': u'7b2603eff6f0', u'thumb_exists': False, u'bytes': 7415072, u'modified': u'Thu, 10 May 2012 15:29:11 +0000', u'mime_type': u'application/octet-stream', u'path': u'/ML02.bin', u'is_dir': False, u'icon': u'page_white', u'root': u'dropbox', u'client_mtime': u'Wed, 21 Dec 2011 16:40:29 +0000', u'revision': 31526}, {u'size': u'0 bytes', 'name': u'Otros', u'rev': u'211f303eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Thu, 06 Mar 2014 11:46:58 +0000', u'path': u'/Otros', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 135667}, {u'size': u'0 bytes', 'name': u'Photos', u'rev': u'a03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Mon, 12 Sep 2011 00:37:53 +0000', u'path': u'/Photos', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 10}, {u'size': u'297.3 KB', 'name': u'Pr\xe1ctica4.pdf', u'rev': u'1dc8703eff6f0', u'thumb_exists': False, u'bytes': 304459, u'modified': u'Sat, 07 Dec 2013 16:36:13 +0000', u'mime_type': u'application/pdf', u'path': u'/Pr\xe1ctica4.pdf', u'is_dir': False, u'icon': u'page_white_acrobat', u'root': u'dropbox', u'client_mtime': u'Mon, 18 Nov 2013 20:06:10 +0000', u'revision': 121991}, {u'size': u'0 bytes', 'name': u'Proyecto 3D(Minecraft)', u'rev': u'e0b703eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Sat, 16 Mar 2013 12:51:01 +0000', u'path': u'/Proyecto 3D(Minecraft)', u'is_dir': True, u'icon': u'folder_user', u'root': u'dropbox', u'revision': 57527}, {u'size': u'0 bytes', 'name': u'Public', u'rev': u'b03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Mon, 12 Sep 2011 00:37:53 +0000', u'path': u'/Public', u'is_dir': True, u'icon': u'folder_public', u'root': u'dropbox', u'revision': 11}, {u'size': u'0 bytes', 'name': u'rest', u'rev': u'2159c03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Wed, 12 Mar 2014 18:17:59 +0000', u'path': u'/rest', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 136604}, {u'size': u'102 KB', 'name': u'resume.docx', u'rev': u'2209c03eff6f0', u'thumb_exists': False, u'bytes': 104449, u'modified': u'Mon, 28 Apr 2014 07:21:00 +0000', u'mime_type': u'application/vnd.openxmlformats-officedocument.wordprocessingml.document', u'path': u'/resume.docx', u'is_dir': False, u'icon': u'page_white_word', u'root': u'dropbox', u'client_mtime': u'Sun, 27 Apr 2014 08:47:10 +0000', u'revision': 139420}, {u'size': u'0 bytes', 'name': u'Shirts', u'rev': u'ab8403eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Thu, 13 Dec 2012 20:35:54 +0000', u'path': u'/Shirts', u'is_dir': True, u'icon': u'folder_user', u'root': u'dropbox', u'revision': 43908}, {u'size': u'0 bytes', 'name': u'stepOne', u'rev': u'2209b03eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Mon, 28 Apr 2014 07:20:57 +0000', u'path': u'/stepOne', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 139419}, {u'size': u'2.1 MB', 'name': u'Todos recortada.JPG', u'rev': u'127c303eff6f0', u'thumb_exists': True, u'bytes': 2197185, u'modified': u'Thu, 08 Aug 2013 01:22:40 +0000', u'mime_type': u'image/jpeg', u'path': u'/Todos recortada.JPG', u'is_dir': False, u'icon': u'page_white_picture', u'root': u'dropbox', u'client_mtime': u'Sun, 13 Jan 2013 08:02:12 +0000', u'revision': 75715}, {u'size': u'0 bytes', 'name': u'Uni', u'rev': u'1103eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Fri, 30 Sep 2011 22:31:53 +0000', u'path': u'/Uni', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 17}, {u'size': u'0 bytes', 'name': u'Uploads', u'rev': u'21cd703eff6f0', u'thumb_exists': False, u'bytes': 0, u'modified': u'Tue, 01 Apr 2014 21:18:45 +0000', u'path': u'/Uploads', u'is_dir': True, u'icon': u'folder', u'root': u'dropbox', u'revision': 138455}, {u'size': u'402 bytes', 'name': u'ybCJjqr.png', u'rev': u'12b3503eff6f0', u'thumb_exists': True, u'bytes': 402, u'modified': u'Tue, 01 Oct 2013 19:20:23 +0000', u'mime_type': u'image/png', u'path': u'/ybCJjqr.png', u'is_dir': False, u'icon': u'page_white_picture', u'root': u'dropbox', u'client_mtime': u'Tue, 01 Oct 2013 19:14:40 +0000', u'revision': 76597}]

		for data in metadata_list:
			data['name'] = data['path'][1:] 
		data = {	'contents': metadata_list,
					'display_name': self.display_name,
					'parent': path,
					'service_name': 'Dropbox',
					'uid': self.uid,
					'username': self.email
					
				}
		return data


    # client = DropboxClient(service.service_token)
    # metadata_list = client.metadata(path)['contents']
    # for element in metadata_list:
    #             if element['is_dir']:
    #                 element['url'] = ('/' + service.service + '/'
    #                               + service.service_email.split('@')[0]
    #                               + element['path'])
    #             else:
    #                 element['url'] = ('/file/' + service.service + '/'
    #                               + service.service_email.split('@')[0]
    #                               + element['path'])
    # accountsAreActive = True
    # listOfAccounts = [service.service_email]
    # return render(request,  'dropbox.html', locals())