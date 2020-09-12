
// Activate the toggle switch
$(document).ready(function() {
   $('.toggle').change(function(e) {
     let current_status
    //  var current_status = $('.status').text();
    console.log("ID", e.target.id)
     switch (e.target.id) {
      case 'develop':
        current_status = 'Developer Mode';
          break;
      case 'analyst':
        current_status = 'Analyst Mode';
          break;
        }
      // Update the toggle value
      $.ajax({
       url: "/get_toggled_status",
       type: "get",
        data: {status: current_status},
        success: function(response) {
          console.log("RES", response)
         $(".status").html(response);
         $(".dev-mode").html(response);
        },
        error: function(xhr) {
         //Do Something to handle error
         console.log("error")
        }
      });


    })
  })
