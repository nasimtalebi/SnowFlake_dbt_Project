import snowflake.connector
import pandas as pd
from snowflake.connector.pandas_tools import write_pandas

# 1. Connect to Snowflake
conn = snowflake.connector.connect(
    account='zrrdpmj-ll39261',
    user='NasimTalebi',
    password='Nasim0310235251',
    warehouse='COMPUTE_WH',
    database='DEMO_DB',
    schema='ANALYTICS'
)

# 2. Fetch data from the marts layer
query = "SELECT * FROM DEMO_DB.ANALYTICS.customers"
df = pd.read_sql(query, conn)

# Standardize column names to uppercase for reliable matching
df.columns = [col.upper() for col in df.columns]
print("Available columns:", df.columns.tolist())

# 3. Python Segmentation Logic
def segment_customer(row):
    # Check for order count column dynamically
    orders_count = row.get('NUMBER_OF_ORDERS', row.get('TOTAL_ORDERS', 0))
    if orders_count >= 5:
        return 'VIP'
    elif orders_count >= 2:
        return 'Regular'
    else:
        return 'New / Low-Value'

df['CUSTOMER_SEGMENT'] = df.apply(segment_customer, axis=1)

# 4. Display sample output in terminal
print("\n--- Segmented Sample Data ---")
sample_cols = [col for col in ['CUSTOMER_ID', 'NUMBER_OF_ORDERS', 'TOTAL_ORDERS', 'CUSTOMER_SEGMENT'] if col in df.columns]
print(df[sample_cols].head())

# 5. Create table if not exists and write data using write_pandas
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS DEMO_DB.ANALYTICS.CUSTOMER_SEGMENTS_PYTHON (
        CUSTOMER_ID VARCHAR,
        CUSTOMER_NAME VARCHAR,
        COUNT_LIFETIME_ORDERS NUMBER,
        FIRST_ORDER_DATE DATE,
        LAST_ORDER_DATE DATE,
        LIFETIME_SPEND_PRETAX FLOAT,
        LIFETIME_TAX_PAID FLOAT,
        LIFETIME_SPEND FLOAT,
        CUSTOMER_TYPE VARCHAR,
        CUSTOMER_SEGMENT VARCHAR
    )
""")
cursor.close()

# Now write data into the table
write_pandas(conn, df, 'CUSTOMER_SEGMENTS_PYTHON')

conn.close()
print("\nData successfully processed and uploaded to Snowflake table: CUSTOMER_SEGMENTS_PYTHON!")