var json2pngOptions = '<input class="form-control" name="size" placeholder="Image Size In Pixels (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="outputType" placeholder="Output Type (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="resolution" placeholder="Image Resolution in Dots Per Inch (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="limit" placeholder="Voltage Range Limit in Percent (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="withNodes" placeholder="Label Branching Nodes (OPTIONAL)">';

$(document).ready(function(){
	$("#convertTo").change(function(){
		var convertTo = $("#convertTo").val();
		if (convertTo == "png"){
			$("#json2png").html(json2pngOptions);
		}
		else {
			$("#json2png").html("");
		}
	});
});
