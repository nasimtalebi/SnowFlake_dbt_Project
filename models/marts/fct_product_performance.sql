with order_items as (
    select * from {{ ref('stg_order_items') }}
),

products as (
    select * from {{ ref('stg_products') }}
),

product_summary as (
    select
        product_id,
        count(order_item_id) as total_units_sold
    from order_items
    group by 1
),

final as (
    select
        products.product_id,
        products.product_name,
        products.product_price,
        coalesce(product_summary.total_units_sold, 0) as total_units_sold
    from products
    left join product_summary on products.product_id = product_summary.product_id
)

select * from final