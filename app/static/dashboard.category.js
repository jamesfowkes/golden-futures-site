$( document ).ready(function() {
  $("#add_category").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $.post($SCRIPT_ROOT + '/category/create', {
        category_name: $("#category_name").val(),
        language: $pagelang,
        category_intro: $("#category_intro").val(),
        category_careers: $("#category_careers").val()
      }, function(data) {
        $("#category_name").val("");
        $("#category_intro").val("");
        $("#category_careers").val("");

        if (data.success) {
          flash = $("<p class='success'></p>").text(data.category_name + " " + $L["add_success"])
        } else {
          flash = $("<p class='fail'></p>").text(data.err)
        }
        flash.insertBefore($("button#add_category"))
      });
      return false;
  });
});
