with customer_rfm_setup as (
select
    o.customer_id,
    max(o.approval_date) as most_recent_order,
    count(o.order_id) as order_frequency,
    sum(oi.price) as total_order_value
from {{ref('stg_orders')}} o
left join {{ref('stg_order_items')}} oi on o.order_id = oi.order_id
where o.order_status = 'delivered' and oi.price is not null
group by o.customer_id
),

customer_raw_rfm_records as (
select 
    c.customer_id,
    c.customer_state,
    c.customer_city,
    crfm.most_recent_order,
    crfm.order_frequency,
    crfm.total_order_value
from {{ref('stg_customers')}} c
left join customer_rfm_setup crfm on c.customer_id = crfm.customer_id
order by order_frequency, customer_id
)

select
    customer_id,
    6 - ntile(5) over (order by most_recent_order asc) as r_score,
    ntile(5) over (order by order_frequency asc) as f_score,
    ntile(5) over (order by total_order_value asc) as m_score,
    (r_score || f_score || m_score) as rfm_score
from customer_raw_rfm_records