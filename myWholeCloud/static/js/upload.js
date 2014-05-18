function sendFileToServer(formData,status)
{
    var uploadURL ="http://127.0.0.1:8000/api/upload/demo/"; //Upload URL
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
            console.log('uploaded')
            $("#status1").append("File upload Done<br>");         
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

    // this.filename.html(name);
    console.log(name);
    console.log(sizeStr);
    // this.size.html(sizeStr);
}

function handleFileUpload(files,obj)
{
   for (var i = 0; i < files.length; i++) 
   {
        var fd = new FormData();
        fd.append('file', files[i]);
 		fd.append('csrfmiddlewaretoken', getCookie('csrftoken'));
        setFileNameSize(files[i].name,files[i].size);
        sendFileToServer(fd,status);
   }
}
$(document).ready(function(){
  var obj = $(".dragandrophandler");
  obj.on('dragenter', function (e){
      e.stopPropagation();
      e.preventDefault();
      $(this).addClass('drag');
  });
  obj.on('dragover', function (e){
       e.stopPropagation();
       e.preventDefault();
  });
  obj.on('drop', function (e){
   
       $(this).removeClass('drag');
       e.preventDefault();
       var files = e.originalEvent.dataTransfer.files;
   
       //We need to send dropped files to Server
       handleFileUpload(files,obj);
  });

  obj.on('dragstop', function (e){
       e.stopPropagation();
       e.preventDefault();
       $(this).removeClass('drag');
  });

  $(document).on('dragenter', function (e){
      e.stopPropagation();
      e.preventDefault();
      $(this).addClass('drag');
  });
  $(document).on('dragover', function (e){
    e.stopPropagation();
    e.preventDefault();
  });
  $(document).on('drop', function (e){
      e.stopPropagation();
      e.preventDefault();
      $(this).removeClass('drag');
  });
});