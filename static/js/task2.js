$(document).ready(function(){
	$('#start').on("click", function(){ 
		startRegression(); 
	});
});

// -- prints response from server as soon as some is available.
function startRegression(){
	$('#searchResults').empty();
	
	var xhr = new XMLHttpRequest();
    xhr.open('GET', 'regression', true);
    xhr.send(null);
    var timer, txtLength = 0;
    timer = window.setInterval(function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            window.clearTimeout(timer);
        }
		if(xhr.responseText.length > txtLength){
			$('#searchResults').append(xhr.responseText.substring(txtLength));
		}
		txtLength = xhr.responseText.length;
    }, 250);
}