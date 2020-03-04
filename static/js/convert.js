var json2pngOptions = '<input class="form-control" name="size" placeholder="Image Size In Pixels (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="output_type" placeholder="Output Type (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="resolution" placeholder="Image Resolution in Dots Per Inch (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="limit" placeholder="Voltage Range Limit in Percent (OPTIONAL)">';
json2pngOptions += '<input class="form-control" name="with_nodes" placeholder="Label Branching Nodes (OPTIONAL)">';

var script = document.currentScript;
var fullUrl = script.src;
var jsonUrl = fullUrl.replace("convert.js", "data.json") // hard coded jsonUrl


$(document).ready(function(){
	$.getJSON(jsonUrl, function(data) {
		fromToConversion = JSON.parse(data)
		var convertTo = $("#convert-to").val();
		var convertFrom = $("#convert-from").val();
		$("#convert-to, #convert-from").change(function(){
			convertTo = $("#convert-to").val();
			convertFrom = $("#convert-from").val();
			conversionOptions = Object.keys(fromToConversion[convertFrom][convertTo]["defaults"])
			var optionsStr = ""
			for (var i = 0; i < conversionOptions.length; i++){
				optionsStr += '<input class="form-control" name="' + conversionOptions[i] + '"placeholder="' + conversionOptions[i] +'(OPTIONAL)">'
			}
			$("#conversion-options").html(optionsStr);
		});
	});
});
