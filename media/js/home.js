function gup( name )
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}

function replyTo(message_id){
	var form = document.getElementById('id_write_review_to_message_form');
	form.text="";
	form.style.visibility = "visible";
	document.getElementById('id_message_parent_id').value = message_id;
	var message = document.getElementById('message_id_'+message_id);
	message.appendChild(form);
	message.appendChild(document.createElement("br"));
}


function detach_form(){
	var form = document.getElementById('id_write_review_to_message_form');
	form.style.visibility = "hidden";
	div = document.getElementById('div_for_form')
	div.appendChild(form);

}

function create_label(text, label_for){
	var label  = document.createElement("Label");
	label.setAttribute("for", label_for);
	label.innerHTML = text;
	return label;
}

function create_mssg_child(message, flag){
	var old = document.getElementById("message_id_"+message.id);
	if(old){
		old.parentNode.removeChild(old);
	}
	var htmldata =
		message.id+
		'<i align="left" style="font-size: 18px; font-weight: 100; margin-left:2%;">'+message.text+'</i>'+
		'<i id="'+message.id+'_note" ><a style="margin-left:30%">'+ message.date_and_time +'</a>'+
			'<div  style="margin-left:50%; font-size: 14px; font-weight: 100;">'+
			'<a id="showChilds_'+ message.id +"\" href=\"#\" onclick=\"show_childs_or_tree('childs', "+message.id +')">Show comments of message</a><br>'+
			'<a id="showTree_'+ message.id +"\" href=\"#\" onclick=\"show_childs_or_tree('trees', "+message.id +')">Show whole discussion of this message</a><br>'+
			'<a id="replyTo_'+ message.id +' href="#" onclick="replyTo('+ message.id +')">Reply</a><br>'+
			'</div>'+
		'</i>'+
		'<br>';
	var e = document.createElement('div');
	e.id = "message_id_"+message.id;
	e.setAttribute('style',"margin-left:"+message.level+"%");
	e.innerHTML = htmldata;
	e.appendChild(document.createElement('br'));
	return e;
}

function show_childs_or_tree(key, id){
	var dictionary={};
	dictionary[key] = id;
	var data = $.param(dictionary);
	$.ajax({
		url: "/show_childs_or_tree/",
		data: data,
		dataType: 'json',
		success: function(resp) {
			if(resp.messages){
				var id = document.getElementById('message_id_' + resp.id);
				var parent = document.getElementById('messages');
				var div = document.getElementById('div_for_form')
				for (var i=resp.messages.length-1; i>=0; i--){
					var message = create_mssg_child(resp.messages[i], key=="trees");
					parent.insertBefore(message, id);
					div.appendChild(id);
					parent.insertBefore(id, message);
				}
				detach_form();
				if('trees' in resp){
					for(var i=0; i<resp.trees.length; i++ ){
						child = document.getElementById('showChilds_' + resp.trees[i]);
						tree = document.getElementById('showTree_' + resp.trees[i]);
						tree.style.visibility = "hidden";
						child.style.visibility = "hidden";
					}
				}else if('childs' in resp){
					node_id = document.getElementById('showChilds_' + resp.childs);
					node_id.style.visibility = "hidden";
				}
				window.history.replaceState(document.title+resp.location, document.title, resp.location);
			} else {
				for (error in resp.errors){								
					var id = document.getElementById('id_' + error).parentNode;
					id.appendChild(create_label(error+" is "+resp.errors[error], "id_error_" + error));
				}
			}
		},
		error: function(resp) {
			err_dict = {};
			for(e in resp){
				err_dict[e] = resp[e];
				console.log(resp[e]);
			}
			alert("Error: "+err_dict);
		},

	});
}
	
$(document).ready(function(){

	$('input[id="cancel"]').click(function(){
		detach_form();
	});
	
	
	$('#id_write_review_to_message_form').submit(function(event){
		event.preventDefault();
		$.ajax({
			type: 'POST',
			data: $(this).serialize(),
			url: "/write_review/",
			dataType: 'json',
			success: function(resp) {
				if(resp.message_type == 'success'){
					var id = document.getElementById('message_id_' + resp.parent_id);
					id.appendChild(create_label("Your message was successfully added", "comment_" + resp.parent_id));
					showchilds_or_tree("childs", resp.parent_id);
				} else {
					for (error in resp.errors){								
						var id = document.getElementById('id_' + error).parentNode;
						id.appendChild(create_label(error+" is "+resp.errors[error], "id_error_" + error));
					}
				}
			},
			error: function(resp) {
				alert("Error: "+resp);
			}
		});
	});
	

});