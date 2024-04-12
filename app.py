"""
The base of this app was taken from the responsive sidebar with icons multi-page-app examples from the facultyai github.
I also added in storage as well so that we can keep track of data, values, etc across pages and sessions.
"""
import datetime
import json

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, callback, State
import plotly.express as px
import pandas as pd
import datetime as dt
import dash_daq as daq
from dash_bootstrap_templates import ThemeSwitchAIO

pd.set_option(
    'display.max_columns', 500
)

import assets.templates.olist_template as OLISTTHEME
import assets.templates.atbanalyticsgrp_default as ATBDEFAULTTHEME

# Setting the Default theme to be the custom created one for ATB Analytics Group
import plotly.io as pio
from os.path import exists

pio.templates.default = "atbAnalyticsGroupDefault"

import page_utilities.page_utilities as pg_utils

pg_utils = pg_utils.PageUtilities()

url_theme1 = ATBDEFAULTTHEME
url_theme2 = OLISTTHEME

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
ATBLOGO = './assets/logo/atb-analytics-group-logo.png'
SIDEBAR_STYLE = "./assets/css/SIDEBAR_STYLE.css"
MAIN_STYLE = './assets/css/main.css'
FONTS = './assets/css/fonts.css'

# DBC_CSS = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css")

# inital data that is going to populate the data store
customers = './data/OListEcomData/olist_customers_dataset.csv'
orders = './data/OListEcomData/olist_orders_dataset.csv'
order_items = './data/OListEcomData/olist_order_items_dataset.csv'
payments = './data/OListEcomData/olist_order_payments_dataset.csv'
products = './data/OListEcomData/olist_products_dataset.csv'
product_category = './data/OListEcomData/product_category_name_translation.csv'
sellers = './data/OListEcomData/olist_sellers_dataset.csv'
order_reviews = './data/OListEcomData/olist_order_reviews_dataset.csv'
geolocation = './data/OListEcomData/olist_geolocation_dataset.csv'
mql = './data/OListEcomData/olist_marketing_qualified_leads_dataset.csv'
closed_deals = './data/OListEcomData/olist_closed_deals_dataset.csv'

# creating dataframes
customers_df = pd.read_csv(customers)
orders_df = pd.read_csv(orders)
payments_df = pd.read_csv(payments)
products_df = pd.read_csv(products)
productCategory_df = pd.read_csv(product_category)
sellers_df = pd.read_csv(sellers)
orderReviews_df = pd.read_csv(order_reviews)
geolocation_df = pd.read_csv(geolocation)
orderItems_df = pd.read_csv(order_items)

# Combine these two together first before adding to main dataframe.
mql_df = pd.read_csv(mql)
closed_deals_df = pd.read_csv(closed_deals)

posCutoff = .10
priceMultiple = 3  # We are assuming that our price is marked up by PriceMultiple(3)X


# converting dates to integers for analysis
def get_date_int(df, col):
    print(type(df[col].loc[0]))
    year = df[col].dt.year
    month = df[col].dt.month
    day = df[col].dt.day
    return year, month, day


