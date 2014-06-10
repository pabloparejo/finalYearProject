function sendFileToServer(formData,status)
{
    var uploadURL = base_url + "upload/demo/"; //Upload URL
    var request=$.ajax({
            xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {

                }
            return xhrobj;
        },
	    url: uploadURL,
	    type: "POST",
	    contentType:false,
	    processData: false,
        cache: false,
        data: formData,
            success: function(data){
            console.log('uploadCompleted');
            // uploadCompleted();       
        }
    });
}
 
setFileNameSize = function(name,size){
    var sizeStr="";
    var sizeKB = size/1024;
    if(parseInt(sizeKB) > 1024)
    {
        var sizeMB = sizeKB/1024;
        sizeStr = sizeMB.toFixed(2)+" MB";
    }
    else
    {
        sizeStr = sizeKB.toFixed(2)+" KB";
    }
    console.log('showFileProgress')
    // showFileProgress(name, sizeStr);
}

function handleFileUpload(files, path)
{
   for (var i = 0; i < files.length; i++) 
   {
      var fd = new FormData();
      fd.append('file', files[i]);
      fd.append('csrfmiddlewaretoken', getCookie('csrftoken'));
      setFileNameSize(files[i].name,files[i].size);
      sendFileToServer(fd, path, status);
   }
}

var prev_html;

function addHelp(){
    prev_html = $('.dragandrophandler').html();
    $('.dragandrophandler').html('<p>Drop the file here to start uploading.</p>');
    $('.dragandrophandler').addClass('drag');
}

function removeHelp(){
    $('.dragandrophandler').html(prev_html);
    $('.dragandrophandler').removeClass('drag');
}


$(document).ready(function(){
  var obj = $(".dragandrophandler");
  obj.on('dragenter', function (e){
      e.preventDefault();
  });

  obj.on('dragover', function (e){
       e.preventDefault();
  });

  obj.on('drop', function (e){
    e.preventDefault();
    var files = e.originalEvent.dataTransfer.files;

    //We need to send dropped files to Server
    //Also, we need to tell the server the path to upload
    var nav_link = $('.crum-item').last().children('crum').attr('href');
    var upload_path = nav_link.split[base_url + '/api/get_path'][1]
    console.log(upload_path);
    handleFileUpload(files, upload_path); 
  });

  obj.on('dragstop', function (e){
    e.preventDefault();
  });

  $(document).on('dragenter', function (e){
    e.preventDefault();
  });
  $(document).on('dragover', function (e){
    e.preventDefault();
  });
  $(document).on('drop', function (e){
    e.preventDefault();


  });


  $.fn.draghover = function(options) {
    return this.each(function() {

      var collection = $(),
          self = $(this);

      self.on('dragenter', function(e) {
        if (collection.length === 0) {
          self.trigger('draghoverstart');
        }
        collection = collection.add(e.target);
      });

      self.on('dragleave drop', function(e) {
        collection = collection.not(e.target);
        if (collection.length === 0) {
          self.trigger('draghoverend');
        }
      });
    });
  };

  $(window).draghover().on({
    'draghoverstart': function() {
      addHelp();
      $('body').css('cursor', 'copy');
    },
    'draghoverend': function() {
      removeHelp();
      $('body').css('cursor', 'default');
    }
  });
});

