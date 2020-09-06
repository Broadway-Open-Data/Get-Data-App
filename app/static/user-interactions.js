
// Activate the toggle switch
$(document).ready(function() {
   $('.toggle').click(function() {
      var current_status = $('.status').text();

      $.ajax({
       url: "/get_toggled_status",
       type: "get",
        data: {status: current_status},
        success: function(response) {
         $(".status").html(response);
        },
        error: function(xhr) {
         //Do Something to handle error
         console.log("error")
        }
      });
    })
  })
