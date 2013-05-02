window.append_backbone_modal = (backbone_class, data, container_id) ->
	modal_view = new backbone_class data
	$("##{container_id}").html ''
	$(modal_view.el).appendTo "##{container_id}"

window.show_error_view = (error_heading, error_msg, div_id) ->
	data =
		error_heading : error_heading
		error_msg : error_msg
	view = new GenericErrorView data
	$("##{div_id}").html ''
	$(view.el).appendTo "##{div_id}"
