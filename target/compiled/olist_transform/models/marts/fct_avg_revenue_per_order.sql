select 
    o.order_id,
    count(oi.order_item_id) as no_of_items
from OLIST_PROJECT.PUBLIC.stg_orders o
join OLIST_PROJECT.PUBLIC.stg_order_items oi on o.order_id = oi.order_id
group by o.order_id