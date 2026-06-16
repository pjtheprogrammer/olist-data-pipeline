select 
    o.order_id,
    count(oi.order_item_id) as no_of_items,
    sum(oi.price) as total_price,
    sum(oi.freight_value) as freight_cost,
    total_price + freight_cost as total_order_value
from {{ref('stg_orders')}} o
join {{ref('stg_order_items')}} oi on o.order_id = oi.order_id
group by o.order_id