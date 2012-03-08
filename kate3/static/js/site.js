function create_mobile_nav() {
    var mobileNav = $('div.mobile-nav-box').after('<fieldset class="mobile-nav"></fieldset>').next().append('<select></select>')
    mobileNav.children('select').append('<option value="">TICK Navigation&hellip;</option>');
    $('ul.sub-nav a').each(function(idx, link) {
        mobileNav.children('select').append('<option value="'+link.href+'">&raquo; '+link.text+'</option>');
    });
    mobileNav.children('select').bind('change', function(event) {
        if (event.target.value) { window.location.href = event.target.value; }
    });
}

$(document).ready(function() {
  create_mobile_nav();
  $("a[rel=popover]")
    .popover()
    .click(function(e) {
      e.preventDefault()
    });

  $("#upload_link").click(function(e) {
    $('#id_url').val('');
  });

  $("#standards_select").hide();
  $("select#id_content_areas[multiple=multiple]").change(function() {
    $("#standards_select").show();
    $("select#id_content_standards").attr('disabled', true);
    $.get("/tick/core_content_ajax/", {content_area: String($(this).val()).split(',').join('_')},
        function(data){
          selected_content_standard = String($('select#id_content_standards').val()).split(',')

          $("select#id_content_standards").html(data);
          $("select#id_content_standards option").attr('selected', false);
            
          for (i=0; i<selected_content_standard.length; i++) {
            $('select#id_content_standards option[value="'+ selected_content_standard[i] +'"]').attr('selected', 'true')
          }
            
          $("select#id_content_standards").attr('disabled', false);
    }, "html");

    $.get("/tick/common_core_ajax/", {content_area: String($(this).val()).split(',').join('_')},
      function(data){
        selected_common_core = String($('select#id_common_core_standards').val()).split(',')
                
        $("select#id_common_core_standards").html(data);
        $("select#id_common_core_standards option").attr('selected', false);
                
        for (i=0; i<selected_common_core.length; i++) {
          $('select#id_common_core_standards option[value="'+ selected_common_core[i] +'"]').attr('selected', 'true')
        }
                
        $("select#id_common_core_standards").attr('disabled', false);
    }, "html");

  });
});