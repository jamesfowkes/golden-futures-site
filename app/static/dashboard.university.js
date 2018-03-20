$( document ).ready(function() {
  $("#add_university").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_add_university").ajaxSubmit({
          url:$SCRIPT_ROOT + $data["api_endpoints"]["add_university"],
          success: function(data) {
            $("#university_name").val("");
            $("#university_intro").val("");

            if (data.success) {
              flash = $("<p class='success'></p>").text(data.university_name + " " + $L["add_success"])
            } else {
              flash = $("<p class='fail'></p>").text(data.err)
            }
            flash.insertBefore($("button#add_university"))
          }
        });
      return false;
  });
});
