$ = django.jQuery;

add_link_to = function(to, object) {
    to
        .append('<br>')
        .append(object);
}

copy_name_link = function() {
    copy_name = $('<a href="#">Copy Name</a>')
        .addClass('copy_name');

    add_link_to($('div.store_name label'), copy_name);

    copy_name.click(function(e) {
        new_value = $('#id_store_name').val();
        $('#id_name').val(new_value);
        e.preventDefault();
    });
}

copy_cost_link = function() {
    copy_cost = $('<a href="#">Copy Cost</a>')
        .addClass('copy_cost');

    add_link_to($('div.store_cost label'), copy_cost);

    copy_cost.click(function(e) {
        new_value = $('#id_store_cost').val();
        $('#id_cost').val(new_value);
        e.preventDefault();
    });
}

copy_link_link = function() {
    copy_link = $('<a href="#">Copy Link</a>')
        .addClass('copy_link');

    add_link_to($('div.store_link label'), copy_link);

    copy_link.click(function(e) {
        new_value = $('#id_store_link').val();
        $('#id_link').val(new_value);
        e.preventDefault();
    });
}

$(document).ready(function(){
    copy_name_link();
    copy_cost_link();
    copy_link_link();
});