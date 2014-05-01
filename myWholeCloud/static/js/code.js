var base_url 		= "http://query.yahooapis.com/v1/public/yql?",
	$content 		= $('#content'),
	positionCoords	= {},
	$ls				= localStorage,
	$sign_form		= $('#sign-form')
	path 			= location.pathname.split('/')[1],
	$user_btn		= $('#user'),
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

// -------- DAJAX ICE -------- //

$('.switchForm-btn').click(DajaxSwitchForm);

function DajaxSwitchForm(e){
	e.preventDefault();
	Dajaxice.userprofiles.switchForm(switchFormFields);
}

function switchFormFields(data){

	clone = $('.sign').clone();
	clone.find('.form-title').text(data.title);
	clone.find('.submit-btn').attr('value', data.title);
	clone.find('.form-content').html(data.content);
	clone.find('.switchForm-btn').text($('.form-title').text());
	$('.sign').slideUp();
	$('#content').prepend(clone);
	clone.hide();
	clone.slideDown();
	setCookie('form', data.cookie, 7);
	$('.switchForm-btn').click(DajaxSwitchForm);
	setTimeout(function(){
		$('.sign').last().remove();
	}, 500);

}


function searchToggle(){
	toggleBtnActive($search_btn)
	$search.toggleClass('show');
	$search.slideToggle();
}

function formToggle(){
	toggleBtnActive($user_btn)
	$sign_form.toggleClass('show');
	$sign_form.slideToggle();
}


setActive();
$user_btn.click(formToggle);
$search_btn.click(searchToggle);

if (path == "checkout-succes"){
	clearCart();
}

