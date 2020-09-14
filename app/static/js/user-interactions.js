
// Activate the toggle switch
$(document).ready(function() {
   $('.toggle').change(function(e) {
     let current_status
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


// -----------------------------------------------------------------------------

  // Activate data summary
  $(document).ready(function() {

    $('#detail-level-slider').on('input change', function (e) {
       let detail_level = this.value
       console.log("ID", e.target.id)

        // Update the data summary
        $.ajax({
         url: "/summarize-data",
         type: "get",
          data: {detail_level: detail_level},
          success: function(response) {
            console.log("RES", response)
             $("#data-summary-table").html(response);

          },
          error: function(xhr) {
           //Do Something to handle error
           console.log("error")
          }
        });

      })
    })
