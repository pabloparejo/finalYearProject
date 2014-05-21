var base_url 		= "http://127.0.0.1:8000/api/",
	$files_home		= $('#files-home'),
	$files_list		= $('#files-list'),
	$ls				= localStorage,
	path 			= location.pathname.split('/')[1],
	$upload			= $('#upload-area')


function setActive(){
	$('.active').removeClass();
	if (!path){
		path = 'home';
	}
	$('#' + path + ' a').addClass('active');

	if (path == "checkout"){
		$cart_btn.addClass('active')
	}
}

function toggleBtnActive(btn){
	if (btn.hasClass('active')) {
		setActive();
	}else{
		$('.active').removeClass();
		btn.addClass('active');
	}
}

// -------- COOKIES -------- //

function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires+ ";path=/;";
}

function getCookie(cname){
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++){
		var c = ca[i].trim();
		if (c.indexOf(name)==0) return c.substring(name.length,c.length);
	}
		return "";
	}


function uploadToggle(){
	$upload.slideToggle();
	$files_list.slideToggle();
}

// -------- AJAX -------- //

function ajax_progress(percent){
	var max_width = $("#bar-container").width();
	var width = $("#ajax-bar").width();
	var width_percent = width*100/max_width
	var rand = Math.random();
	if (percent > Math.floor(width_percent)){
		$("#ajax-bar").width(width_percent + (1.5*(rand)) +"%");
		if (Math.floor(width_percent) >= 99){
			$("#ajax-bar").width(0);
		}else{
			window.setTimeout(function(){
				ajax_progress(percent);
			}, 15)
		}
	}else{
		if (Math.floor(width_percent) >= 99){
			$("#ajax-bar").width(0);
		}
	}
}

function get_path(e){
	e.preventDefault();
	ajax_progress(20);
	link = $(this).find('.get-path-btn').attr('href');
	console.log(link);
	ajax_progress(60);
	$.getJSON(link, path_navigation);
	ajax_progress(75);
}

function get_home(e){
	e.preventDefault();
	ajax_progress(20);
	link = base_url + 'get_path/';
	console.log(link);
	ajax_progress(60);
	$.getJSON(link, display_home);
	ajax_progress(75);
}

// -------- AJAX Response handlers -------- //

function display_content_items(items){
	for (item in items){
		console.log(items[item]);
		$clone = $first_clone.clone();
		$clone.find('.name a').text(items[item].name);
		//$clone.('.item-mod').text(items[item].modified);
		$clone.find('.size').text(items[item].size);
		$files_list.append($clone);
		$clone.fadeIn();
	}
}

function display_home(data){
	myData = data; // DEVELOPING ONLY
	ajax_progress(80);
	$first_clone = $files_list.children().first().clone();
	$files_list.children().fadeOut();
	console.log('We have to change items icons, class and id.');
	console.log('Dict key is different between services.');
	console.log('If item === folder --> size = "--"');
	ajax_progress(90);
	$files_list.children().remove();
	for (service_i in data.services){
		display_content_items(data.services[service_i].contents)
	}
	ajax_progress(100);
}


var myData
function path_navigation(data){
	myData = data; // DEVELOPING ONLY
	ajax_progress(80);
	$first_clone = $files_list.children().first().clone();
	$files_list.children().fadeOut();
	console.log('We have to change items icons, class and id.');
	console.log('Dict key is different between services.');
	console.log('If item === folder --> size = "--"');
	ajax_progress(90);
	$files_list.children().remove();
	display_content_items(data.contents)
	ajax_progress(100);
}

var childrenTimeOut;

function toggleShowChildren(){
	var parentObj = this;
	childrenTimeOut = setTimeout(function(){
		childrenTimeOut = null;
		$(parentObj).children('.service-email').animate({width: 'toggle'});
	}, 240);
}

function removeTimeOut(){
	if (!childrenTimeOut){
		$(this).children('.service-email').animate({width: 'toggle'});
	}
	clearTimeout(childrenTimeOut);
	childrenTimeOut = null;
}

// -------- Navigation -------- //
function filter(e){
	e.preventDefault();
	$('ul.item').fadeOut();
	$('.'+this.id).fadeIn();
}

function displayAll(e){
	e.preventDefault();
	$('ul.item').fadeIn();
}


setActive();
// $('.get-path-btn').click(get_path);
$('.service-link').click(filter);
$('#all-services').click(displayAll);
$('#upload-btn').click(uploadToggle);

$('.service-link').hover(toggleShowChildren, removeTimeOut)

$('ul.item').click(get_path);

$files_home.click(get_home);






