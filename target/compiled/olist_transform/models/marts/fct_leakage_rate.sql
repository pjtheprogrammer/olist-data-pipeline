select * from OLIST_PROJECT.PUBLIC.stg_orders
where approval_date is not null
and order_status = 'canceled'
or order_status = 'unavailable'