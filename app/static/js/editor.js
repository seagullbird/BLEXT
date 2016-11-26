	// text validation
	function validate_text() {
		// for testing
		return true;
		if ($('#plainText').val() != '') return true;
		alert('Nothing is wrtten!')
		return false;		
	}

	$('#publish').click(function() {
		if (validate_text()) {
			$('#draft').val(false);
	    	$('#text_form').submit();
		} 
	});

	$('#sava_draft').click(function() {
		if (validate_text()) {
			$('#draft').val(true);
	    	$('#text_form').submit();
		} 
	});

	window.onload = function() {
		$("#plainText").markdown({autofocus:true, iconlibrary:'fa'});
	}