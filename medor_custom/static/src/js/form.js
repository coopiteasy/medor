/*
 * Copyright 2019 Coop IT Easy SCRL fs
 *   Rémy Taymans <remy@coopiteasy.be>
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
 */
odoo.define('medor_custom.oe_user_form', function (require) {
    $(document).ready(function () {
        "use strict";
        var ajax = require('web.ajax');

        function hide_friend_address() {
            var deliv_method = $("input[name='delivery_method']:checked").val();

            if(deliv_method == "friend") {
                $(".title-friend").show('quick');
                $(".field-friend_name").show('quick');
                $(".field-friend_street").show('quick');
                $(".field-friend_zip_code").show('quick');
                $(".field-friend_city").show('quick');
                $(".field-friend_country_id").show('quick');
            } else {
                $(".title-friend").hide('quick');
                $(".field-friend_name").hide('quick');
                $(".field-friend_street").hide('quick');
                $(".field-friend_zip_code").hide('quick');
                $(".field-friend_city").hide('quick');
                $(".field-friend_country_id").hide('quick');
            }
        }

        $("input[name='delivery_method']").click(function(ev) {
            hide_friend_address();
        });

        $(".oe_delivery_form").each(function () {
            hide_friend_address();
        });

        $(".oe_delivery_method_info").each(function () {
            hide_friend_address();
        });
    });
});
