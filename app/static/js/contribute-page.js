// Toggle this for rich console printouts
var debug = false;

// sleep time expects milliseconds
function sleep (time) {
  return new Promise((resolve) => setTimeout(resolve, time));
};


// // Activate data summary
$(document).ready(function() {

  // Up here, can determine the column values / index position
  // Backlogging this though...

  $('table.dataframe').delegate('tr', 'click', function() {

      // Get values
      let myRow = this.children
      let rowId = parseInt(myRow[0].innerText)
      let rowDOB = myRow[2].innerText
      let rowGenderIdentity = myRow[3].innerText
      let rowRacialIdentity = myRow[4].innerText

      // For testing
      if(debug==true){
        console.log(
          "id: "+ rowId + "; " +
          "DOB: " + rowDOB + "; " +
          "Gender Identity: " + rowGenderIdentity + "; " +
          "Racial Identity: " + rowRacialIdentity + ";"
        );
      }


      // Set values
      $('input[name=person_id]').val(rowId);
      $('input[name=date_of_birth]').val(rowDOB);
      $('input[name=racial_identity]').val(rowRacialIdentity);
      $('input[name=gender_identity]').val(rowGenderIdentity);

    });

    // Indeed you can do 2 functions in one "on document ready"
    $('form').submit( function() {


        // I'd love to have this delayed before pushing
        // Might need to submit the form with ajax to make this happen...
        // Now clear
        $('input[name=edit_comment]').val('');
        $('input[name=edit_citation]').val('');

  });

})
