function countryStateInit(){
	$("#id_us_state").val($("#id_state").val());
	hideShowState();
	
	function hideShowState() {
		 var country = $("#id_country option:selected").val();
		 var state = $("#id_state");
		 var usState = $("#id_us_state");
		 if (country == "US")  { 
			 state.hide();
			 usState.show();
		 }
		 else {
			 state.show();
			 usState.hide();
		 }		
	}
	
	$("#id_country").change(function() {
		hideShowState();		 
	});
	
	$("#id_us_state").change(function(){
		var state = $("#id_us_state option:selected").val();
		$("#id_state").val(state);
	});	
	
}