$(function() {
	var item_language = "{{ request.GET.language }}";
	var item_usertype = "{{ request.GET.usertype }}";
	if(item_language !=='' || item_language!==null){
		$("#item_language option[value='" + item_language + "']").attr("selected","selected");
    }
	if(item_usertype !=='' || item_usertype!==null){
		$("#item_usertype option[value='" + item_usertype + "']").attr("selected","selected") ;
	}
	$("a[id^=unlike_]").hide();

});

function showSelected() {
	var item_language = $("#item_language option:selected").val();
	var item_usertype = $("#item_usertype option:selected").val();
	window.location = "{% url 'home' %}"+'?language='+item_language+'&usertype='+item_usertype
}


function reblog(id){
	$.ajax({
			 type: "POST",
			 data: { 'csrfmiddlewaretoken': '{{ csrf_token }}'},
			 dataType: "json",
			 url: $('#reblog_'+id).attr("href"),
			 success: function(response) {
				 $('#reblog_count_'+id).html(response.reblog_count);
			  }
		});
	return false
};

function like(id){
	$.ajax({
			 type: "POST",
			 data: { 'csrfmiddlewaretoken': '{{ csrf_token }}'},
			 dataType: "json",
			 url: $('#like_'+id).attr("href"),
			 success: function(response) {
				 $('#unlike_count_'+id).html(response.likes_count);
				 $('#like_'+id).hide();
				 $('#unlike_'+id).show();
			  }
		});
	return false
};

function unlike(id){
	$.ajax({
			 type: "POST",
			 data: { 'csrfmiddlewaretoken': '{{ csrf_token }}'},
			 dataType: "json",
			 url: $('#unlike_'+id).attr("href"),
			 success: function(response) {
				 $('#like_count_'+id).html(response.likes_count);
				 $('#like_'+id).show();
				 $('#unlike_'+id).hide();
			  }
		});
	return false
};
