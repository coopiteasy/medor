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
set start_date = data_table.payment_date
from (
         select pso.id as subscription_id,
                pso.name,
                pso.start_date,
                psr.payment_date
         from product_subscription_object pso
                  join product_subscription_request psr
                       on pso.id = psr.subscription
     ) data_table
where id = subscription_id
;

-- update start date for historical users
update product_subscription_object
set start_date = data_table.payment_date
from (
    select distinct on (pso.subscriber, pso.id)
           pso.subscriber as subscriber_id,
           pso.id as subscription_id,
           pso.name as subscription_name,
           psr.name,
           pso.start_date,
           psr.payment_date
    from product_subscription_object pso
    join product_subscription_request psr on pso.subscriber = psr.subscriber
    where pso.state in ('ongoing', 'renew')
       and psr.state = 'paid'
--        and pso.subscriber = 7525
    order by pso.subscriber, pso.id, psr.payment_date desc
     ) data_table
where id = subscription_id
  and product_subscription_object.state = 'ongoing'
