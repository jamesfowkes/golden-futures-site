function show_or_hide_approval_divs()
{
  if ($("div#additions > div.pending").length == 0)
  {
    $("div#additions").hide();
  }
  else
  {
    $("div#additions").show();
  }

  if ($("div#edits > div.pending").length == 0)
  {
    $("div#edits").hide();
  }
  else
  {
    $("div#edits").show();
  }

if ($("div#deletions > div.pending").length == 0)
  {
    $("div#deletions").hide();
  }
  else
  {
    $("div#deletions").show();
  }
}

$( document ).ready(function() {
  $("#add_category").click(function(event) {
      
      $.post($SCRIPT_ROOT + '/category/create', {
        category_name: $("#category_name").val(),
        language: $("#category_name").attr("lang"),
        category_intro: $("#category_intro").val(),
        category_careers: $("#category_careers").val()
      }, function(data) {
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
            show_or_hide_approval_divs();
          }
          return false;
        }
      });
    }
  }

  $(".approve-category").click(ajax_fn('/category/pending/approve', "approveid"));
  $(".reject-category").click(ajax_fn('/category/pending/reject', "rejectid"));

  show_or_hide_approval_divs();
});
