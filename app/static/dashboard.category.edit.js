$( document ).ready(function() {
  $("#category_edit_submit").click(function(event) {
      course_ids = $("form#form_add_category input:checkbox:checked").map(function(){
        return $(this).val();
      }).get();
      $.post($SCRIPT_ROOT + '/category/edit/' + $data["category_id"], {
        language: $pagelang,
        category_name: $("#category_name").val(),
        category_intro: $("#category_intro").val(),
        category_careers: $("#category_careers").val(),
        category_courses: course_ids
      }, function(data) {
        if (data.success) {
          window.location.replace(data.redirect)
        }
      });
      return false;
  });
});
