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

function approve_button(approve_id, class_type, button_text)
{
  return $('<button type="button" approveid="' + approve_id + '" class="approve-' + class_type + ' btn btn-outline-success btn-sm">' + button_text + '</button>')
}

function reject_button(reject_id, class_type, button_text)
{
  return $('<button type="button" approveid="' + reject_id + '" class="reject-' + class_type + ' btn btn-outline-danger btn-sm">' + button_text + '</button>')
}

function add_approval_div(container_id, entries, pending_id, class_type, approve_text, reject_text)
{
  container_div = $("div#" + container_id);
  new_div = $('<div class="pending">');

  new_approve_button = approve_button(pending_id, class_type, approve_text);
  new_reject_button = reject_button(pending_id, class_type, reject_text);

  for (var i = 0, len = entries.length; i < len; i++) {
    new_p = $("<p></p>").text(entries[i]);
    new_div.append(new_p)
  }
  new_div.append(new_approve_button)
  new_approve_button.after(" ");
  new_div.append(new_reject_button)
  container_div.append(new_div)
}

function refresh_approval_divs() {
  if ($("div#pending_changes").length) {
    show_hide_approval_divs();
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
        add_approval_div("additions", data["entries"], data["pending_id"], "category", data["approve_text"], data["reject_text"]);
        refresh_approval_divs();
      });
      return false;
  });

  function pending_changes_ajax_handler(url, data_attr) {
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
            refresh_approval_divs();
          }
          return false;
        }
      });
    }
  }

  $('body').on('click', '.approve-category', pending_changes_ajax_handler('/category/pending/approve', "approveid"));
  $(".reject-category").click(pending_changes_ajax_handler('/category/pending/reject', "rejectid"));

  refresh_approval_divs();
});
