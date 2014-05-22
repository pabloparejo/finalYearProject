var base_url 		= "http://127.0.0.1:8000/api/",
	$breadcrums		= $('#breadcrums')
	$files_list		= $('#files-list'),
	$ls				= localStorage,
	nav_path 		= [''],
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

function back_to_path(e){
	e.preventDefault();
	disable_ajax();
	ajax_progress(20);
	console.log(this);
	var link = $(this).find('a').attr('href');
	ajax_progress(60);
	var jqxhr = $.getJSON(link, path_navigation)
		.done(function(){
			ajax_progress(80);
			pop_crum();
			enable_ajax();
		})
		.fail(ajax_error);
}

function get_path(e){
	e.preventDefault();
	disable_ajax();
	ajax_progress(20);
	console.log(this);
	var path_name = $(this).find('li.name a').text();
	var link = $(this).find('li.name a').attr('href');
	console.log(link);
	ajax_progress(60);
	var jqxhr = $.getJSON(link, path_navigation)
		.done(function(){
			push_crum(path_name, link);
			ajax_progress(75);
			enable_ajax();
		})
		.fail(ajax_error);
}

function disable_ajax(){
	$breadcrums.children().unbind('click');//User's clicks before the call are disabled
	$breadcrums.children().click(function(e){
		e.preventDefault();
	});
	$('ul.item').unbind('click'); //User's clicks before the call are disabled
	$('ul.item').click(function(e){
		e.preventDefault();
	});
}

function enable_ajax(){
	$('#files-home').unbind('click')
	$('#files-home').click(get_home);
	$breadcrums.children('.crum-item').click(back_to_path);
	$breadcrums.children().last().unbind('click').click(function(e){
		e.preventDefault();
	})
}

function get_home(e){
	e.preventDefault();
	disable_ajax();
	ajax_progress(20);
	var link = base_url + 'get_path/';
	console.log(link);
	ajax_progress(60);
	var jqxhr = $.getJSON(link, display_home)
		.done(function(){
			remove_crums();
			ajax_progress(75);
			enable_ajax();
		})
		.fail(ajax_error);
}

// -------- AJAX Response handlers -------- //
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
			$("#ajax-bar").fadeOut('slow');
			window.setTimeout(function(){
				$("#ajax-bar").width(0);
				$("#ajax-bar").show();
			}, 1000)
			
		}
	}
}

function ajax_error(){
	$('#ajax-bar').fadeOut('fast');
	$('#ajax-error').slideDown('slow');
	window.setTimeout(function(){
		$('#ajax-bar').width(0);
		$('#ajax-bar').fadeIn();
		$('#ajax-error').slideUp('slow');}
		, 5000);
}

function display_content_items(parent_url, items, $first_clone){
	for (item in items){
		var $clone = $first_clone.clone();
		var $clone_link = $clone.find('.name a')
		$clone_link.text(items[item].name);
		$clone_link.attr('href', parent_url + items[item].path);
		$clone.find('span').removeClass().addClass('big-icon icon-' + items[item].icon);
		if (items[item].is_dir){
			$clone.find('.size').text('--');
		} else if (items[item].icon == 'application/vnd.google-apps.folder'){
			$clone.find('.size').text('--');
		}else{
			$clone.find('.size').text(items[item].size);
		}
		$files_list.append($clone);
		$clone.fadeIn();
	}
	ajax_progress(95);
}

function display_home(data){
	myData = data; // DEVELOPING ONLY
	ajax_progress(85);
	var $first_clone = $files_list.children().first().clone();
	$files_list.children().fadeOut();
	$files_list.children().remove();
	for (service_i in data.services){
		parent_url = data.services[service_i].parent_url
		contents = data.services[service_i].contents
		display_content_items(parent_url, contents, $first_clone)
	}
	ajax_progress(100);
	$('ul.item').click(get_path);
	$('ul.item').hover(scrollUpName, scrollDownName);
}

var myData
function path_navigation(data){
	myData = data; // DEVELOPING ONLY
	ajax_progress(85);
	var $first_clone = $files_list.children().first().clone();
	$files_list.children().fadeOut();
	$files_list.children().remove();
	display_content_items(data.parent_url, data.contents, $first_clone)
	ajax_progress(100);
	$('ul.item').click(get_path);
	$('ul.item').hover(scrollUpName, scrollDownName);
}

var $span
function push_crum(path_name, link){
	console.log(path_name);
	nav_path[nav_path.length] = path_name  //Faster than push in small arrays
	var $crum = $breadcrums.children().first().clone();
	var $crum_link = $crum.find('a');
	$crum_link.removeAttr('id').addClass('crum-item')
	$span = $crum_link.find('span');
	$span.removeClass().addClass('icon-crum-arrow big-icon yellow');
	$crum_link.attr('href', link)
	$crum_link.find('p').text(path_name);
	$crum_link.prepend($span);
	$crum.hide();
	$breadcrums.append($crum);
	$crum.prev().unbind('click').click(back_to_path);
	$crum.click(function(e){
		e.preventDefault();
	})
	$crum.show('slow');
}

function pop_crum(){
	nav_path.pop();
	var $crum = $breadcrums.children('.crum-item').last().hide('slow');
	$crum.remove();
}

function remove_crums(){
	$breadcrums.children().fadeOut();
	var $home = $breadcrums.children().first().clone();
	nav_path = [''];
	$breadcrums.children().remove();
	$breadcrums.append($home).show();
	$('#files-home').click(get_home);
}

var scrollUpInterval;
function scrollUpName(){
	var $item_name = $(this).find('li.name a');
	var prev = 0
	scrollUpInterval = window.setInterval(function(){
		prev = $item_name.scrollTop();
		$item_name.scrollTop(prev + 1);
		if (prev >= $item_name.scrollTop()){
			clearInterval(scrollUpInterval);
		}
	}, 15);
}

function scrollDownName(){
	clearInterval(scrollUpInterval);
	var $item_name = $(this).find('li.name a');
	var prev = 0
	var scrollDownInterval = window.setInterval(function(){
		prev = $item_name.scrollTop();
		$item_name.scrollTop(prev - 1);
		if (prev <= $item_name.scrollTop()){
			clearInterval(scrollDownInterval);
		}
	}, 10);
}


setActive();
enable_ajax();
$('#upload-btn').click(uploadToggle);
$('ul.item').click(get_path);
$('ul.item').hover(scrollUpName, scrollDownName);







