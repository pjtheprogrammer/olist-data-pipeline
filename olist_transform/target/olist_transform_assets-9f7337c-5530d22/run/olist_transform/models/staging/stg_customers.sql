
  create or replace   view OLIST_PROJECT.PUBLIC.stg_customers
  
  
  
  
  as (
    select 
    customer_id,
    customer_city,
    customer_state
from OLIST_PROJECT.PUBLIC.RAW_CUSTOMERS
  );

