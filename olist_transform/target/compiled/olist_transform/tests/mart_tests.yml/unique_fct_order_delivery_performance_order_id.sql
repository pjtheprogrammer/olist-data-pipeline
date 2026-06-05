
    
    

select
    order_id as unique_field,
    count(*) as n_records

from OLIST_PROJECT.PUBLIC.fct_order_delivery_performance
where order_id is not null
group by order_id
having count(*) > 1


