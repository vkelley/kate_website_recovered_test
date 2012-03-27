$ = django.jQuery;

copy_link_link = function() {
    $('<a href="#">Copy Link</a>')
        .attr('style', 'margin: 8px 0 0; float: right;')
        .addClass('copy_link')
        .appendTo('div.store_link > div');
}

$(document).ready(function(){
    //copy_name_link();
    //copy_cost_link();
    copy_link_link();
});