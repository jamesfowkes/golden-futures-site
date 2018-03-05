$( document ).ready(function() {
  $("#add_category").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_add_category").ajaxSubmit({
          url:$SCRIPT_ROOT + $data["api_endpoints"]["add_category"],
          success: function(data) {
            $("#category_name").val("");
            $("#category_intro").val("");
            $("#category_careers").val("");

            if (data.success) {
              flash = $("<p class='success'></p>").text(data.category_name + " " + $L["add_success"])
            } else {
              flash = $("<p class='fail'></p>").text(data.err)
            }
            flash.insertBefore($("button#add_category"))
          }
        });
      return false;
  });
});
