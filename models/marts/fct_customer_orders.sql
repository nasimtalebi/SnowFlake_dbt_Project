{{
    config(
        materialized='table'
    )
}}

with customers as (
    select * from {{ ref('stg_customers') }}
),

orders_payment as (
    select * from {{ ref('int_orders_payment') }}
),

customer_summary as (
    select
        customer_id,
        count(order_id) as total_orders,
        min(order_date) as first_order_date,
        max(order_date) as most_recent_order_date,
        sum(total_items) as total_items_purchased
    from orders_payment
    group by customer_id
),

final as (
    select
        customers.customer_id,
        -- استفاده از ستون customer_name که در استیجینگ تعریف شده بود
        customers.customer_name,
        customer_summary.total_orders,
        customer_summary.first_order_date,
        customer_summary.most_recent_order_date,
        coalesce(customer_summary.total_items_purchased, 0) as total_items_purchased
    from customers
    left join customer_summary on customers.customer_id = customer_summary.customer_id
)

select * from final