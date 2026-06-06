
  create or replace   view OLIST_PROJECT.PUBLIC.stg_orders
  
  
  
  
  as (
    select 
    order_id,
    customer_id,
    order_status,
    to_timestamp_ntz(order_purchase_timestamp/1000000000) as purchase_date,
    to_timestamp_ntz(order_approved_at/1000000000) as approval_date,
    to_timestamp_ntz(order_delivered_carrier_date/1000000000) as carrier_delivered_date,
    to_timestamp_ntz(order_estimated_delivery_date/1000000000) as estimated_delivery_date,
    to_timestamp_ntz(order_delivered_customer_date/1000000000) as customer_delivered_date,
from OLIST_PROJECT.PUBLIC.RAW_ORDERS
  );

