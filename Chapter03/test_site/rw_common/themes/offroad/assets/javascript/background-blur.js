
$(document).ready(function(){$('<div class="blurred" style="background-image: '+$('body').css('background-image')+'"></div>').insertAfter('.body-overlay')
$(window).scroll(function(){var opacity=($(window).scrollTop()/300)
$('.blurred').css('opacity',opacity)})})