# Basic Stats for the dataframe that is being passed
def explore_df(df):
    date_cols = []

    if df is not None:
        print("***********************************", "Dataframe Columns",
              "**************************************************************\n\n\n")
        print(df.columns)
        print("*************************************************************************************************\n\n\n")
        for col in df.columns:
            print(col, " has this many unique amounts -", len(df[col].unique()))
            if "date" in col or "timestamp" in col or "approved_at" in col:
                date_cols.append(col)
                df[col] = pd.to_datetime(df[col])
        print("*************************************************************************************************\n\n\n")
        print("***********************************", "Dataframe EDA",
              "**************************************************************\n\n\n")
        print("Dataframe Shape : ", df.shape)
        print("Dataframe Head :\n\n", df.head())
        print("Dataframe info(memory_usage='deep') : ", df.info(memory_usage='deep'))
        print("Duplicate Values: ", df.duplicated().sum(), "\n\n")
        print("Has Missing Values: ", df.isnull().sum(), "\n\n")

        print("Data Description", df.describe())

        if "customer_unique_id" in df.columns and "payment_value" in df.columns:
            top_customers = df.groupby("customer_unique_id")["payment_value"].sum().reset_index().sort_values(
                "payment_value", ascending=False)
            top_customers.rename(columns={"payment_value": "LV"}, inplace=True)
            top_customers["% of Total Sales"] = (top_customers["LV"] / top_customers["LV"].sum()) * 100
            top_customers["Cum % of Total Sales"] = top_customers["% of Total Sales"].cumsum()

            most_percent_of_sales = top_customers[top_customers["% of Total Sales"] >= posCutoff]

            print("********************************\nOList Top Customers\n", top_customers,
                  "********************************\n", )
            print("********************************\nCustomers making up greater than", (posCutoff * 100),
                  "%of sales.\n",
                  most_percent_of_sales,
                  "********************************\n", )

            # TODO use this in analyis
            top_products = df.groupby(["product_category_name_english"]).agg(
                {'order_id': 'nunique', 'payment_value': 'sum'}).reset_index().sort_values(
                "payment_value", ascending=False)
            top_products.rename(columns={"payment_value": "LV"}, inplace=True)
            top_products["% of Total Sales"] = (top_products["LV"] /
                                                top_products["LV"].sum()) * 100
            top_products["Cum % of Total Sales"] = top_products["% of Total Sales"].cumsum()

            most_percent_of_sales_prod = top_products[
                top_products["% of Total Sales"] >= posCutoff]

            print("********************************\nOList Top Products\n", top_products,
                  "********************************\n", )
            print("********************************\nCustomers making up greater than", (posCutoff * 100),
                  "%of sales.\n",
                  most_percent_of_sales_prod,
                  "********************************\n", )

    else:
        print("Dataframe is empty, you have to pass a valid pandas dataframe for this to work.")


all_dfs = [
    customers_df, orders_df, orderItems_df, payments_df,
    products_df, productCategory_df, sellers_df,
    orderReviews_df, geolocation_df, mql_df, closed_deals_df
]

# Checking if the Combined data file exists.
data = exists('data/combined_olist_data.csv')

