function hide_all()
{
	$(".university_card").hide();
	$(".category_span").hide();
}

function show_all()
{
	$(".university_card").show();
	$(".category_span").show();
	$(".comma").show();
}

$( document ).ready(function() {
    $(".category_filter_button").click(function(event){
    	hide_all();
    	category_to_show = ".category_".concat(event.target.id);
    	$(category_to_show).show();

    	$(".university_card").each(function() {
   			$('.comma:visible:last', this).hide();
		});
    });

   	$("#reset_filter_button").click(function(event){
   		show_all();
   	});

});
