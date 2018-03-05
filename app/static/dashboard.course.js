$( document ).ready(function() {
  $("#add_course").click(function(event) {
    $("p.success").remove();
    $("p.fail").remove();
    $("#form_add_course").ajaxSubmit({
      url:$SCRIPT_ROOT + $data["api_endpoints"]["add_course"],
      success: function(data) {
        if (data.success) {
          flash = $("<p class='success'></p>").text(data.data.course_name + " " + $L["add_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#add_course"))
      }
    });
    return false;
  });
});
