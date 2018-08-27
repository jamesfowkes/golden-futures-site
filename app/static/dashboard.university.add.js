$( document ).ready(function() {
  $("#add_university").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_addedit_university").ajaxSubmit({
          url:$SCRIPT_ROOT + $data["api_endpoints"]["add_university"],
          success: function(data) {
            $("#form_addedit_university").find(".form-control").val("");

            if (data.success) {
              flash = $("<p class='success'></p>").text(data.university_name + " " + $L["add_success"])
            } else {
              flash = $("<p class='fail'></p>").text(data.err)
            }
            flash.insertBefore($("button#add_university"))
          },
          error: function(data ) { alert(data); },
        });
      return false;
  });
});
