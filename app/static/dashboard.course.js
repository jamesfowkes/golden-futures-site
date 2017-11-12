$( document ).ready(function() {
  $("#add_course").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $.post($SCRIPT_ROOT + '/course/create', {
        course_name: $("#course_name").val(),
        language: $pagelang,
      }, function(data) {
        $("#course_name").val("");
        if (data.success) {
          flash = $("<p class='success'></p>").text(data.data.course_name + " " + $L["add_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#add_course"))
      });
      return false;
  });
});
