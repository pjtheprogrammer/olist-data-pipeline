
  create or replace   view OLIST_PROJECT.PUBLIC.stg_order_items
  
  
  
  
  as (
    select * from OLIST_PROJECT.PUBLIC.RAW_ORDER_ITEMS
  );

