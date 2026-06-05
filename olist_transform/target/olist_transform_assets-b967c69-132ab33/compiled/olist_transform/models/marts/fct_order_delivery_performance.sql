select 
    *,
    datediff('day', purchase_date, estimated_delivery_date) as estimated_delivery_time,
    datediff('day', purchase_date, customer_delivered_date) as actual_delivery_time,
    estimated_delivery_time - actual_delivery_time as estimated_vs_actual,
    case
        when estimated_vs_actual > 0 then 'early'
        when estimated_vs_actual < 0 then 'late'
    end as punctuality_performance,
    datediff('day', carrier_delivered_date, customer_delivered_date) as days_in_carrier_transit
from OLIST_PROJECT.PUBLIC.stg_orders