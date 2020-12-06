
// // Activate the toggle switch
$(document).ready(function() {


   // $('#update-erd-broadway').click(function(e) {

    // Simplified things
    // console.log("ID", e.target.id, e.target.value)
    //let new_status = e.target.value
    // Update the toggle value
    $.ajax({
     url: "generate-erd/broadway",
     type: "get",
      data: {generate: false},
      success: function(response) {
        let path = encodeURIComponent(response)
        $("#erd-broadway").attr({'src':path}).css({"display": "inline"});
      },
      error: function(xhr) {
       //Do Something to handle error
       console.log("error")
      }
    });

    // })
  })
