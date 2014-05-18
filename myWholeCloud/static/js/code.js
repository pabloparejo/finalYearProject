var base_url 		= "http://127.0.0.1/api/",
	$files_list		= $('#files-list'),
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
	link = $(this).find('.get-path-btn').attr('href');
	console.log(link);

	$.getJSON(link, navigation);
}


var myData
function navigation(data){
	myData = data; // DEVELOPING ONLY
	$first_clone = $files_list.children().first().clone();
	$files_list.children().fadeOut().remove();
	for (item in data.contents){
		$clone = $first_clone.clone();
		$clone.find('.name a').text(data.contents[item].name)
		console.log('We have to change items icons, class and id');
		console.log('modification key is different between services');
		//$clone.('.item-mod').text(data.contents[item].modified)
		$clone.find('.size').text(data.contents[item].size)
		$files_list.append($clone);
		$clone.fadeIn();
	}

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
$search_btn.click(searchToggle);

$('.service-link').hover(toggleShowChildren, removeTimeOut)

$('ul.item').click(get_path);






