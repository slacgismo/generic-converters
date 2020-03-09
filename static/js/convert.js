$(document).ready(function(){
	fromToConversion = fromToConversion.replace(/'/g,'"');
	fromToConversion = fromToConversion.replace(/<.*?>/g, "null")
	fromToConversion = fromToConversion.replace("False", "false")
	fromToConversion = fromToConversion.replace("True", "true")
	fromToConversion = fromToConversion.replace("None", "null")
	var conversionDict = JSON.parse(fromToConversion);

	var convertTo = $("#convert-to").val();
	var convertFrom = $("#convert-from").val();
	$("#convert-to, #convert-from").change(function(){
		convertTo = $("#convert-to").val();
		convertFrom = $("#convert-from").val();
		conversionOptions = Object.keys(conversionDict[convertFrom][convertTo]["defaults"])
		var optionsStr = ""
		for (var i = 0; i < conversionOptions.length; i++){
			optionsStr += '<input class="form-control" name="' + conversionOptions[i] + '"placeholder="' + conversionOptions[i] +'(OPTIONAL)">'
		}
		$("#conversion-options").html(optionsStr);
	});
});
