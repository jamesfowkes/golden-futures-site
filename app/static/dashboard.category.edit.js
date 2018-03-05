$( document ).ready(function() {
  $("#edit_category").click(function(event) {
    $("#form_edit_category").ajaxSubmit({
      url:$SCRIPT_ROOT + $data["api_endpoints"]["edit_category"],
      success: function(data) {
        if (data.success) {
          flash = $("<p class='success'></p>").text(data.category_name + " " + $L["edit_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#add_category"))
      }
    });
  });

  $("#edit_category_courses").click(function(event) {
      course_ids = $("form#form_edit_category_courses input:checkbox:checked").map(function(){
        return $(this).val();
      }).get();
      
    $("#form_edit_category_courses").ajaxSubmit({
      url:$SCRIPT_ROOT + $data["api_endpoints"]["edit_category_courses"],
      success: function(data) {
        if (data.success) {
          flash = $("<p class='success'></p>").text(data.category_name + " " + $L["edit_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#add_category"))
      }
    });
  });
});

/* $( document ).ready(function() {
  
});
*/