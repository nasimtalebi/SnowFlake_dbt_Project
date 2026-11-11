{{ config(materialized='table') }}

with date_dimension as (
    {{ dbt_date.get_date_dimension(
        start_date="2020-01-01",
        end_date="2026-12-31"
    ) }}
)

select * from date_dimension