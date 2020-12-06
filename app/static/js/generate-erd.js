
// // Activate the toggle switch
$(document).ready(function() {


  // On page load
  $.ajax({
   url: "generate-erd/broadway",
   type: "get",
    data: {generate: false},
    success: function(response) {
      let path = encodeURIComponent(response)

      $("#erd-broadway").attr({'src':response}).css({"display": "block"});
    },
    error: function(xhr) {
     //Do Something to handle error
     console.log("error")
    }
  });



   $('#update-erd-broadway').click(function(e) {
    $.ajax({
     url: "generate-erd/broadway",
     type: "get",
      data: {generate: true},
      success: function(response) {
        let path = encodeURIComponent(response)

        $("#erd-broadway").attr({'src':response}).css({"display": "block"});
      },
      error: function(xhr) {
       //Do Something to handle error
       console.log("error")
      }
    });

    })
  })
