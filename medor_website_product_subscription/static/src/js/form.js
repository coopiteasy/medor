odoo.define('medor_website_product_subscription.oe_user_form', function (require) {
    $(document).ready(function () {
        "use strict";
        var ajax = require('web.ajax');

        $(".oe_user_form").each(function () {

            function hide_invoice_address() {
                var inv_add = $("input[name='invoice_address']:checked").val();

                if(inv_add == "on") {
                    $(".title-inv_address").show('quick');
                    $(".field-inv_street").show('quick');
                    $(".field-inv_zip_code").show('quick');
                    $(".field-inv_city").show('quick');
                    $(".field-inv_country_id").show('quick');
                } else {
                    $(".title-inv_address").hide('quick');
                    $(".field-inv_street").hide('quick');
                    $(".field-inv_zip_code").hide('quick');
                    $(".field-inv_city").hide('quick');
                    $(".field-inv_country_id").hide('quick');
                }
            }
            hide_invoice_address();

            $("input[name='invoice_address']").click(function(ev) {
                hide_invoice_address();
            });
        });
    });
});
