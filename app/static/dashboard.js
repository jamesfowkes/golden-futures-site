$( document ).ready(function() {
  function pending_changes_ajax_handler(url, data_attr) {
    return function(event) {
      parent_div = $(this).parent().parent()
      $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + url,
        context: event.target,
        data: {data_id: $(this).attr(data_attr)},
        success: function(data) {
          if (data.success)
          {
            $(this).parent().remove();
            if (data.remaining_count == 0) {
              heading = parent_div.find("h4.pending_heading")
              heading.text($L[heading.attr("i18n_key")])
            }
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

  $(".approve-university").click(pending_changes_ajax_handler('/university/pending/approve', 'approveid'));
  $(".reject-university").click(pending_changes_ajax_handler('/university/pending/reject', 'rejectid'));

});
