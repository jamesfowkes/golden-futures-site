$( document ).ready(function() {
  $("#course_edit_submit").click(function(event) {
      $.post($SCRIPT_ROOT + '/course/edit/' + $data["course_id"], {
        language: $pagelang,
        course_name: $("#course_name").val()
      }, function(data) {
        if (data.success) {
          window.location.replace(data.redirect)
        }
      });
      return false;
  });
});
