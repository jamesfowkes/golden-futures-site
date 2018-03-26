var id_counters = {
  "contact_details": 0
}

function i18n_deleter_fn(event) {
    to_delete = $(this).attr("target");
    $(to_delete).remove();
}

function get_i18n_divs() {
  lcolumn_div = $("<div>").addClass("col-sm-6")
  linput_div = $("<div>").addClass("input-group")
  rcolumn_div = $("<div>").addClass("col-sm-6")
  rinput_div = $("<div>").addClass("input-group")

  lcolumn_div.append(linput_div)
  rcolumn_div.append(rinput_div)

  return {
    lcol: lcolumn_div,
    linput: linput_div,
    rcol: rcolumn_div,
    rinput: rinput_div
  }
}

function get_i18n_input(class_name, language_id, index) {
  input = $("<input>")
  input.addClass("form-control")
  input.attr("type","text")
  input.attr("id",class_name + "." + language_id + "." + index)
  input.attr("name", class_name + "." + language_id + "[]")

  return input
}

function add_i18n_edits(parent, class_name, index, languages) {
  parent_div = $("<div>")
  parent_div.addClass("row")
  parent_div.addClass(class_name)
  parent_div.attr("id", class_name + index)

  divs = get_i18n_divs()

  left_input = get_i18n_input(class_name, languages[0][0], index)
  right_input = get_i18n_input(class_name, languages[1][0], index)

  deleter = $("<i>")
  deleter.attr("target", "#" + class_name + index)
  deleter.attr("aria-hidden", "true")
  deleter.addClass("fa fa-remove fa-2x pull-right i18n_deleter")
  deleter.click(i18n_deleter_fn)

  divs.linput.append(left_input)
  divs.rinput.append(right_input)
  divs.rinput.append(deleter)

  parent_div.append(divs.lcol)
  parent_div.append(divs.rcol)

  parent.append(parent_div)
}


$( document ).ready(function() {
  $("#edit_university").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_add_university").ajaxSubmit({
          url:$SCRIPT_ROOT + $data["api_endpoints"]["edit_university"],
          success: function(data) {
            $("#university_name").val("");
            $("#university_intro").val("");

            if (data.success) {
              flash = $("<p class='success'></p>").text(data.university_name + " " + $L["add_success"])
            } else {
              flash = $("<p class='fail'></p>").text(data.err)
            }
            flash.insertBefore($("button#edit_university"))
          }
        });
      return false;
  });

  $(".i18n_deleter").click(i18n_deleter_fn)

  $("#add_new_contact_details").click(function(event) {
    add_i18n_edits($("div#contact_details_container"), "university_contact_detail", id_counters["contact_details"]+1, $data["languages"]);
    id_counters["contact_details"]++;
  });

  id_counters["contact_details"] = $("div.contact_details").length-1
});
