with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select * from {{ ref('stg_order_items') }}
),

item_totals as (
    select
        order_id,
        count(order_item_id) as total_items
    from order_items
    group by order_id
),

final as (
    select
        orders.order_id,
        orders.customer_id,
        orders.order_date,
        coalesce(item_totals.total_items, 0) as total_items
    from orders
    left join item_totals on orders.order_id = item_totals.order_id
)

select * from final