// Enable js to hide content on the page...

function closeDiv(){
   //do something
   var x = document.getElementById("close-alert");
   x.parentNode.style.display = 'none';
}


// Make the header sticky
document.addEventListener("readystatechange", function() {
  // When the user scrolls the page, make the header sticky
  window.onscroll = function() {makeSticky()};

  // Get the header
  var header = document.getElementById("myHeader");
  // Get the offset position of the navbar
  var sticky = header.offsetTop;

  // Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
  function makeSticky() {
    if (window.pageYOffset > sticky) {
      header.classList.add("sticky");
    } else {
      header.classList.remove("sticky");
    }
  }
}
)

// Make the footer at the bottom of the page...
document.addEventListener("readystatechange", function() {
    $('#footer').css('position', $(document).height() > $(window).height() ? "inherit" : "fixed");
});
