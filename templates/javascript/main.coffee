# This contains all the javascript needed by the merchant side

window.bind_live_toggle_btn = () ->
	live_toggle_params =
		onClick : (event, status) ->
			livemode_toggle status
	$('.live_toggle').toggleSlide live_toggle_params

window.bind_toggle_btn = (btns) ->
	toggle_params = {}
	for btn in btns
		$(".#{btn}").toggleSlide toggle_params

livemode_toggle = (status) ->
	if status.attr('checked')
		# changing from Live mode to Test Mode - check whether test mode is allowed or not
		ajax_params =
			url : '/check_test_mode_allowed'
			data :
				form_id : $('#form_id').val()
			dataType : 'json'
			type : 'POST'
			error : (obj, txt) ->
				console.log "Some error occurred: #{txt}"
			success : (response) ->
				if response.error
					console.log "Some error occurred: #{response.error}"
				else if response.success
					if response.not_allowed
						view_dict =
							test_stripe_connect_url : response.test_stripe_connect_url
						window.append_backbone_modal StripeTestConnectModalView, view_dict, 'modal_container'
						$('#test_connect_modal').modal()
		$.ajax ajax_params

show_payment_progress_bar = () ->
	view = new PaymentProgressView
	$('#payments_tab').html ''
	$(view.el).appendTo '#payments_tab'
	window.interval_timer_id = window.setInterval ->
		if window.current_progres_bar_width <= 80
			window.current_progres_bar_width = window.current_progres_bar_width + 10
			$('#payments_progress_bar').css('width', "#{window.current_progres_bar_width}%")
	, 1000

window.get_payments = () ->
	window.current_progres_bar_width = 5
	show_payment_progress_bar()
	ajax_params =
		url : '/get_form_transactions'
		data :
			form_id : $('#form_id').val()
		dataType : 'json'
		type : 'POST'
		error : (obj, txt) ->
			window.clearInterval window.interval_timer_id
			window.show_error_view 'Unexpected Error', txt, 'payments_tab'
		success : (response) ->
			window.clearInterval window.interval_timer_id
			if response.error
				window.show_error_view 'Unexpected Error', response.error, 'payments_tab'
			else
				$('#payments_progress_bar').css('width', '100%')
				report_view_dict =
					transactions : response.transactions
				report_view = new TransactionReportView report_view_dict
				$('#payments_tab').html ''
				$(report_view.el).appendTo '#payments_tab'
	$.ajax ajax_params

window.submit_user_details = (ev) ->
	$(this).button 'loading'
	ajax_params =
		url : '/save_user_details'
		data :
			name : $.trim $('#name').val()
			business_name : $.trim $('#business_name').val()
			terms_url : $.trim $('#terms_url').val()
		dataType : 'json'
		type : 'POST'
		error : (obj, txt) ->
			$(this).button 'reset'
			alert 'Error occurred'
		success : (response) ->
			if response.error
				alert "Error: #{response.error}"
			else if response.success
				window.location.reload()
	$.ajax ajax_params

window.create_new_form = (ev) ->
	$(this).button 'loading'
	$('#new_form_alert').hide()
	$('#error_form_alert').hide()
	form_name = $.trim $('#form_name').val()
	if form_name.length > 0
		ajax_params =
			url : '/save_new_form'
			data :
				name : form_name
			dataType : 'json'
			type : 'POST'
			error : (obj, txt) ->
				$(this).button 'reset'
				$('#error_form_alert').show()
			success : (response) ->
				if response.error
					$(this).button 'reset'
					$('#error_form_alert').show()
				else if response.success
					window.location.href = "/form_conf?id=#{response.id}"
		$.ajax ajax_params
	else
		$(this).button 'reset'
		$('#new_form_alert').show()
		$('#form_name').closest('.control-group').addClass 'error'

window.save_form_conf = (ev) ->
	ajax_params =
		url : '/save_form_conf'
		type : 'POST'
		dataType : 'json'
		data :
			id : $.trim $('#form_id').val()
			cost : $.trim $('#cost').val()
			seller_name : $.trim $('#seller_name').val()
			seller_email : $.trim $('#seller_email').val()
			description : $.trim $('#description').val()
			billing_address_required : if $('#billing_address_required').is(':checked') then 'true' else ''
			send_payment_receipts : if $('#send_invoice_email').is(':checked') then 'true' else ''
			bcc_email : if $('#bcc_email').is(':checked') then 'true' else ''
			livemode : if $('#livemode').is(':checked') then 'true' else ''
		error : (obj, txt) ->
			alert 'Error'
		success : (response) ->
			if response.error
				alert "Error: #{response.error}"
			else if response.success
				window.location.reload()
	$(this).button 'loading'
	$.ajax ajax_params

window.form_tr_hover_in = (ev) ->
	# Show Preview Button
	$(".#{$(this).attr('data-form-id')}").show()

window.form_tr_hover_out = (ev) ->
	# Hide Preview Button
	$(".#{$(this).attr('data-form-id')}").hide()

window.show_form_delete_modal = (ev) ->
	view_dict =
		form_name : $(this).attr('data-form-name')
		form_id : $(this).attr('data-form-id')
	window.append_backbone_modal FormDeleteModalView, view_dict, 'delete_modal_container'
	$('#delete_modal').modal()
