window.onload = function () {
$(window).on("scroll", function(){
	$('input[name="scroll"]').val($(window).scrollTop());
});

$(document).ready(function(){
	var p = window.location.search;
	p = p.match(new RegExp('scroll=([^&=]+)'));
	if (p) {
		window.scrollTo(0, p[1]);
	}
});
}

