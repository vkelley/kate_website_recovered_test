$ = django.jQuery;

set_tech_standards = function(){
    $('#tech_standard_list').html("");
    standards_select = $('select#id_tech_standards');

    $.get("/api/v1/tech_standard/set/"+standards_select.val().join(";")+"/", {},
        function(data){
            
            $('<table/>')
                .attr('id', 'tech_standards_table')
                .attr('style', 'border: 1px solid #eee; border-width: 1px 1px 0 1px;')
                .appendTo('#tech_standard_list');

            $.each(data.objects, function(index, object) {
                $('#tech_standards_table')
                    .append("<tr><td nowrap='true'><strong>"+object.name+"</strong></td><td>"+object.description+"</td></tr>")
            });
        });
}

tech_standards = function(){
    $('<div/>')
        .attr("id", "tech_standard_list")
        .appendTo('.tech_standards');

    set_tech_standards();

    $('select#id_tech_standards').change(function() {
        set_tech_standards();
    });
};

$(document).ready(function(){
    tech_standards();
});