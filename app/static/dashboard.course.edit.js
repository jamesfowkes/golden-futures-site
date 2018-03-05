$( document ).ready(function() {
  $("#edit_course").click(function(event) {
    $("p.success").remove();
    $("p.fail").remove();
    $("#form_edit_course").ajaxSubmit({
      url:$SCRIPT_ROOT + $data["api_endpoints"]["edit_course"],
      success: function(data) {
        if (data.success) {
          flash = $("<p class='success'></p>").text(data.data.course_name + " " + $L["edit_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#edit_course"))
      }
    });
    return false;
  });
});
