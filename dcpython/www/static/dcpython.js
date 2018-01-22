/* DG Strip Donations */

/* global jQuery, console, Stripe, window */

jQuery(function ($) {
  "use strict";

  var DONATION_AMTS = [
    ["aws", 2500],
    ["platinum", 1000],
    ["gold", 500],
    ["silver", 250],
    ["bronze", 100],
    ["individual", 50],
    ["other", 0]
  ];

  var DONATION_AMTS_DICT = {
    aws: 2500,
    platinum: 1000,
    gold: 500,
    silver: 250,
    bronze: 100,
    individual: 50,
    other: 25
  };

  // DONATION TEXTBOX VALUE CHANGE
  var handle_donation_change = function () {
    var i;
    var donation = parseFloat($("#donationAmt").val());
    for (i = 0; i < DONATION_AMTS.length; i++) {
      $("." + DONATION_AMTS[i][0]).removeClass("active");
    }
    for (i = 0; i < DONATION_AMTS.length; i++) {
      if (donation >= DONATION_AMTS[i][1]) {
        $("." + DONATION_AMTS[i][0]).addClass("active");
        break;
      }
    }
    $("#id_donation").val(donation);
  };

  $("#donationAmt").change(handle_donation_change).keyup(handle_donation_change);
  handle_donation_change();

  // LEVEL CLICKS
  var handle_donor_lvl_click = function (e) {
    var donation = DONATION_AMTS_DICT[$(e.currentTarget).attr("class").split(" ")[1]];

    $("#donationAmt").val(donation);
    handle_donation_change();
  };

  $(".donor_lvl").click(handle_donor_lvl_click);

  // DONATION SOURCE CHANGE
  var handle_donation_source_change = function (e) {
    var donation_source = $(e.target).val();

    $(".payment-form").addClass("hidden");
    $("#form-" + donation_source).removeClass("hidden");
    $("#id_donation_type").val(donation_source);
  };


  $("#donate_source").change(handle_donation_source_change);
  // need to do this so value is "C" at start
  $("#id_donation_type").val("C");

  // handle SUBMIT btn
  window.handle_submit_btn = function (event) {
    event.preventDefault();
    $('#error_msg').html("").addClass('hidden');

    // remove any errors, so can add just existing errors
    $(".form-group").removeClass("has-danger");
    
    var donation_amount = $("#donationAmt").val();
    // validate amount first - 1 to 999999.99 dollars 
    // TODO this is not ideal b/c full form is not validated
    if (!/^[1-9][0-9]{0,5}(\.[0-9]{1,2})?$/.test(donation_amount)) {
      $("#donationAmt").parents(".form-group").addClass("has-danger");
      $('#error_msg').html("please fix the red errors and resubmit").removeClass('hidden');
      return false;
    }

    var card_number = $("#card_number").val();
    if (!/^\d+$/.test(card_number)) {
      $("#card_number").parents(".form-group").addClass("has-danger");
      $('#error_msg').html("please fix the red errors and resubmit").removeClass('hidden');
      return false;
    }

    var expiration = $("#card_exp").val().split("/");
    if (expiration.length !== 2) {
      $("#card_exp").parents(".form-group").addClass("has-danger");
      $('#error_msg').html("please fix the red errors and resubmit").removeClass('hidden');
      return false;
    }

    var cvc = $("#card_cvc").val();
    if (!/^\d+$/.test(cvc)) {
      $("#card_cvc").parents(".form-group").addClass("has-danger");
      $('#error_msg').html("please fix the red errors and resubmit").removeClass('hidden');
      return false;
    }

    var ccData = {
      number: card_number,
      exp_month: expiration[0],
      exp_year: expiration[1],
      cvc: cvc
    };

    Stripe.setPublishableKey('pk_test_gP3ct0P3yGeiANNsWWJZDBhz'); // TODO: Switch to prod key

    Stripe.card.createToken(ccData, function (status, resp) {
      if (resp.error) {
        $('#error_msg').html(resp.error.message).removeClass('hidden');
      } else {
        var data = {};
        data.csrfmiddlewaretoken = $("#master_donate_form").find("input[name=csrfmiddlewaretoken]").val();
        data.token = resp.id;
        data.amount = donation_amount;
        makeAjax(data);
        return false;
      }
    });
    return false;
  };

  function makeAjax(data) {
    $.post("/make_donation", data, function (resp) {
      resp = JSON.parse(resp);
      if (resp.html) {
        $('#error_msg').html("please fix the red errors and resubmit").removeClass('hidden');
        $("#master_donate_div").html(resp.html);
      } else if (resp.payment_error) {
        $('#error_msg').html(resp.payment_error).removeClass('hidden');
      } else if (resp.redirect) {
        window.location.href = resp.redirect;
      }
    });
  }

  $("#master_donate_form").submit(window.handle_submit_btn);

});
