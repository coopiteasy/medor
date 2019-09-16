select
       r.id, r.name,
       pst.id, pst.name,
       pso.id, pso.name,
       r.subscription_date
from product_subscription_request r
  join product_subscription_object pso on r.subscription = pso.id
  join product_subscription_template pst on r.subscription_template = pst.id
where r.state = 'paid'
;

UPDATE product_subscription_object
SET template = data_table.template_id,
    request = data_table.request_id
FROM (
    select
       request.id as request_id, request.name as request_name,
       pst.id as template_id, pst.name as template_name,
       pso.id as subscription_id, pso.name as subscription_name
    from product_subscription_request request
      join product_subscription_object pso on request.subscription = pso.id
      join product_subscription_template pst on request.subscription_template = pst.id
--     where request.state = 'paid'
    ) data_table
WHERE
    id = data_table.subscription_id
;

 -- MAIS des souscriptions (historique? renouvelées?) n'ont pas le lien vers la request.

select id, name from product_subscription_template;

update product_subscription_object set template = 2 where template is null;


select id, name, template, request
from product_subscription_object
where state = 'ongoing'
limit 100
;

-- update start date for historical users
update product_subscription_object
set start_date = data_table.subscription_date
from (
         select pso.id as subscription_id,
                pso.name,
                pso.start_date,
                psr.subscription_date
         from product_subscription_object pso
                  join product_subscription_request psr
                       on pso.id = psr.subscription
     ) data_table
where id = subscription_id
;
