var category_filter = null;
var fee_filter = null;

function hide_all() {
	$(".university_card").hide();
	$(".category_span").hide();
}

function show_all() {
	$(".university_card").show();
	$(".category_span").show();
	$(".comma").show();
}

function filter_by_category(filter) {
  $(".university_card").each(function() {
    
    if (!$(this).attr("category_id").includes(filter)) {
      $(this).hide();
    }

    $(".category_span", this).each(function() {
      if (!$(this).attr("category_id").includes(filter)) {
        $(this).hide();
      }
    });

    $('.comma:visible:last', this).hide();
  });
}

function filter_by_fee(max_fee) {
  $(".university_card").each(function() {
    var this_min_fee = parseInt($(this).attr("min_fee"));
    if (this_min_fee >= max_fee) {
      $(this).hide();
    }
  });
}

function apply_filters() {
  show_all();

  if (category_filter != null) {
    filter_by_category(category_filter);
  }

  if (fee_filter != null) {
    filter_by_fee(fee_filter);
  }
}

$( document ).ready(function() {

    $(".category_filter_button").click(function(event) {
      category_filter = "category_".concat(event.target.id);
      apply_filters();
      $("#reset_all_filter_button").show();
    });

    $("#apply_fee_filter_button").click(function(event) {

      var max_fee = parseInt($("#fee_filter").val(), 10);
      if (isNaN(max_fee)) {
        return;
      }
      
      fee_filter = max_fee;

      apply_filters();

      $("#reset_all_filter_button").show();

    });

    $("#reset_all_filter_button").click(function(event) {
      show_all();
      fee_filter = null;
      category_filter = null;
      $(this).hide();
    });
});
