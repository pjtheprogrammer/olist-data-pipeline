
    
    

select
    customer_id as unique_field,
    count(*) as n_records

from OLIST_PROJECT.PUBLIC.fct_order_delivery_performance
where customer_id is not null
group by customer_id
having count(*) > 1


