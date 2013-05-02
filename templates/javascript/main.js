// Generated by CoffeeScript 1.4.0
(function() {
  var livemode_toggle, show_payment_progress_bar;

  window.bind_live_toggle_btn = function() {
    var live_toggle_params;
    live_toggle_params = {
      onClick: function(event, status) {
        return livemode_toggle(status);
      }
    };
    return $('.live_toggle').toggleSlide(live_toggle_params);
  };

  window.bind_toggle_btn = function(btns) {
    var btn, toggle_params, _i, _len, _results;
    toggle_params = {};
    _results = [];
    for (_i = 0, _len = btns.length; _i < _len; _i++) {
      btn = btns[_i];
      _results.push($("." + btn).toggleSlide(toggle_params));
    }
    return _results;
  };

  livemode_toggle = function(status) {
    var ajax_params;
    if (status.attr('checked')) {
      ajax_params = {
        url: '/check_test_mode_allowed',
        data: {
          form_id: $('#form_id').val()
        },
        dataType: 'json',
        type: 'POST',
        error: function(obj, txt) {
          return console.log("Some error occurred: " + txt);
        },
        success: function(response) {
          var view_dict;
          if (response.error) {
            return console.log("Some error occurred: " + response.error);
          } else if (response.success) {
            if (response.not_allowed) {
              view_dict = {
                test_stripe_connect_url: response.test_stripe_connect_url
              };
              window.append_backbone_modal(StripeTestConnectModalView, view_dict, 'modal_container');
              return $('#test_connect_modal').modal();
            }
          }
        }
      };
      return $.ajax(ajax_params);
    }
  };

  show_payment_progress_bar = function() {
    var view;
    view = new PaymentProgressView;
    $('#payments_tab').html('');
    $(view.el).appendTo('#payments_tab');
    return window.interval_timer_id = window.setInterval(function() {
      if (window.current_progres_bar_width <= 80) {
        window.current_progres_bar_width = window.current_progres_bar_width + 10;
        return $('#payments_progress_bar').css('width', "" + window.current_progres_bar_width + "%");
      }
    }, 1000);
  };

  window.get_payments = function() {
    var ajax_params;
    window.current_progres_bar_width = 5;
    show_payment_progress_bar();
    ajax_params = {
      url: '/get_form_transactions',
      data: {
        form_id: $('#form_id').val()
      },
      dataType: 'json',
      type: 'POST',
      error: function(obj, txt) {
        window.clearInterval(window.interval_timer_id);
        return window.show_error_view('Unexpected Error', txt, 'payments_tab');
      },
      success: function(response) {
        var report_view, report_view_dict;
        window.clearInterval(window.interval_timer_id);
        if (response.error) {
          return window.show_error_view('Unexpected Error', response.error, 'payments_tab');
        } else {
          $('#payments_progress_bar').css('width', '100%');
          report_view_dict = {
            transactions: response.transactions
          };
          report_view = new TransactionReportView(report_view_dict);
          $('#payments_tab').html('');
          return $(report_view.el).appendTo('#payments_tab');
        }
      }
    };
    return $.ajax(ajax_params);
  };

  window.submit_user_details = function(ev) {
    var ajax_params;
    $(this).button('loading');
    ajax_params = {
      url: '/save_user_details',
      data: {
        name: $.trim($('#name').val()),
        business_name: $.trim($('#business_name').val()),
        terms_url: $.trim($('#terms_url').val())
      },
      dataType: 'json',
      type: 'POST',
      error: function(obj, txt) {
        $(this).button('reset');
        return alert('Error occurred');
      },
      success: function(response) {
        if (response.error) {
          return alert("Error: " + response.error);
        } else if (response.success) {
          return window.location.reload();
        }
      }
    };
    return $.ajax(ajax_params);
  };

  window.create_new_form = function(ev) {
    var ajax_params, form_name;
    $(this).button('loading');
    $('#new_form_alert').hide();
    $('#error_form_alert').hide();
    form_name = $.trim($('#form_name').val());
    if (form_name.length > 0) {
      ajax_params = {
        url: '/save_new_form',
        data: {
          name: form_name
        },
        dataType: 'json',
        type: 'POST',
        error: function(obj, txt) {
          $(this).button('reset');
          return $('#error_form_alert').show();
        },
        success: function(response) {
          if (response.error) {
            $(this).button('reset');
            return $('#error_form_alert').show();
          } else if (response.success) {
            return window.location.href = "/form_conf?id=" + response.id;
          }
        }
      };
      return $.ajax(ajax_params);
    } else {
      $(this).button('reset');
      $('#new_form_alert').show();
      return $('#form_name').closest('.control-group').addClass('error');
    }
  };

  window.save_form_conf = function(ev) {
    var ajax_params;
    ajax_params = {
      url: '/save_form_conf',
      type: 'POST',
      dataType: 'json',
      data: {
        id: $.trim($('#form_id').val()),
        cost: $.trim($('#cost').val()),
        seller_name: $.trim($('#seller_name').val()),
        seller_email: $.trim($('#seller_email').val()),
        description: $.trim($('#description').val()),
        billing_address_required: $('#billing_address_required').is(':checked') ? 'true' : '',
        send_payment_receipts: $('#send_invoice_email').is(':checked') ? 'true' : '',
        bcc_email: $('#bcc_email').is(':checked') ? 'true' : '',
        livemode: $('#livemode').is(':checked') ? 'true' : ''
      },
      error: function(obj, txt) {
        return alert('Error');
      },
      success: function(response) {
        if (response.error) {
          return alert("Error: " + response.error);
        } else if (response.success) {
          return window.location.reload();
        }
      }
    };
    $(this).button('loading');
    return $.ajax(ajax_params);
  };

  window.form_tr_hover_in = function(ev) {
    return $("." + ($(this).attr('data-form-id'))).show();
  };

  window.form_tr_hover_out = function(ev) {
    return $("." + ($(this).attr('data-form-id'))).hide();
  };

  window.show_form_delete_modal = function(ev) {
    var view_dict;
    view_dict = {
      form_name: $(this).attr('data-form-name'),
      form_id: $(this).attr('data-form-id')
    };
    window.append_backbone_modal(FormDeleteModalView, view_dict, 'delete_modal_container');
    return $('#delete_modal').modal();
  };

}).call(this);