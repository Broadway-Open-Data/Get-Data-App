
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


// Allow searching through the table
document.addEventListener('DOMContentLoaded', function() {
  // Quick Table Search
  $('#search').keyup(function() {
    var regex = new RegExp($('#search').val(), "i");
    var rows = $('#show-data > tbody > tr');
    rows.each(function (index) {
      title = $(this).find("td").eq(2).html()
      if (title.search(regex) != -1) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  });
});
