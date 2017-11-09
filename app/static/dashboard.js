$( document ).ready(function() {
  $("#add_category").click(function(event) {
      
      $.post($SCRIPT_ROOT + '/category/create', {
        category_name: $("#category_name").val(),
        language: $("#category_name").attr("lang"),
        category_intro: $("#category_intro").val(),
        category_careers: $("#category_careers").val()
      }, function(data) {
        alert(data.result);
      });
      return false;

  });

  function ajax_fn(url, data_attr) {
    return function(event) {
      $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + url,
        context: event.target,
        data: {category_id: $(this).attr(data_attr)},
        success: function(data) {
          if (data.result)
          {
            $(this).parent().remove();
          }
          return false;
        }
      });
    }
  }

  $(".approve-category").click(ajax_fn('/category/pending/approve', "approveid"));
  $(".reject-category").click(ajax_fn('/category/pending/reject', "rejectid"));

});
