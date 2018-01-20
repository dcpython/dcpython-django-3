$(document).ready(function() {
    $('.dateinput').datepicker({ format: "yyyy-mm-dd", todayHighlight: "true"});
    $('.datetimeinput').datepicker({ format: "yyyy-mm-dd", todayHighlight: "true"});
    $('.totals').hide().before('<a href="#" id="toggle-totals" class="btn btn-default"><h4>Totals <i class="fa fa-caret-down"></i></h4></a>');
    $('a#toggle-totals').click(function() {
        $('.totals').slideToggle(250);
        return false;
    });
    $('.actives').hide().before('<a href="#" id="toggle-actives" class="btn btn-default"><h4>Active <i class="fa fa-caret-down"></i></h4></a>');
    $('a#toggle-actives').click(function() {
        $('.actives').slideToggle(250);
        return false;
    });
});
