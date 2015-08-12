var MOD_BASE = '';

// -- on load function, registers events
$(document).ready(function(){
	
	$('#mine').on("click", function(){ 
		mine(); 
	});
	renderRadioGroup();
});

function renderRadioGroup(){
	
	var radioMembers = ['Age', 'Sex', 'Race', 'Day of Admission',
						'Discharge Status', 'Stay Indicator', 'DRG Code',
						'Length of Stay', 'DRG Price', 'Total charges',
						'Covered charges', 'POA diagnosis indicator 1',
						'POA diagnosis inidicator 2', 'Diagnosis code 1', 
						'Diagnosis code 2', 'Procedure code 1',
						'Procedure code 2', 'Discharge destination',
						'Source of admission', 'Type of admission', 
						'Admitting diagnosis code'];
	var content = '';
	$.each(radioMembers, function(i, item){
		if(i%4 == 0){
			content += '<div class="row">';
		}
		content += '<div class="col-xs-3">';
		content += '<label class="checkbox-inline">';
		content += '<input type="checkbox" value="'+ i +'">' + item;
		content += '</label></div>';
		if(i%4 == 3){
			content += '</div>'
		}
	});
	$('#radioGroup').append(content);
						
}

/* validates input params to be send to server and
calls render function on response.*/
function mine(){
	
	// -- read param values
	var support = $('#support').val();
	var confidence = $('#confidence').val();
	if($.isEmptyObject(support) || $.isEmptyObject(confidence) || !$.isNumeric(support) || !$.isNumeric(confidence)){
		alert('Invalid Support or Confidence value');
		return;
	}
	var selected = $('#radioGroup input:checked').map(function() {
		return $(this).val();
	}).get().join(',');
	
	if($.isEmptyObject(selected) || selected.length < 3){
		alert('Atleast two attributes needs to be selected for mining');
		return;
	}
	
	var data = {'support': support,
				'confidence': confidence,
				'selected_attributes': selected};
				
	$.ajax({url: 'mine', 
			data: data, 
			type: 'GET',
			beforeSend:function(){
				$('#mineResults').empty();
				$('#mineResults').append('Processing ...');
			},
			success:function(result){
				renderResults(result.data);
			}});
}

/*Constructs HTML from the data retrieved and appends to Document.*/
function renderResults(data){
	
	$('#mineResults').empty();
	
	var content = '<table class="table table-bordered">';
	content += '<caption>Assocation mining results</caption>';
	content += '<thead><tr><th>Precedent</th>';
	content += '<th>Attribute</th>';
	content += '<th>Support (%)</th>';
	content += '<th>Confidence (%)</th>';
	content += '<th>Lift</th>';
	content += '</tr></thead>';
	
	var rows = '';
	$.each(data, function(i, item){
		rows += '<tr><td>' + item.attr_1 + '=' + item.attr_1_value + '</td>';
		rows += '<td>' + item.attr_2 + '=' + item.attr_2_value + '</td>';
		rows += '<td>' + item.support + '</td>';
		rows += '<td>' + item.confidence + '</td>';
		rows += '<td>' + item.lift + '</td></tr>';
	});
	
	content += '<tbody>' + rows + '</tbody></table>'
	
	$('#mineResults').append(content);
}