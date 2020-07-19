
// Only allow once the page is finished loading...
document.addEventListener("DOMContentLoaded", function() {

  var allCells = $("td, th");

  // Format your table
  allCells.on("mouseover", function() {
      var el = $(this),
          pos = el.index();
      el.parent().find("th, td").addClass("hover");
      allCells.filter(":nth-child(" + (pos+1) + ")").addClass("hover");
    })
    .on("mouseout", function() {
      allCells.removeClass("hover");
    });

});
