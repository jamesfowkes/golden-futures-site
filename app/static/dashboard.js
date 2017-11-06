/*function add_new_career_input(name) {
  container = $(get_div("form-inline"));
  span = $("<span>");
  new_label = $(get_label(name));
  new_input = $(get_text_input(name, name));
  remove_button = $("<i class='fa fa-times delete-icon' aria-hidden='true'></i>");

  span.append(new_label);
  span.append(new_input);
  span.append(remove_button);
  
  container.append(span);

  $("#category_careers").append(container);

  return false;
}*/

$( document ).ready(function() {
  $("#add_category").click(function(event) {
      
      $.post($SCRIPT_ROOT + '/category/create', {
        category_name: $("#category_name").val(),
        language: $("#category_name").attr("lang"),
        category_intro: $("#category_intro").val(),
        category_careers: $("#category_careers").val()
      }, function(data) {
        alert(text(data.result));
      });
      return false;

    });

    /*var career_ids = [];
    var career_id = 0;
    $("#add_career").click(function(event) {
      name = 'input_career' + career_id;
      add_new_career_input(name);
      career_ids.push(name);
      career_id++;
    });

    $(".remove_career").click(function(event) {
      return false;
    });*/
});
