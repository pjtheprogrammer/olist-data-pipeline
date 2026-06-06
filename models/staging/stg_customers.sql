select 
    customer_id,
    customer_city,
    customer_state
from {{source('olist_raw', 'raw_customers')}}