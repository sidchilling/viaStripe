remove_error = () ->
	$('.control-group').removeClass 'error'
	$('#payment_error_div').html ''

validate_fields = (fields) ->
	is_blank = false
	for field in fields
		if $.trim($("##{field}").val()) == ''
			is_blank = true
			$("##{field}").closest('.control-group').addClass 'error'
	if is_blank then return false else return true

window.address_payment = (ev) ->
	$(this).button 'loading'
	remove_error()
	fields = [
		'name_on_card',
		'email',
		'card_number',
		'security_code',
		'card_expiry_month',
		'card_expiry_year',
		'billing_address',
		'city',
		'state',
		'postal_code',
		'country'
	]
	if validate_fields fields
		get_stripe_token address_stripe_response_handler
	else
		show_payment_error 'Please enter the fields marked in red'
		$(this).button 'reset'

get_stripe_token = (callback) ->
	stripe_params =
		number : $('#card_number').val()
		cvc : $('#security_code').val()
		exp_month : $('#card_expiry_month').val()
		exp_year : $('#card_expiry_year').val()
	Stripe.createToken stripe_params, callback

window.no_address_payment = (ev) ->
	$(this).button 'loading'
	remove_error()
	fields = [
		'name_on_card',
		'email',
		'card_number',
		'security_code',
		'card_expiry_month',
		'card_expiry_year'
	]
	if validate_fields fields
		get_stripe_token no_address_stripe_response_handler
	else
		show_payment_error 'Please enter the fields marked in red'
		$(this).button 'reset'

show_payment_error = (error_msg) ->
	data =
		error_message : error_msg
	modal_view = new PaymentErrorView data
	$("#payment_error_div").html ''
	$(modal_view.el).appendTo '#payment_error_div'

reset_address_pay_btn = () ->
	$('#address_pay_btn').button 'reset'

reset_no_address_pay_btn = () ->
	$('#no_address_pay_btn').button 'reset'

address_stripe_response_handler = (status, response) ->
	if response.error
		show_payment_error response.error.message
		reset_address_pay_btn()
	else
		ajax_params =
			url : '/submit_payment_with_address'
			dataType : 'json'
			type : 'POST'
			error : (obj, txt) ->
				show_payment_error txt
				reset_address_pay_btn()
			success : (response) ->
				if response.error
					show_payment_error response.error
					reset_address_pay_btn()
				else
					show_payment_success response
			data :
				token : response['id']
				form_id : $.trim $('#form_id').val()
				name_on_card : $.trim $('#name_on_card').val()
				email : $.trim $('#email').val()
				billing_address : $.trim $('#billing_address').val()
				city : $.trim $('#city').val()
				state : $.trim $('#state').val()
				postal_code : $.trim $('#postal_code').val()
				country : $.trim $('#country').val()
		$.ajax ajax_params
	