if data:
    df = pd.read_csv('data/combined_olist_data.csv')
    """
    Use this for Debugging purposes otherwise it slows down the program.
    """
    # explore_df(df)

    # TODO Move to the ELSE statement as well so that this is created even if
    # Olist full data file is not there. Or better yet, put these into functions,
    # and return them.
    """
    
    Customers Dataframe

    """

    """
        Date Cols 
        
        order_month_date, 
        order_delivered_customer_date,
        order_estimated_delivery_date,
        order_purchase_timestamp,
        shipping_limit_date,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date,
        first_contact_date, 
        won_date,

    """
    date_cols = [
        'order_month_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
        'order_purchase_timestamp',
        'shipping_limit_date',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date',
        'first_contact_date',
        'won_date',
    ]
    pg_utils.convert_to_datetime(df=df, col=date_cols)

    # df['order_month_date'] = pd.to_datetime(df['order_month_date'],
    #                                         errors='coerce',
    #                                         infer_datetime_format=True)
    #
    # df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'],
    #                                                      errors='coerce',
    #                                                      infer_datetime_format=True)
    # df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"],
    #                                                      errors='coerce',
    #                                                      infer_datetime_format=True)
    # df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"],
    #                                                 errors='coerce',
    #                                                 infer_datetime_format=True)
    #
    # df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"],
    #                                            errors='coerce',
    #                                            infer_datetime_format=True)
    #
    # df["order_delivered_carrier_date"] = pd.to_datetime(df["order_delivered_carrier_date"],
    #                                                     errors='coerce',
    #                                                     infer_datetime_format=True)
    #
    # df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"],
    #                                                      errors='coerce',
    #                                                      infer_datetime_format=True)
    #
    # df["order_estimated_delivery_date"] = pd.to_datetime(df["order_estimated_delivery_date"],
    #                                                      errors='coerce',
    #                                                      infer_datetime_format=True)
    #
    # df["first_contact_date"] = pd.to_datetime(df["first_contact_date"],
    #                                           errors='coerce',
    #                                           infer_datetime_format=True)
    #
    # df["won_date"] = pd.to_datetime(df["won_date"],
    #                                 errors='coerce',
    #                                 infer_datetime_format=True)

    print("This dataset takes up ", df.info(memory_usage='deep'))

    # create month by month bar graph for customers
    customers_df = df[['customer_unique_id', 'zip_code', 'order_month_date', 'payment_value', 'order_id', 'profit',
                       'order_delivered_customer_date', 'order_estimated_delivery_date',
                       'order_purchase_timestamp', 'order_item_id', 'freight_value',
                       'order_status', 'price', 'review_score', 'cohort_month', 'cohort_index']]

    # Creating new columns for analysis by select all rows by this column or list of columns
    customers_df['customer_count'] = customers_df.loc[:, 'customer_unique_id']
    customers_df['customer_revenue'] = customers_df.loc[:, 'payment_value']
    customers_df['order_id_count'] = customers_df.loc[:, 'order_id']
    customers_df['tot_unique_customers'] = customers_df.loc[:, 'customer_unique_id']
    customers_df['review_count'] = customers_df.loc[:, 'review_score']
    customers_df.rename(
        columns={
            "order_delivered_customer_date": "customer_received_date",
            "order_estimated_delivery_date": "est_customer_receive_date",
            "order_purchase_timestamp": "order_purchased",
        },
        inplace=True,
    )

    # customers_df['customer_received_date'] = pd.to_datetime(customers_df['customer_received_date'], errors='coerce',
    #                                                         infer_datetime_format=True)
    # customers_df["est_customer_receive_date"] = pd.to_datetime(customers_df["est_customer_receive_date"],
    #                                                            errors='coerce',
    #                                                            infer_datetime_format=True)
    # customers_df["order_purchased"] = pd.to_datetime(customers_df["order_purchased"],
    #                                                  errors='coerce',
    #                                                  infer_datetime_format=True)

    print("Data type for the Date Column is ", type(customers_df['customer_received_date'][0]),
          type(customers_df['est_customer_receive_date'][0]), type(customers_df['order_purchased'][0]))

    customers_df['order2cus_days'] = (customers_df['customer_received_date'] - customers_df[
        'order_purchased']).dt.days

    # if you received the order early the days would be negative. this is a good thing is this case.
    customers_df['on_time_days'] = (customers_df['est_customer_receive_date'] - customers_df[
        'customer_received_date']).dt.days

    # TODO check if filling these with np.mean or np.sum has any effciency effects.
    customers_by_month = customers_df.groupby(['order_month_date']).agg(
        {
            'customer_count': 'count',
            'tot_unique_customers': 'nunique',
            'customer_revenue': 'sum',
            'profit': 'sum',
            'freight_value': 'sum',
            'order_id': 'nunique',
            'order_id_count': 'count',
            'order_item_id': 'count',
            'order2cus_days': 'mean',
            'on_time_days': 'mean',
            'review_score': 'mean',
            'review_count': 'count',
        }
    ).reset_index()
    customers_by_month['purchase_frequency'] = customers_by_month['order_id_count'] / customers_by_month[
        'tot_unique_customers']
    customers_by_month['revenue_per_customer'] = customers_by_month['customer_revenue'] / customers_by_month[
        'customer_count']
    customers_by_month['profit_per_customer'] = customers_by_month['profit'] / customers_by_month[
        'tot_unique_customers']
    customers_by_month['avg_order_value'] = customers_by_month['customer_revenue'] / customers_by_month[
        'order_id']
    customers_by_month['customer_value'] = (customers_by_month['avg_order_value'] / customers_by_month[
        'purchase_frequency']) / 1  # Since we do not compute churn rate, we will us 1.

    # customers_by_month = json.dumps(customers_by_month)

    print("This dataset takes up ", customers_by_month.info(memory_usage='deep'))

    """
    
    Merchants by Month DF
    
    """
    merchants_df = df[
        ['order_month_date', 'order_id', 'seller_id', 'zip_code_y', 'product_category_name_english',
         'order_item_id', 'payment_value', 'freight_value', 'review_score',
         'shipping_limit_date', 'order_delivered_carrier_date', 'order_delivered_customer_date',
         'order_estimated_delivery_date', 'order_status', 'business_segment', 'business_type', 'profit',
         'first_contact_date', 'landing_page_id', 'origin', 'sdr_id', 'sr_id', 'mql_id',
         'won_date', 'lead_type', 'lead_behaviour_profile', 'customer_unique_id'
         ]
    ]

    merchants_df['avg_freight_value'] = merchants_df['freight_value']

    # Days to win seller's business and have them list on the  OList.
    merchants_df['days_to_close_seller'] = (merchants_df['won_date'] - merchants_df[
        'first_contact_date']).dt.days

    merchants_df.rename(
        columns={
            "shipping_limit_date": "ship_to_wh_date",
            "order_delivered_carrier_date": "wh_received_date",
            "order_delivered_customer_date": "customer_received_date",
            "order_estimated_delivery_date": "est_customer_receive_date",
        },
        inplace=True)

    # Finding out how long it took the merchant to ship to Olist Warehouse.
    # merchant_to_wh_df = merchants_df[
    #     ['seller_id', 'order_month_date', 'ship_to_wh_date', 'wh_received_date', 'ship_days']]
    # merchants_df['ship_to_wh_date'] = pd.to_datetime(merchants_df['ship_to_wh_date'], errors='coerce',
    #                                                  infer_datetime_format=True)
    # merchants_df['wh_received_date'] = pd.to_datetime(merchants_df['wh_received_date'], errors='coerce',
    #                                                   infer_datetime_format=True)

    # Getting Days between when the Order was shipped from the merchant to Olist Warehouse/Carrier
    # and then from the time that the customer ordered it to delivery.
    merchants_df['ship_days'] = (merchants_df['wh_received_date'] - merchants_df['ship_to_wh_date']).dt.days

    merchants_df['tot_ship_days'] = merchants_df['ship_days']
    merchants_df['avg_ship_days'] = merchants_df['ship_days']
    merchants_df['avg_review_score'] = merchants_df['review_score']

    merchants_by_month = merchants_df.groupby(['order_month_date']).agg(
        {
            'seller_id': 'nunique',
            'order_item_id': 'sum',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'avg_freight_value': 'mean',
            'tot_ship_days': 'sum',
            'avg_ship_days': 'mean',
            'review_score': 'count',
            'avg_review_score': 'mean',
            'profit': 'sum',
            'days_to_close_seller': 'mean',
            'customer_unique_id': 'nunique',
        }
    ).reset_index()

    print("This dataset takes up ", merchants_by_month.info(memory_usage='deep'))

    """
    
    Top_n_by_ df's 
    
    """
    top_n_df = df[['order_month_date', 'product_category_name_english',
                   'payment_value', 'freight_value', 'customer_unique_id',
                   'seller_id', 'profit', 'order_item_id', 'shipping_limit_date',
                   'order_delivered_customer_date',
                   ]]

    top_n_df_by_product = top_n_df.groupby('product_category_name_english').agg(
        {
            # 'product_category_name_english': 'first',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'customer_unique_id': 'nunique',
            'seller_id': 'nunique',
            'profit': 'sum',
            'order_item_id': 'sum',
        }
    ).reset_index()

    print("This dataset takes up ", top_n_df_by_product.info(memory_usage='deep'))

    top_n_df_by_month = top_n_df.groupby('order_month_date').agg(
        {
            # 'product_category_name_english': 'first',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'customer_unique_id': 'nunique',
            'seller_id': 'nunique',
            'profit': 'sum',
            'order_item_id': 'sum'
        }
    ).reset_index()

    print("This dataset takes up ", top_n_df_by_month.info(memory_usage='deep'))

    top_n_df_by_customer = top_n_df.groupby('customer_unique_id').agg(
        {
            # 'product_category_name_english': 'first',
            'payment_value': 'sum',
            'freight_value': 'sum',
            # 'customer_unique_id': 'nunique',
            'seller_id': 'nunique',
            'profit': 'sum',
            'order_item_id': 'sum',
        }
    ).reset_index()

    print("This dataset takes up ", top_n_df_by_customer.info(memory_usage='deep'))

    top_n_df_by_seller = top_n_df.groupby('seller_id').agg(
        {
            # 'product_category_name_english': 'first',
            'payment_value': 'sum',
            'freight_value': 'sum',
            'customer_unique_id': 'nunique',
            # 'seller_id': 'nunique',
            'profit': 'sum',
            'order_item_id': 'sum',
        }
    ).reset_index()

    print("This dataset takes up ", top_n_df_by_customer.info(memory_usage='deep'))
    """
    
    Seller/Customer Data to be pivoted by product_category_name_english and order month 
    
    """
    # Use this for creating interactivity and drill-down analysis
    seller_cust_pivot_df = df[['order_month_date', 'customer_unique_id', 'seller_id',
                               'product_category_name_english', 'payment_value', 'freight_value',
                               'order_item_id', 'profit', 'payment_type', 'review_score'
                               ]]
    print("This dataset takes up ", seller_cust_pivot_df.info(memory_usage='deep'))
    """

    Seller/Customer Data to be pivoted by product_category_name_english and order month 

    """
    # Use this for creating interactivity and drill-down analysis
    seller_cust_mapping_df = df[['order_month_date', 'customer_unique_id', 'seller_id',
                                 'product_category_name_english', 'payment_value', 'freight_value',
                                 'order_item_id', 'profit', 'payment_type', 'zip_code', 'zip_code_y', 'review_score'
                                 ]]
    print("This dataset takes up ", seller_cust_pivot_df.info(memory_usage='deep'))


