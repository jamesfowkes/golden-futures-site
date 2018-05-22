$( document ).ready(function() {
  function pending_changes_ajax_handler(post_url, redirect_url, data_attr) {
    return function(event) {
      parent_div = $(this).parent().parent()
      $.ajax({
        type: "POST",
        url: $SCRIPT_ROOT + post_url,
        context: event.target,
        data: {data_id: $(this).attr(data_attr)},
        success: function(data) {
          if (data.success)
          {
            window.location.replace(redirect_url)
          }
          return false;
        }
      });
    }
  }

  $(".approve-university").click(
    pending_changes_ajax_handler('/university/pending/approve', $data["approve_reject_redirect"], 'approveid')
  );
  
  $(".reject-university").click(
    pending_changes_ajax_handler('/university/pending/reject',$data["approve_reject_redirect"], 'rejectid')
  );

});