window.make_country_typeahead = () ->
	countries = ['AFGHANISTAN', 'ALAND ISLANDS', 'ALBANIA', 'ALGERIA', 'AMERICAN SAMOA', 'ANDORRA', 'ANGOLA', 'ANGUILLA', 'ANTARCTICA',
		'ANTIGUA AND BARBUDA', 'ARGENTINA', 'ARMENIA', 'ARUBA', 'AUSTRALIA', 'AUSTRIA', 'AZERBAIJAN', 'BAHAMAS', 'BAHRAIN', 'BANGLADESH',
		'BARBADOS', 'BELARUS', 'BELGIUM', 'BELIZE', 'BENIN', 'BERMUDA', 'BHUTAN', 'BOLIVIA PLURINATIONAL STATE OF', 'BONAIRE SINT EUSTATIUS AND SABA',
		'BOSNIA AND HERZEGOVINA', 'BOTSWANA', 'BOUVET ISLAND', 'BRAZIL', 'BRITISH INDIAN OCEAN TERRITORY', 'BRUNEI DARUSSALAM', 'BULGARIA', 'BURKINA FASO',
		'BURUNDI', 'CAMBODIA', 'CAMEROON', 'CANADA', 'CAPE VERDE', 'CAYMAN ISLANDS', 'CENTRAL AFRICAN REPUBLIC', 'CHAD', 'CHILE', 'CHINA',
		'CHRISTMAS ISLAND', 'COCOS KEELING) ISLANDS', 'COLOMBIA', 'COMOROS', 'CONGO', 'CONGO THE DEMOCRATIC REPUBLIC OF THE', 'COOK ISLANDS',
		'COSTA RICA', 'COTE D\'IVOIRE', 'CROATIA', 'CUBA', 'CURACAO', 'CYPRUS', 'CZECH REPUBLIC', 'DENMARK', 'DJIBOUTI', 'DOMINICA', 'DOMINICAN REPUBLIC',
		'ECUADOR', 'EGYPT', 'EL SALVADOR', 'EQUATORIAL GUINEA', 'ERITREA', 'ESTONIA', 'ETHIOPIA', 'FALKLAND ISLANDS MALVINAS', 'FAROE ISLANDS', 'FIJI', 'FINLAND',
		'FRANCE', 'FRENCH GUIANA', 'FRENCH POLYNESIA', 'FRENCH SOUTHERN TERRITORIES', 'GABON', 'GAMBIA', 'GEORGIA', 'GERMANY', 'GHANA', 'GIBRALTAR', 'GREECE',
		'GREENLAND', 'GRENADA', 'GUADELOUPE', 'GUAM', 'GUATEMALA', 'GUERNSEY', 'GUINEA', 'GUINEA-BISSAU', 'GUYANA', 'HAITI', 'HEARD ISLAND AND MCDONALD ISLANDS',
		'HOLY SEE VATICAN CITY STATE', 'HONDURAS', 'HONG KONG', 'HUNGARY', 'ICELAND', 'INDIA', 'INDONESIA', 'IRAN ISLAMIC REPUBLIC OF', 'IRAQ', 'IRELAND',
		'ISLE OF MAN', 'ISRAEL', 'ITALY', 'JAMAICA', 'JAPAN', 'JERSEY', 'JORDAN', 'KAZAKHSTAN', 'KENYA', 'KIRIBATI', 'KOREA DEMOCRATIC PEOPLE\'S REPUBLIC OF',
		'KOREA REPUBLIC OF', 'KUWAIT', 'KYRGYZSTAN', 'LAO PEOPLE\'S DEMOCRATIC REPUBLIC', 'LATVIA', 'LEBANON', 'LESOTHO', 'LIBERIA', 'LIBYAN ARAB JAMAHIRIYA',
		'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'MACAO', 'MACEDONIA THE FORMER YUGOSLAV REPUBLIC OF', 'MADAGASCAR', 'MALAWI', 'MALAYSIA', 'MALDIVES',
		'MALI', 'MALTA', 'MARSHALL ISLANDS', 'MARTINIQUE', 'MAURITANIA', 'MAURITIUS', 'MAYOTTE', 'MEXICO', 'MICRONESIA FEDERATED STATES OF', 'MOLDOVA REPUBLIC OF',
		'MONACO', 'MONGOLIA', 'MONTENEGRO', 'MONTSERRAT', 'MOROCCO', 'MOZAMBIQUE', 'MYANMAR', 'NAMIBIA', 'NAURU', 'NEPAL', 'NETHERLANDS', 'NEW CALEDONIA',
		'NEW ZEALAND', 'NICARAGUA', 'NIGER', 'NIGERIA', 'NIUE', 'NORFOLK ISLAND', 'NORTHERN MARIANA ISLANDS', 'NORWAY', 'OMAN', 'PAKISTAN', 'PALAU',
		'PALESTINIAN TERRITORY OCCUPIED', 'PANAMA', 'PAPUA NEW GUINEA', 'PARAGUAY', 'PERU', 'PHILIPPINES', 'PITCAIRN', 'POLAND', 'PORTUGAL', 'PUERTO RICO',
		'QATAR', 'REUNION', 'ROMANIA', 'RUSSIAN FEDERATION', 'RWANDA', 'SAINT BARTHELEMY', 'SAINT HELENA ASCENSION AND TRISTAN DA CUNHA', 'SAINT KITTS AND NEVIS',
		'SAINT LUCIA', 'SAINT MARTIN FRENCH PART', 'SAINT PIERRE AND MIQUELON', 'SAINT VINCENT AND THE GRENADINES', 'SAMOA', 'SAN MARINO', 'SAO TOME AND PRINCIPE',
		'SAUDI ARABIA', 'SENEGAL', 'SERBIA', 'SEYCHELLES', 'SIERRA LEONE', 'SINGAPORE', 'SINT MAARTEN DUTCH PART', 'SLOVAKIA', 'SLOVENIA', 'SOLOMON ISLANDS',
		'SOMALIA', 'SOUTH AFRICA', 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS', 'SPAIN', 'SRI LANKA', 'SUDAN', 'SURINAME', 'SVALBARD AND JAN MAYEN',
		'SWAZILAND', 'SWEDEN', 'SWITZERLAND', 'SYRIAN ARAB REPUBLIC', 'TAIWAN PROVINCE OF CHINA', 'TAJIKISTAN', 'TANZANIA UNITED REPUBLIC OF', 'THAILAND',
		'TIMOR-LESTE', 'TOGO', 'TOKELAU', 'TONGA', 'TRINIDAD AND TOBAGO', 'TUNISIA', 'TURKEY', 'TURKMENISTAN', 'TURKS AND CAICOS ISLANDS', 'TUVALU', 'UGANDA',
		'UKRAINE', 'UNITED ARAB EMIRATES', 'UNITED KINGDOM', 'UNITED STATES', 'UNITED STATES MINOR OUTLYING ISLANDS', 'URUGUAY', 'UZBEKISTAN', 'VANUATU',
		'VENEZUELA BOLIVARIAN REPUBLIC OF', 'VIET NAM', 'VIRGIN ISLANDS BRITISH', 'VIRGIN ISLANDS U.S.', 'WALLIS AND FUTUNA', 'WESTERN SAHARA', 'YEMEN', 
		'ZAMBIA', 'ZIMBABWE']
	typeahead_params =
		source : countries
		items : 4
		minLength : 1
	$('.typeahead').typeahead typeahead_params

show_payment_success = (response) ->
	transaction_data =
		transaction_id : response.transaction_id
		name_on_card : response.name_on_card
		email : response.email
		cost : response.cost
	payment_successful_view = new PaymentSuccessfulView transaction_data
	$('#main_payment_container').html ''
	$(payment_successful_view.el).appendTo '#main_payment_container'

no_address_stripe_response_handler = (status, response) ->
	if response.error
		show_payment_error response.error.message
		reset_no_address_pay_btn()
	else
		ajax_params =
			url : '/submit_payment_without_address'
			dataType : 'json'
			type : 'POST'
			error : (obj, txt) ->
				show_payment_error txt
				reset_no_address_pay_btn()
			success : (response) ->
				if response.error
					show_payment_error response.error
					reset_no_address_pay_btn()
				else
					show_payment_success response
			data :
				token : response['id']
				form_id : $.trim $('#form_id').val()
				name_on_card : $.trim $('#name_on_card').val()
				email : $.trim $('#email').val()
		$.ajax ajax_params