else:
    """
    Use this for Debugging purposes otherwise it slows down the program. Or spit it out in a Log file. 
    """
    # all_dfs_count = len(all_dfs)
    # count = 0
    # for df in all_dfs:
    #     if count <= all_dfs_count:
    #         print("********************************\n", "Dataframe ", count, "********************************\n"),
    #         count += 1
    #         explore_df(df)
    #         print(
    #             "*************************************************************************************************\n\n\n")

    # changing column names before merging
    customers_df.rename(columns={"customer_zip_code_prefix": "zip_code"}, inplace=True)
    sellers_df.rename(columns={"seller_zip_code_prefix": "zip_code"}, inplace=True)
    geolocation_df.rename(columns={"geolocation_zip_code_prefix": "zip_code"}, inplace=True)

    # This way you can break down the larger csv, and add the necessary geography to those columns only. But it really
    # should be in a db instead of flat files.
    geolocation_df = geolocation_df.groupby('zip_code', as_index=False).agg(
        {'geolocation_lat': 'first', 'geolocation_lng': 'first', 'geolocation_city': 'first',
         'geolocation_state': 'first'})

    # merging the order, customer, and payments dataframes into one dataframe
    df = orders_df.merge(customers_df, on='customer_id').merge(orderItems_df, on="order_id").merge(
        products_df, on="product_id").merge(
        productCategory_df, on="product_category_name").merge(
        payments_df, on="order_id").merge(sellers_df, on="seller_id").merge(
        orderReviews_df, on="order_id")

    # Creating the Marketing DataFrame separetely so that it can be joined with the Seller's Geo DF later since
    # OList Marketing is targeting having sellers sign up for their platform.

    # Using the mql_df as the base since it has more data and we can look at all of the marketing efforts
    # and not just the deals that closed.
    if not exists('data/suppliers_geo_data.csv') or not exists('data/combined_olist_data.csv'):
        marketing_df = mql_df.merge(closed_deals_df, on='mql_id', how='left')

        # Adding additional column that will be used in our analysis and saved in the combined dataframe.

        marketing_df['time_to_close'] = pd.to_datetime(marketing_df['won_date'], errors='coerce',
                                                       infer_datetime_format=True) - pd.to_datetime(
            marketing_df['first_contact_date'], errors='coerce', infer_datetime_format=True)
        # marketing_df['time_to_close'].fillna(0)

    # making a customers_geo_df and a suppliers_geo_df to be saved separately
    if exists('data/customers_geo_data.csv'):
        pass
    else:
        customers_geo_df = customers_df.merge(geolocation_df, on='zip_code')
        print(customers_geo_df.head(5))
        customers_geo_df = customers_geo_df.groupby('customer_unique_id', as_index=False).agg({
            'zip_code': 'first',
            'customer_city': 'first',
            'customer_state': 'first',
            'geolocation_lat': 'first',
            'geolocation_lng': 'first',
            'geolocation_city': 'first',
            'geolocation_state': 'first'
        })
        customers_geo_df.to_csv('./data/customers_geo_data.csv', index=False)

    if exists('data/suppliers_geo_data.csv'):
        pass
    else:
        if "seller_zip_code_prefix" in sellers_df.columns:
            sellers_df.rename(columns={"seller_zip_code_prefix": "zip_code"}, inplace=True)

        suppliers_geo_df = sellers_df.merge(geolocation_df, on='zip_code')

        suppliers_geo_df = suppliers_geo_df.groupby('seller_id', as_index=False).agg({
            'zip_code': 'first',
            'seller_city': 'first',
            'seller_state': 'first',
            'geolocation_lat': 'first',
            'geolocation_lng': 'first',
            'geolocation_city': 'first',
            'geolocation_state': 'first'
        })

        suppliers_geo_df = suppliers_geo_df.merge(marketing_df, on='seller_id', how='left')
        print(suppliers_geo_df.head(5))
        suppliers_geo_df.to_csv('./data/suppliers_geo_data.csv', index=False)

    # explore_df(df)

    # dropping columns we do not need to save memory
    # Columns to be removed
    """
    product_category_name                 0
    product_name_lenght                   0
    product_description_lenght            0
    product_photos_qty                    0
    product_weight_g                      1
    product_length_cm                     1
    product_height_cm                     1
    product_width_cm                      1
    review_comment_title             101808
    review_comment_message            66703
    
    """

    colsToDrop = ['product_category_name',
                  'product_name_lenght',
                  'product_description_lenght',
                  'product_photos_qty',
                  'product_weight_g',
                  'product_length_cm',
                  'product_height_cm',
                  'product_width_cm',
                  'review_comment_title',
                  'review_comment_message'
                  ]
    df.drop(columns=colsToDrop, inplace=True)
    if not exists('data/suppliers_geo_data.csv') or not exists('data/combined_olist_data.csv'):
        marketing_df = mql_df.merge(closed_deals_df, on='mql_id', how='left')
        df = df.merge(marketing_df, on='seller_id', how='left')

    # Adding additional columns to the dataframe
    df['order_month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.month
    df['order_year'] = pd.to_datetime(df['order_purchase_timestamp']).dt.year
    print("Checking Datatype for Order Month: ", type(df['order_month'].loc[0]))
    print("Checking Datatype for Order Year: ", type(df['order_year'].loc[0]))

    # Creating the order_month_date which is just grouping the orders into MM01YYYY format.
    df['order_month_date'] = pd.to_datetime(df['order_purchase_timestamp']).dt.date
    print("Checking Datatype for Order Month Date: ", type(df['order_month_date'].loc[0]))

    df['order_month_date'] = pd.to_datetime(df['order_month_date'], errors='coerce', infer_datetime_format=True).apply(
        lambda x: x.replace(day=1))
    print(type(df['order_month_date'].loc[0]))
    df['most_recent_order'] = df.groupby('customer_id')['order_month_date'].transform('max')
    df['most_recent_order'] = pd.to_datetime(df['most_recent_order'], errors='coerce', infer_datetime_format=True)
    print("Checking Datatype for Most Recent Order: ", type(df['most_recent_order'].loc[0]))

    # Cohort month gets the first month that a customer ordered from Olist.
    cohort_df = df.groupby('customer_unique_id')['order_month_date']
    df['cohort_month'] = cohort_df.transform('min')
    print("Checking Datatype for Cohort Month: ", type(df['cohort_month'].loc[0]))

    print(df.head(25))

    # Date Math and Conversions
    invoice_year, invoice_month, _ = get_date_int(df, 'order_month_date')
    cohort_year, cohort_month, _ = get_date_int(df, 'cohort_month')
    years_diff = invoice_year - cohort_year
    month_diff = invoice_month - cohort_month
    df['cohort_index'] = years_diff * 12 + month_diff + 1  # Forces the index to start at 1 instead of 0.

    # These are assumptions that are being made about the data
    df['prod_cost'] = df['price'] / priceMultiple  # cost to product the product not incl shipping.
    df['tot_price'] = df['price'] + df['freight_value']
    # df['profit'] = df['price'] - df['freight_value']
    df['profit'] = df['price'] - df['prod_cost']
    df['profit_margin'] = df['profit'] / df['price']
    df['freight_percentage'] = df['freight_value'] / df['tot_price']

    print(df['order_status'].value_counts())
    print(df['order_month'].value_counts())
    print(df['order_year'].value_counts())
    print(df['product_category_name_english'].value_counts())

    # Really is the Customer Zip , seller zipcode is listed as zip_code_y
    if 'zip_code_x' in df.columns:
        df.rename(columns={"'zip_code_x'": "zip_code"}, inplace=True)

    df.to_csv('./data/combined_olist_data.csv', index=False)

# Prepare the data to be saved into the data-store.
# accepts dict | list | number | string | boolean
# Turning dataframe into records to be stored.
# df = df.to_dict('records')
# df = df.to_dict('records')


# Might be better to save and read in as a csv when really needed.
customers_df = customers_df.to_csv('./data/customers_df.csv', index=False)
merchants_df = merchants_df.to_csv('./data/merchants_df.csv', index=False)

# These datasets are small enough to be saved in the data storage and power a lot of the
# KPI Viz's

mql_df = pd.read_csv('./data/OlistEcomData/olist_marketing_qualified_leads_dataset.csv')
closed_df = pd.read_csv('./data/OlistEcomData/olist_closed_deals_dataset.csv')

customers_by_month = customers_by_month.to_json(orient='records', date_format='iso')
merchants_by_month = merchants_by_month.to_json(orient='records', date_format='iso')
top_n_df_by_product = top_n_df_by_product.to_json(orient='records', date_format='iso')
top_n_df_by_customer = top_n_df_by_customer.to_json(orient='records', date_format='iso')
top_n_df_by_month = top_n_df_by_month.to_json(orient='records', date_format='iso')
top_n_df_by_seller = top_n_df_by_seller.to_json(orient='records', date_format='iso')
seller_cust_pivot_df = seller_cust_pivot_df.to_json(orient='records', date_format='iso')
seller_cust_mapping_df = seller_cust_mapping_df.to_json(orient='records', date_format='iso')
marketing_mql = mql_df.to_json(orient='records', date_format='iso')
marketing_closed_deals = closed_df.to_json(orient='records', date_format='iso')
# sales_by_month = merchants_by_month.to_dict('records')
# merchants_by_month = merchants_by_month.to_dict('records')

datasets = {
    # 'all': df,
    # 'customers_df': customers_df,
    # 'merchants_df': merchants_df,
    'customer_by_month_df': customers_by_month,
    'merchants_by_month_df': merchants_by_month,
    'top_n': {
        'product': top_n_df_by_product,
        'month': top_n_df_by_month,
        'customer': top_n_df_by_customer,
        'seller': top_n_df_by_seller,
    },
    'seller_cust_pivot_df': seller_cust_pivot_df,
    'marketing_mql': marketing_mql,
    'marketing_closed_deals': marketing_closed_deals,
}
datasets = json.dumps(datasets)
# df = df[:70000].to_dict('records')
print("df converted to dictionary and is being saved into storage...")

# Setting up the Application
app = dash.Dash(__name__,
                use_pages=True,
                external_stylesheets=[
                    dbc.themes.FLATLY,
                    # DBC_CSS,
                    # dbc.icons.FONT_AWESOME,
                    FONTS,
                    SIDEBAR_STYLE,
                    MAIN_STYLE,
                ],
                meta_tags=[
                    {
                        "name": "viewport",
                        "content": "width=device-width, initial-scale=1"
                    }
                ],
                title="OList - Sales Analytics App - by ATB Analytics Group",
                update_title="Data is being collected, and organized for your viewing pleasure. Please Wait....",
                assets_folder='./assets/',

                )

sidebar_header = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Link([
                    html.Img(id='logoImg', src=ATBLOGO, alt="ATB Analytics Group Logo")
                ], href="https://www.atb-analytics-group.webflow.io"),
            ],
            width=2,
        ),

        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
        dbc.Col([
            html.Br(),
            html.H2(
                id='sidebar-menu-name',
                children=["Home"],
                # className="display-5",
            ),
        ],
            width=12,
        ),
    ]
)

