// Toggle this for rich console printouts
var debug = true;



// This is loaded once the document is ready
$(document).ready(function() {

  // Every time you click a row...
  $('table.dataframe').delegate('tr', 'click', function() {


      // Get values
      let myRow = this.children
      let rowId = parseInt(myRow[0].innerText)
      let userId = parseInt(myRow[1].innerText)
      let rowEmail = myRow[2].innerText
      let rowStatus = parseInt(myRow[4].innerText)

      // For testing
      if(debug==true){
        console.log(
          "row id: "+ rowId + "; " +
          "user id: "+ userId + "; " +
          "email: " + rowEmail + "; " +
          "approval status: " + rowStatus + "; "
        );
      }
  
  
      // Set values
      $('input[id=allFields-userEmail]').val(rowEmail);
      // if user is approved:
        if (rowStatus == 1){
          $('input[id=allFields-un_approve]').prop("checked", true);
          $('input[id=allFields-approve]').prop("checked", false);
        } 
        else {
          $('input[id=allFields-un_approve]').prop("checked", false);
          $('input[id=allFields-approve]').prop("checked", true);
        }
  //     $('input[name=date_of_birth]').val(rowDOB);
  //     $('input[name=racial_identity]').val(rowRacialIdentity);
  //     $('input[name=gender_identity]').val(rowGenderIdentity);
  //
  //     // Clear these too...
  //     $('input[name=edit_comment]').val('');
  //     $('input[name=edit_citation]').val('');
  //
  //   });
  //
  //   // Indeed you can do 2 functions in one "on document ready"
  //
  //   // On submit, I'd like this thing to clear.....
  //   $('form').submit( function() {
  //
  //     // Do something here if you want...
  //
  // });

});

})
