$ = django.jQuery;

$(document).ready(function() {
    standards_select = $('select#id_tech_standards');

    $.get("/api/v1/tech_standard/", {'id[]': standards_select.val()},
        function(data) {
            $.each(data.objects, function(index, object) {
                console.log(object.category);
            });
        });


});