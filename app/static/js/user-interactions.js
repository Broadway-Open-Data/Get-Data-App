
view_mode_dict = {0:"Interested",1:"Analyst",2:"Developer"}
// // Activate the toggle switch
$(document).ready(function() {
   $('.toggle').change(function(e) {

    // Simplified things
    // console.log("ID", e.target.id, e.target.value)
    let new_status = e.target.value
    // Update the toggle value
    $.ajax({
     url: "/get_view_status",
     type: "get",
      data: {new_status: new_status},
      success: function(response) {
        let val = parseInt(response)
        $(".page-content #view-mode").html(view_mode_dict[val]);
        $(".navigation #view-mode").html(view_mode_dict[val])
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








// // Activate data summary
$(document).ready(function() {

  // Another function....
  $('#data-query-advanced-label').click(function(){
    let x = document.getElementById('data-query-advanced-content')

    let visible = x.style.display;

    // Toggle visibility
    if (visible === "none") {
      x.style.display = "block";
    }
    else {
      x.style.display = "none";
    }


    // console.log("visible",  visible);

   })

})






















//
