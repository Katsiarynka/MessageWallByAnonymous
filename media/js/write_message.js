$(document).ready(function(){
	$('#message_form').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			data: $(this).serialize(),
			url: "/write_message/",
			dataType: 'json',
			
			success: function(resp) {
				if(resp.message_type == 'success'){
					window.location.replace(document.referer || '/');
				} else {
					for (error in resp.errors){								
						var id = document.getElementById('id_' + error).parentNode;
						var label  = document.createElement("Label");
						label.setAttribute("for", "id_error_" + error);
						label.innerHTML = error+" is "+resp.errors[error];
						id.appendChild(document.createElement("br"));
						id.appendChild(label);
					}
				}
			},
			error: function(resp) {
				alert("Error: "+resp);
			},
		});
	});
});
