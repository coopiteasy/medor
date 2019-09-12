odoo.define('medor_website_product_subscription.oe_user_form', function (require) {
    $(document).ready(function () {
        "use strict";
        var ajax = require('web.ajax');

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

        $("input[name='invoice_address']").click(function(ev) {
            toggle_invoice_address_fields();
        });

        $(".oe_user_form").each(function () {
            toggle_invoice_address_fields();
        });
    });
});
