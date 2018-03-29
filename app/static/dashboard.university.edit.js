var id_counters = {
  "contact_details": 0,
  "facilities": 0,
  "tuition_fees": 0,
  "scholarships": 0
}

function i18n_deleter_fn(event) {
    to_delete = $(this).attr("target");
    $(to_delete).remove();
}

function get_i18n_deleter(class_name, index) {
  deleter = $("<i>")
  deleter.attr("target", "#" + class_name + index)
  deleter.attr("aria-hidden", "true")
  deleter.addClass("fa fa-remove fa-2x pull-right i18n_deleter")
  deleter.click(i18n_deleter_fn)

  return deleter
}

function get_i18n_divs(size="col-sm-6") {
  lcolumn_div = $("<div>").addClass(size)
  linput_div = $("<div>")
  rcolumn_div = $("<div>").addClass(size)
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

function form_array(name="") {
  return "[" + name + "]";
}

function get_indexed_input(class_name, index, type="text") {
  input = $("<input>")
  input.addClass("form-control")
  input.attr("type",type)
  input.attr("id",class_name + form_array(index))
  input.attr("name", class_name + form_array())

  return input
}

function get_indexed_i18n_input(class_name, language_id, index, type="text") {
  input = get_indexed_input(class_name, index, type)
  input.attr("id",class_name + form_array(language_id) + form_array(index))
  input.attr("name",class_name + form_array(language_id) + form_array())
  return input
}

function get_indexed_div(class_name, index) {
  div = $("<div>")
  div.addClass("university_detail")
  div.addClass(class_name)
  div.attr("id", class_name + index)

  return div
}

function add_i18n_edits(parent, class_name, index, languages) {

  top_level_div = get_indexed_div(class_name, index)

  row = $("<div>").addClass("row")

  divs = get_i18n_divs()

  left_input = get_indexed_i18n_input(class_name, languages[0][0], index)
  right_input = get_indexed_i18n_input(class_name, languages[1][0], index)

  deleter = get_i18n_deleter(class_name, index)

  divs.linput.append(left_input)
  divs.rinput.append(right_input)
  divs.rinput.append(deleter)

  row.append(divs.lcol)
  row.append(divs.rcol)

  top_level_div.append(row)
  
  parent.append(top_level_div)

  return top_level_div
}

function get_label(text, name, index="") {
  label = $("<label>" + text + "</label>")
  label.attr("for", name + index)
  return label  
}

function get_currency_input(label_text, name, index) {
  currency_div = $("<div>")
  currency_div.addClass("col-sm-2")

  currency_label = get_label(label_text, name, index)
  currency_input_group = $("<div>")
  currency_input_group.addClass("input-group")

  currency_addon_group = $("<div>")
  currency_addon_group.addClass("input-group-addon")

  currency_addon = $("<div>$</div>")
  currency_addon.addClass("input-group-text")

  currency_input = get_indexed_input(name, index, type="number")
  currency_addon_group.append(currency_addon)
  currency_input_group.append(currency_addon_group)
  currency_input_group.append(currency_input)

  currency_div.append(currency_label)
  currency_div.append(currency_input_group)

  return currency_div
}

function get_hidden_input(attributes) {
  input = $("<input>")
  input.attr("type", "hidden")
  for (var attr_name in attributes) {
    input.attr(attr_name, attributes[attr_name])
  }
  return input
}

function add_tuition_fee_inputs(parent, index, languages) {
  top_level_div = get_indexed_div("university_tuition_fee", index);
  top_row = $("<div>").addClass("row")
  bottom_row = $("<div>").addClass("row")
  minimum_fee_div = get_currency_input("Minimum", "university_tuition_fee_min", index)
  maximum_fee_div = get_currency_input("Maximum", "university_tuition_fee_max", index)

  award_divs = get_i18n_divs("col-sm-4")
  left_label = get_label("Award (" + languages[0][1] + ")")
  left_input = get_indexed_i18n_input("university_tuition_fee_award", languages[0][0], index)
  right_label = get_label("Award (" + languages[1][1] + ")")
  right_input = get_indexed_i18n_input("university_tuition_fee_award", languages[1][0], index)

  deleter = get_i18n_deleter("university_tuition_fee", index)

  award_divs.lcol.prepend(left_label)
  award_divs.linput.append(left_input)
  award_divs.rcol.prepend(right_label)
  award_divs.rinput.append(right_input)
  award_divs.rinput.append(deleter)

  top_row.append(minimum_fee_div)
  top_row.append(maximum_fee_div)
  top_row.append(award_divs.lcol)
  top_row.append(award_divs.rcol)

  include_chk_id = "university_tuition_fee_include_in_filter"+ form_array(index)
  include_chk_label = get_label($L["include_in_filter"], include_chk_id)
  include_checkbox = $("<input>").attr("type", "checkbox")
  include_checkbox.attr("name", "university_tuition_fee_include_in_filter[]")
  include_checkbox.attr("id", include_chk_id)
  include_checkbox.attr("value", index)
  include_checkbox.attr("checked")

  include_column = $("<div>").addClass("col-sm-12")

  include_column.append(include_chk_label)
  include_column.append(include_checkbox)
  bottom_row.append(include_column)

  hidden_period_inputs = [
    get_hidden_input({
      "name": "university_tuition_fee_period" + form_array(languages[0][0]),
      "value": "year"
    }),
    get_hidden_input({
      "name": "university_tuition_fee_period" + form_array(languages[1][0]),
      "value": "!year!"
    })
  ]

  hidden_index_input = get_hidden_input({
    "name": "university_tuition_fee_index[]",
    "value": index
  })

  top_level_div.append(hidden_period_inputs[0])
  top_level_div.append(hidden_period_inputs[1])
  top_level_div.append(hidden_index_input)

  top_level_div.append(top_row)
  top_level_div.append(bottom_row)

  parent.append(top_level_div);
}

$( document ).ready(function() {
  $("#edit_university").click(function(event) {
      $("p.success").remove();
      $("p.fail").remove();
      $("#form_edit_university").ajaxSubmit({
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

  $("#add_new_facility").click(function(event) {
    add_i18n_edits($("div#facilities_container"), "university_facility", id_counters["facilities"]+1, $data["languages"]);
    id_counters["facilities"]++;
  });

  $("#add_new_tuition_fee").click(function(event) {
    add_tuition_fee_inputs($("div#tuition_fees_container"), id_counters["tuition_fees"]+1, $data["languages"])
    id_counters["tuition_fees"]++;
  });

  $("#add_new_scholarship").click(function(event) {
    add_i18n_edits($("div#scholarships_container"), "university_scholarship", id_counters["scholarships"]+1, $data["languages"]);
    id_counters["scholarships"]++;
  });

  id_counters["contact_details"] = $("div.university_contact_detail").length-1
  id_counters["facilities"] = $("div.university_facility").length-1
  id_counters["tuition_fees"] = $("div.university_tuition_fee").length-1
  id_counters["scholarships"] = $("div.university_scholarship").length-1
});
