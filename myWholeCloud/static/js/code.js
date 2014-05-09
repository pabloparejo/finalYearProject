var base_url 		= "http://127.0.0.1/api/",
	$ls				= localStorage,
	path 			= location.pathname.split('/')[1],
	$search			= $('#search-bar'),
	$search_btn 	= $("#search a");


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


function searchToggle(){
	toggleBtnActive($search_btn)
	$search.toggleClass('show');
	$search.slideToggle();
}


// -------- AJAX -------- //
function get_path(e){
	e.preventDefault();
	$.getJSON(this.href, navigation);
}


var myData
function navigation(data){
	myData = data; 
}

// -------- Navigation -------- //
function filter(e){
	e.preventDefault();
	$('.item-row').fadeOut();
	$('.'+this.id).fadeIn();
}

function displayAll(e){
	e.preventDefault();
	$('.item-row').fadeOut();
	$('.item-row').fadeIn();
}


setActive();
$('#all-services').click(displayAll);
$('.get-path-btn').click(get_path);
$('.service-link').click(filter);
$search_btn.click(searchToggle);

