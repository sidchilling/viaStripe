// Generated by CoffeeScript 1.4.0
(function() {
  var PaymentErrorView, PaymentSuccessfulView,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  PaymentErrorView = (function(_super) {

    __extends(PaymentErrorView, _super);

    function PaymentErrorView() {
      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return PaymentErrorView.__super__.constructor.apply(this, arguments);
    }

    PaymentErrorView.prototype.initialize = function() {
      this.template = $('#payment_error_tmpl').template();
      this.render();
      return this;
    };

    PaymentErrorView.prototype.render = function() {
      var tmpl_dict;
      tmpl_dict = {
        error: this.options.error_message
      };
      return $(this.el).html($.tmpl(this.template, tmpl_dict));
    };

    return PaymentErrorView;

  })(Backbone.View);

  PaymentSuccessfulView = (function(_super) {

    __extends(PaymentSuccessfulView, _super);

    function PaymentSuccessfulView() {
      this.render = __bind(this.render, this);

      this.initialize = __bind(this.initialize, this);
      return PaymentSuccessfulView.__super__.constructor.apply(this, arguments);
    }

    PaymentSuccessfulView.prototype.initialize = function() {
      this.template = $('#payment_successful_tmpl').template();
      this.render();
      return this;
    };

    PaymentSuccessfulView.prototype.render = function() {
      var tmpl_dict;
      tmpl_dict = {
        transaction_id: this.options.transaction_id,
        name_on_card: this.options.name_on_card,
        email: this.options.email,
        cost: this.options.cost
      };
      return $(this.el).html($.tmpl(this.template, tmpl_dict));
    };

    return PaymentSuccessfulView;

  })(Backbone.View);

  window.PaymentErrorView = PaymentErrorView;

  window.PaymentSuccessfulView = PaymentSuccessfulView;

}).call(this);