# theme_switch = ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2], )

sidebar = html.Div(
    [
        html.Br(),
        sidebar_header,
        html.Br(),
        html.Div(
            id="blurb",
            children=[
                # width: 3rem ensures the logo is the exact width of the
                # collapsed sidebar (accounting for padding)
                # html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                # html.H2("Sidebar", ),
                html.P("This is a blurb that is about, the menu items.")
            ],

        ),
        html.Hr(),
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink(f"{page['name']} ", href=page["relative_path"]) for page in
                    dash.page_registry.values() if page["module"] != "pages.not_found_404"

                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
        # theme_switch,
    ],
    id="sidebar",
)

# Container to hold the pages.
content = dbc.Col(
    id="page-content",
    children=[dash.page_container],
    width="auto",
)

# Application Layout.
app.layout = dbc.Container(
    children=[
        # json.dumps(datasets)
        dcc.Loading(dcc.Store('data-store', data=datasets), fullscreen=True, type="dot", color="AQUAMARINE"),
        # dcc.Loading(dcc.Store('data-store', data=df), fullscreen=True, type="dot", color="AQUAMARINE"),
        dcc.Store('data-value-store', data=None),
        sidebar,
        content
    ],
    fluid=True,
    # className="dbc"
)


@callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@callback(
    Output('sidebar-menu-name', 'children'),
    Output('blurb', 'children'),
    Input('data-store', 'data'),
    Input('page-content', 'children'),
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
)
def update_sidebar_menu(data, page_content):
    # print(page_content)
    pathname = page_content[0]['props']['children'][0]['props']['pathname']
    if pathname == '/merchants-analysis':
        menu_name = "Merchant Analysis"
        blurb = "This is the Merchant Analysis page, where we have broken down things like average shipping cost, " \
                "who are top merchants are, where their located, etc."
    elif pathname == '/customer-analysis':
        menu_name = "Customer Analysis "
        blurb = """
                This is the Customer Analysis, where we have broken down things like the average order value, 
                RFM, Customer Segmentation, and more.
            """
    elif pathname == '/contact':
        menu_name = "Contact ATB Analytics Group"
        blurb = """
                        Ready to do more with your data? 
                        Looking to have something similar created for your business.
                        Get in touch with us today.
                    """
    elif pathname == '/about':
        menu_name = "About"
        blurb = """
This is a little history on OList and the Economy of Brazil at the time that this dataset was published. 
                        """
    elif pathname == '/marketing-analysis':
        menu_name = "Marketing Analysis"
        blurb = """
                           This is the Marketing Campaign Data that was provided by OList.
                       """
    else:
        menu_name = "Executive Analytics Suite"
        blurb = "This is an application to visualize OList data from 2016-2018ish timeframe," \
                "and provide a quick look into their business at that time."
    return menu_name, blurb


if __name__ == '__main__':
    app.run_server(
        debug=True
    )
