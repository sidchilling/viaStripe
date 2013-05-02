class FormDeleteModalView extends Backbone.View
	initialize: =>
		@template = $('#delete_form_modal').template()
		@render()
		return @

	render: =>
		tmpl_dict =
			form_name : @options.form_name
		$(@el).html $.tmpl(@template, tmpl_dict)
	
	events: =>
		'click #delete_form_btn' : 'delete_form'
	
	delete_form: (ev) =>
		ajax_params =
			url : '/form_delete'
			type : 'POST'
			dataType : 'json'
			data :
				id : @options.form_id
			error : (obj, txt) ->
				alert 'Error while deleting the form'
			success : (response) ->
				if response.error
					alert "Error: #{response.error}"
				else if response.success
					window.location.reload()
		$(ev.currentTarget).button 'loading'
		$.ajax ajax_params

class StripeTestConnectModalView extends Backbone.View
	initialize: =>
		@template = $('#test_stripe_connect_modal').template()
		@render()
		return @
	
	render: =>
		tmpl_dict =
			test_stripe_connect_url : @options.test_stripe_connect_url
		$(@el).html $.tmpl(@template, tmpl_dict)

class PaymentProgressView extends Backbone.View
	initialize: =>
		@template = $('#payments_progress_bar_tmpl').template()
		@render()
		return @

	render: =>
		$(@el).html $.tmpl(@template)

class GenericErrorView extends Backbone.View
	initialize: =>
		@template = $('#generic_error_tmpl').template()
		@render()
		return @

	render: =>
		tmpl_dict =
			error_heading : @options.error_heading
			error_msg : @options.error_msg
		$(@el).html $.tmpl(@template, tmpl_dict)

class TransactionReportView extends Backbone.View
	initialize: =>
		@template = $('#transaction_report_tmpl').template()
		@render()
		return @

	render: =>
		tmpl_dict =
			transactions : @options.transactions
		$(@el).html $.tmpl(@template, tmpl_dict)

window.FormDeleteModalView = FormDeleteModalView
window.StripeTestConnectModalView = StripeTestConnectModalView
window.PaymentProgressView = PaymentProgressView
window.GenericErrorView = GenericErrorView
window.TransactionReportView = TransactionReportView
