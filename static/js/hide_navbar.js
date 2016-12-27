function main() {
  $('#navbar').hide();
  $('#nav_text').on('click', function() {
 $('#navbar').slideToggle(200);
});
}

$(document).ready(main);