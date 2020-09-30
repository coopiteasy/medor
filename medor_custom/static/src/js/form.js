/*
 * Copyright 2019 Coop IT Easy SCRL fs
 *   Rémy Taymans <remy@coopiteasy.be>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */
odoo.define('medor_custom.oe_user_form', function (require) {
    $(document).ready(function () {
        "use strict";
        var ajax = require('web.ajax');

        function toggle_friend_address_fields() {
            var deliv_method = $("input[name='delivery_method']:checked").val();

            if(deliv_method == "friend") {
                $(".title-friend").show('quick');
                $(".field-friend_name").show('quick');
                $("input[name='friend_name']").prop('required', true);
                $(".field-friend_street").show('quick');
                $("input[name='friend_street']").prop('required', true);
                $(".field-friend_zip_code").show('quick');
                $("input[name='friend_zip_code']").prop('required', true);
                $(".field-friend_city").show('quick');
                $("input[name='friend_city']").prop('required', true);
                $(".field-friend_country_id").show('quick');
            } else {
                $(".title-friend").hide('quick');
                $(".field-friend_name").hide('quick');
                $("input[name='friend_name']").prop('required', false);
                $(".field-friend_street").hide('quick');
                $("input[name='friend_street']").prop('required', false);
                $(".field-friend_zip_code").hide('quick');
                $("input[name='friend_zip_code']").prop('required', false);
                $(".field-friend_city").hide('quick');
                $("input[name='friend_city']").prop('required', false);
                $(".field-friend_country_id").hide('quick');
            }
        }
        
        function toggle_invoice_address_fields() {
            var inv_add = $("input[name='invoice_address']").is(":checked");

            if(inv_add) {
                $(".title-inv_address").show('quick');
                $(".field-inv_street").show('quick');
                $("input[name='inv_street']").prop('required', true);
                $(".field-inv_zip_code").show('quick');
                $("input[name='inv_zip_code']").prop('required', true);
                $(".field-inv_city").show('quick');
                $("input[name='inv_city']").prop('required', true);
                $(".field-inv_country_id").show('quick');
                $("input[name='inv_country_id']").prop('required', true);
            } else {
                $(".title-inv_address").hide('quick');
                $(".field-inv_street").hide('quick');
                $("input[name='inv_street']").prop('required', false);
                $(".field-inv_zip_code").hide('quick');
                $("input[name='inv_zip_code']").prop('required', false);
                $(".field-inv_city").hide('quick');
                $("input[name='inv_city']").prop('required', false);
                $(".field-inv_country_id").hide('quick');
                $("input[name='inv_country_id']").prop('required', false);
            }
        }


        $("input[name='delivery_method']").click(function(ev) {
            toggle_friend_address_fields();
        });

        $(".oe_delivery_form").each(function () {
            toggle_friend_address_fields();
        });
        
        $("input[name='invoice_address']").click(function(ev) {
            toggle_invoice_address_fields();
        });

        $(".oe_subscribe_form").each(function () {
            toggle_friend_address_fields();
        });

        $(".oe_delivery_method_info").each(function () {
            toggle_friend_address_fields();
        });
        
        $(".oe_user_form").each(function () {
            toggle_invoice_address_fields();
        });
    });
});
