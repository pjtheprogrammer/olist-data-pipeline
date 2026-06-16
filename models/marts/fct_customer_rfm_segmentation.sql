with customer_rfm as (
select
    o.customer_id,
    max(o.approval_date) as most_recent_order,
    count(o.order_id) as order_frequency,
    sum(oi.price) as total_order_value
from {{ref('stg_orders')}} o
left join {{ref('stg_order_items')}} oi on o.order_id = oi.order_id
where o.order_status = 'delivered'
group by o.customer_id
)

select 
    c.customer_id,
    c.customer_state,
    c.customer_city,
    crfm.most_recent_order,
    crfm.order_frequency,
    crfm.total_order_value
from {{ref('stg_customers')}} c
left join customer_rfm crfm on c.customer_id = crfm.customer_id
order by order_frequency, customer_id