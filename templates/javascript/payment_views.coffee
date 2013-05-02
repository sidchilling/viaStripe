class PaymentErrorView extends Backbone.View
	initialize: =>
		@template = $('#payment_error_tmpl').template()
		@render()
		return @

	render: =>
		tmpl_dict =
			error : @options.error_message
		$(@el).html $.tmpl(@template, tmpl_dict)

class PaymentSuccessfulView extends Backbone.View
	initialize: =>
		@template = $('#payment_successful_tmpl').template()
		@render()
		return @

	render: =>
		tmpl_dict =
			transaction_id : @options.transaction_id
			name_on_card : @options.name_on_card
			email : @options.email
			cost : @options.cost
		$(@el).html $.tmpl(@template, tmpl_dict)

window.PaymentErrorView = PaymentErrorView
window.PaymentSuccessfulView = PaymentSuccessfulView
