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
    
    if (!$(this).attr("category_id").includes(filter["id"])) {
      $(this).hide();
    }

    $(".category_span", this).each(function() {
      if (!$(this).attr("category_id").includes(filter["id"])) {
        $(this).hide();
      }
    });

    $('.comma:visible:last', this).hide();
  });
}

function filter_by_fee(max_fee) {
  $(".university_card").each(function() {
    var this_min_fee = parseInt($(this).attr("min_fee"));
    if (this_min_fee > max_fee) {
      $(this).hide();
    }
  });
}

function apply_filters(filters) {
  show_all();

  applied_filters = []
  Object.keys(filters).forEach(function(k) {
    if (filters[k]["data"] != null) {
      filters[k]["fn"](filters[k]["data"]);
      applied_filters.push(filters[k]["text"](filters[k]["data"]));
    }
  });

  return applied_filters;
}

function clear_filter_data(filters) {
  Object.keys(filters).forEach(function(k) {
    filters[k]["data"] = null;
  });
}

function display_applied_filters(text) {
  $("div#applied_filters").html("");
  $("div#applied_filters").append("<h4>" + $L["applied_filters"] + "</h4>");
  list = $("<ul></ul>")
  var l = text.length;
  for (var i = 0; i < l; i++) {
    list.append("<li>" + text[i] + "</li>");
  }
  $("div#applied_filters").append(list);
}

var filters = {
  "category": {
    "fn":filter_by_category,
    "text": function(cat) {return $L["category_filter_display_text"] + ": " + cat["name"];},
    "data":null
  },
  "fee": {
    "fn":filter_by_fee,
    "text": function(fee) {return $L["fee_filter_display_text"] + ": " + $L["currency"] + fee;},
    "data":null
  }
};

$( document ).ready(function() {

    $(".category_filter_button").click(function(event) {
      filters["category"].data = {
        "id": "category_".concat(event.target.id),
        "name": event.target.text
      };

      applied_filters = apply_filters(filters);
      display_applied_filters(applied_filters);
      $("#reset_all_filter_button").show();
    });

    $("#apply_fee_filter_button").click(function(event) {

      var max_fee = parseInt($("#fee_filter").val(), 10);
      if (isNaN(max_fee)) {
        return;
      }
      
      filters["fee"].data = max_fee;

      applied_filters = apply_filters(filters);
      display_applied_filters(applied_filters);
      $("#reset_all_filter_button").show();
    });

    $("#reset_all_filter_button").click(function(event) {
      show_all();
      clear_filter_data(filters);
      $("div#applied_filters").html("");
      $(this).hide();
    });
});
