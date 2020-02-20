$(document).ready(function(){
	$("#convertTo").change(function(){
		var convertTo = $("#convertTo").val();
		if (convertTo == "png"){
			$("#convertForm").append("<div id='json2pngOptions'>Hey</div>")
		}
});
