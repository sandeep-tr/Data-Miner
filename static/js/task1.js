var MOD_BASE = '';
var age_group;
var sex;

// -- On load function, registers events and loads categories
$(document).ready(function(){
	age_group = $('#age_group').val();
	sex = $('#sex').val();
	
	if(age_group && sex){
		loadDiagnosis();
	}
	
	$('#age_group').on('change', function(event){
		age_group = $(this).val();
		loadDiagnosis();
	});
	$('#sex').on('change', function(event){
		sex = $(this).val();
		loadDiagnosis();
	});
	$('#search').on("click", function(){ 
		search(); 
	});
	loadCategories();
});

/* Fetches diagnosis codes corresponding to already 
selected Sex and Gender. Render function called on response. */
function loadDiagnosis(){
	
	var data = {'age_group': age_group,
				'sex': sex};
	$.ajax({url: 'data/diagnosis', 
			data: data, 
			type: 'GET',
			success:function(result){
				renderDiagnosisOpt(result);
			}});
}

/* Fetches diagnosis codes corresponding to already 
selected Sex and Gender. Render function called on response. */
function renderDiagnosisOpt(data){
	
	$('#diagnosis')
	.find('option')
	.remove()
	.end();	
	
	$.each(data.codes, function(i, item){
		$('#diagnosis').append($('<option>', {
			value: item.diagnosis_code,
			text: item.diagnosis_code
		}));
	});
}

/* Fetches metrics from the provided endpoint.
Render function called on response. */
function search(){
	
	// -- read param values
	var diagnosis = $('#diagnosis').val();
	if($.isEmptyObject(diagnosis)){
		alert('Please select a value for Admission diagnosis');
		return;
	}
	var data = {'age_group': age_group,
				'sex': sex,
				'diagnosis': diagnosis};
	
	$.ajax({url: 'search', 
			data: data, 
			type: 'GET',
			beforeSend:function(){
				$('#searchResults').empty();
				$('#searchResults').append('Processing ...');
			},
			success:function(result){
				renderSearchResults(result);
			}});
}

/* Render function for search method, constructs HTML from the 
retrieved data and appends to HTML.*/
function renderSearchResults(data){
	
	$('#searchResults').empty();
	
	var content = '<table class="table table-bordered">';
	content += '<caption>Search results</caption>';
	content += '<thead><tr><th></th>';
	content += '<th>Average length of stay (No.)</th>';
	content += '<th>Discharged alive (%)</th>';
	content += '<th>Average cost ($)</th>';
	content += '</tr></thead>';
	
	var specific = '<tr><td>Specific (Age/Gender/Diagnosis)</td>';
	specific += '<td>'+precise2(data.average_stay)+'</td>';
	specific += '<td>'+precise2(data.alive_status)+'</td>';
	specific += '<td>'+precise2(data.average_cost)+'</td></tr>';
	
	var common = '<tr><td>Common (Age/Gender)</td>';
	common += '<td>'+precise2(data.common_average_stay)+'</td>';
	common += '<td>'+precise2(data.common_alive_status)+'</td>';
	common += '<td>'+precise2(data.common_average_cost)+'</td></tr>';
	
	var deviation_ratio = '<tr><td>Deviation ratio (%)</td>';
	deviation_ratio += '<td>'+devRatio(data.average_stay, data.common_average_stay)+'</td>';
	deviation_ratio += '<td>'+devRatio(data.alive_status, data.common_alive_status)+'</td>';
	deviation_ratio += '<td>'+devRatio(data.average_cost, data.common_average_cost)+'</td></tr>';
	
	var abs_diff = '<tr><td>Absolute difference</td>';
	abs_diff += '<td>'+absDiff(data.average_stay, data.common_average_stay)+'</td>';
	abs_diff += '<td>'+absDiff(data.alive_status, data.common_alive_status)+'</td>';
	abs_diff += '<td>'+absDiff(data.average_cost, data.common_average_cost)+'</td></tr>';
	
	content += '<tbody>' + specific + common + deviation_ratio + abs_diff;
	content += '</tbody></table>'
	
	$('#searchResults').append(content);
}

function precise2(value){
	return value.toFixed(2);
}

function devRatio(value1, value2){
	return ((value1/value2) * 100).toFixed(2);
}

function absDiff(value1, value2){
	return (value1 - value2).toFixed(2);
}

/* Render function for search method, constructs HTML from the 
retrieved data and appends to Document.*/
function loadCategories(){
	
	$.ajax({url: 'categories', 
		type: 'GET',
		success:function(result){
			renderCategoryResults(result.categories);
		}});
}

/* Render function for retrieved category results from backend.
Constructs HTML from the data and appends to Document.*/
function renderCategoryResults(data){
	$('.table-responsive').empty();
	
	//-- 1
	var content = '<table class="table table-bordered">';
	content += '<caption>Top 10 Mortality rates</caption>';
	content += '<thead><tr><th>#</th>';
	content += '<th>Diagnosis</th>';
	content += '<th>Mortality rate (%)</th>';
	content += '</tr></thead>';
	
	var body = '<tbody>';
	$.each(data.top_mortality_rate, function(i, item){
		body += '<tr><td>'+(i+1)+'</td>';
		body += '<td>'+item.diagnosis_code+'</td>'
		body += '<td>'+item.mortality_rate+'</td></tr>'
	});
	body += '</tbody>';
	content += body + '</table>';
	$('.table-responsive:eq(0)').append(content);
	
	//-- 2
	content = '<table class="table table-bordered">';
	content += '<caption>Top 10 Expensive diagnosis</caption>';
	content += '<thead><tr><th>#</th>';
	content += '<th>Diagnosis</th>';
	content += '<th>Average cost ($)</th>';
	content += '</tr></thead>';
	
	body = '<tbody>';
	$.each(data.top_average_charges, function(i, item){
		body += '<tr><td>'+(i+1)+'</td>';
		body += '<td>'+item.diagnosis_code+'</td>'
		body += '<td>'+item.avg_charges+'</td></tr>'
	});
	body += '</tbody>';
	content += body + '</table>';
	$('.table-responsive:eq(1)').append(content);
	
	//-- 3
	content = '<table class="table table-bordered">';
	content += '<caption>Top 10 Length of stay</caption>';
	content += '<thead><tr><th>#</th>';
	content += '<th>Diagnosis</th>';
	content += '<th>Average stay (No.)</th>';
	content += '</tr></thead>';
	
	body = '<tbody>';
	$.each(data.top_average_stay, function(i, item){
		body += '<tr><td>'+(i+1)+'</td>';
		body += '<td>'+item.diagnosis_code+'</td>'
		body += '<td>'+item.avg_stay+'</td></tr>'
	});
	body += '</tbody>';
	content += body + '</table>';
	$('.table-responsive:eq(2)').append(content);
}