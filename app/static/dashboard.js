$( document ).ready(function() {

    $("#add_category").click(function(event) {
      
      $.postJSON($SCRIPT_ROOT + '/category/create', {
        category_name: $("#category_name").val(),
        language: $("#category_name").attr("lang")
      }, function(data) {
        alert(text(data.result));
      });
      return false;

    });

    var career_ids = [];
    var career_id = 0;
    $("#add_career").click(function(event) {
      name = 'input_career' + career_id;
      new_label = $(get_label(name));
      new_input = $(get_text_input(name, name));
      remove_button = $("<span class='glyphicon glyphicon-remove'></span>");
      career_ids.push(name);
      career_id++;
      $("#category_careers").append(new_label);
      $("#category_careers").append(new_input);
      $("#category_careers").append(remove_button);
      return false;
    });

    $(".remove_career").click(function(event) {
      return false;
    });
});
