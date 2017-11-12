function show_hide_approval_divs() {
  var has_additions = $("div#additions > div.pending").length > 0;
  var has_edits = $("div#edits > div.pending").length > 0;
  var has_deletions = $("div#deletions > div.pending").length > 0;

  if (has_additions) {
    $("div#additions").show();
  } else {
    $("div#additions").hide();
  }

  if (has_edits) {
    $("div#edits").show();
  } else {
    $("div#edits").hide();
  }

  if (has_deletions) {
    $("div#deletions").show();
  } else {
    $("div#deletions").hide();
  }

  if (has_additions || has_edits || has_deletions) {
    $("div#pending_changes").show();
  } else {
    $("div#pending_changes").hide();
  }
}

$( document ).ready(function() {
  function pending_changes_ajax_handler(url, data_attr) {
    return function(event) {
      $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + url,
        context: event.target,
        data: {data_id: $(this).attr(data_attr)},
        success: function(data) {
          if (data.result)
          {
            $(this).parent().remove();
            show_hide_approval_divs();
          }
          return false;
        }
      });
    }
  }

  $(".approve-category").click(pending_changes_ajax_handler('/category/pending/approve', 'approveid'));
  $(".reject-category").click(pending_changes_ajax_handler('/category/pending/reject', 'rejectid'));

  $(".approve-course").click(pending_changes_ajax_handler('/course/pending/approve', 'approveid'));
  $(".reject-course").click(pending_changes_ajax_handler('/course/pending/reject', 'rejectid'));

  show_hide_approval_divs();
});
