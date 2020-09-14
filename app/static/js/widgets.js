
$(document).ready(function() {

    // on page load, set the text of the label based the value of the range
    let x = document.getElementById('detail-level-slider')
    if(x){
      document.getElementById('detail-level-text').innerHTML = x.value;
    }


    // setup an event handler to set the text when the range value is dragged (see event for input) or changed (see event for change)
    $('#detail-level-slider').on('input change', function () {
        $('#detail-level-text').text(this.value);
    });

});
