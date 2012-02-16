function create_mobile_nav() {
    var mobileNav = $('ul.sub-nav').parent('div').after('<fieldset class="mobile-nav"></fieldset>').next().append('<select></select>')
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
      })
});