	// title validation
	function validate_title() {
		// for testing
		return true;
		var 
			re_title = /^[0-9a-zA-Z\_][0-9a-zA-Z\_\s]{0,49}$/,
			title = $('#title');
			if (re_title.test(title.val())) return true;
			alert('Invalid title format.');
			return false;
	}

	// Category validation
	function validate_cat() {
		// for testing
		return true;
		var
			re_cat = /^[0-9a-zA-Z\.\_]{1,20}$/,
			cat = $('#category');
			if (re_cat.test(cat.val())) return true;
			alert('Invalid category format.');
			return false;
	}

	// tag validation
	function valiadate_tag() {
		// for testing
		return true;
		var
			re_tag = /^[0-9a-zA-Z\_\,]{0,256}$/,
			tags = $('#tags');
			if (re_tag.test(tags.val())) return true;
			alert('Invalid tags format.');
			return false;
	}

	// text validation
	function validate_text() {
		// for testing
		return true;
		if ($('#plainText').val() != '') return true;
		alert('Nothing is wrtten!')
		return false;		
	}

	$('#publish').click(function() {
		if (validate_title() && validate_cat() && valiadate_tag() && validate_text()) {
			$('#draft').val(false);
	    	$('#text_form').submit();
		} 
	});

	$('#sava_draft').click(function() {
		if (validate_title() && validate_cat() && valiadate_tag() && validate_text()) {
			$('#draft').val(true);
	    	$('#text_form').submit();
		} 
	});

	window.onload = function() {
		$("#plainText").markdown({autofocus:true, iconlibrary:'fa'});
	}