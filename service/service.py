from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import psycopg2, requests, json, tls_client,os,csv

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app = Flask(__name__)

conn = psycopg2.connect(
        host="localhost",
        database="invoice_manager",
        user="postgres",
        password="postgres"
        )

####################################################

@app.route('/login_user', methods=["GET"])
@cross_origin()
def login():

    license_key = request.headers["key"]

    sql_query = "select * from user_list where user_list.license_key = '" +  str(license_key)  + "'"

    with conn.cursor() as c:
        c.execute(sql_query)
        res = c.fetchall()

    return jsonify({"data": res})

@app.route('/get_user_data')
@cross_origin()
def get_user_data():

    user_id = request.headers["user_id"]

    user_data = {
    "user_settings": {},
    "user_alias_sales": [],
    "user_stockx_sales": []
    }

    settings_query = """
    select
        user_settings.user_id,
        user_settings.sevdesk_api_key,
        user_settings.sevdesk_creator_id,
        user_settings.sevdesk_alias_id,
        user_settings.sevdesk_stockx_id,
        user_settings.sort_invoice_by_sale_date,
        user_settings.alias_email,
        user_settings.alias_password
    from user_settings
        where user_settings.user_id = %s
    """

    with conn.cursor() as c:
        c.execute(settings_query,(user_id,))
        try:
            result = c.fetchall()[0]
            user_data["user_settings"] = {
            "settings_user_id": result[0],
            "sevdesk_api_key": result[1],
            "sevdesk_creator_id": result[2],
            "sevdesk_alias_id": result[3],
            "sevdesk_stockx_id": result[4],
            "sort_invoice_by_sale_date": result[5],
            "alias_email": result[6],
            "alias_password": result[7]
            }
        except IndexError as e:
            user_data["user_settings"] = []
        conn.commit()

    alias_sales_query = """
    select
        alias_sales.date,
        alias_sales.order,
        alias_sales.sku,
        alias_sales.product_name,
        alias_sales.product_size,
        alias_sales.tracking,
        alias_sales.sale_price_usd,
        alias_sales.provision,
        alias_sales.sales_fee,
        alias_sales.payout_fee,
        alias_sales.payout_usd,
        alias_sales.exchange_rate,
        alias_sales.payout_eur
    from alias_sales
        where alias_sales.user_id = %s
    """

    with conn.cursor() as c:
        c.execute(alias_sales_query,(user_id,))
        try:
            sales = c.fetchall()

            for element in sales:
                user_data["user_alias_sales"].append({
                "date": element[0],
                "order": element[1],
                "sku": element[2],
                "product_name": element[3],
                "product_size": element[4],
                "tracking": element[5],
                "sale_price_usd": element[6],
                "provision": element[7],
                "sales_fee": element[8],
                "payout_fee": element[9],
                "payout_usd": element[10],
                "exchange_rate": element[11],
                "payout_eur": element[12],
                })

        except IndexError as e:
            user_data["user_alias_sales"] = []
        conn.commit()

    stockx_query = """
    select
        stockx_sales.date,
        stockx_sales.order,
        stockx_sales.sku,
        stockx_sales.product_name,
        stockx_sales.product_size,
        stockx_sales.tracking,
        stockx_sales.payout_eur
    from stockx_sales
        where stockx_sales.user_id = %s
    """

    with conn.cursor() as c:
        c.execute(stockx_query,(user_id,))

        try:
            user_data["user_stockx_sales"] = c.fetchall()
        except IndexError as e:
            user_data["user_stockx_sales"] = []
        conn.commit()

    return user_data

#############################################

@app.route('/refresh_alias_sales', methods=["POST"])
@cross_origin()
def upload_alias():

    user_id = request.headers["user_id"]

    request_data = json.loads(request.data)
    alias_email = request_data["alias_email"]
    alias_password = request_data["alias_password"]
    current_alias_sales = []

    try:
        with conn.cursor() as c:
            c.execute("""
                SELECT "order" FROM ALIAS_SALES WHERE USER_ID = %s
            """,(user_id,))
            current_alias_sales = c.fetchall()
            conn.commit()
    except Exception as e:
        current_alias_sales = []
        
    data = None
    header = None
    session = None
    access_token = None
    scraped_orders = []
    exchange_rate = 1.0

    # INITIAL HEADER/SESSION/PASSWORD
    header = {
        "User-Agent":"alias/1.16.0 (iPhone; iOS 15.4.1; Scale/3.00) Locale/de",
        "Content-Type":"application/json",
        "authorization": 'Bearer {}'.format(access_token)
        }
    session = tls_client.Session(
        client_identifier="safari_ios_16_0"
        )
    payload = json.dumps({
        "grantType": "password",
        "username": alias_email,
        "password": alias_password
        })

    # REQUEST ALIAS ACCESS TOKEN WITH LOGIN CREDENTIALS
    try:
        response = session.post("https://sell-api.goat.com/api/v1/unstable/users/login",headers = header, data = payload)
        access_token = response.json().get('auth_token').get('access_token')
    except Exception as e:
        return {"data": 401}

    # SCRAPE TRANSACTIONS
    current_page = 0
    total_pages=1
    stop_search = False

    header = {
        "User-Agent":"alias/1.16.0 (iPhone; iOS 15.4.1; Scale/3.00) Locale/de",
        "Content-Type":"application/json",
        "authorization": 'Bearer {}'.format(access_token)
        }

    while not stop_search:
        response = session.get("https://sell-api.goat.com/api/v1/users/transactions?includeMetadata=1&page={}".format(current_page), headers = header)
        transactions = response.json().get('items')
        for transaction in transactions:
            if transaction.get('transaction_type') == "CASHOUT":
                response = session.get("https://sell-api.goat.com/api/v1/users/transaction-details?id={}".format(transaction.get("id")),headers=header)
                transaction_details = response.json()
                exchange_rate,transaction_details =  int(transaction_details.get('cash_out').get('localized_transfer_amount_cents').get('amount_cents')) / int(transaction_details.get('cash_out').get('transfer_amount_cents')), transaction_details
                transaction["transaction_details"]=transaction_details
                transaction["exchange_rate"]=exchange_rate
                scraped_orders.append(transaction)
            elif transaction.get('transaction_type') == 'SALE' and exchange_rate > 0:
                order_number = transaction.get('type').split('#')[1]
                if not any(d[0] == order_number for d in current_alias_sales):
                    try:
                        response = session.get("https://sell-api.goat.com/api/v1/purchase-orders/{}".format(order_number), headers = header)
                        order_details = response.json()
                    except:
                        print(response.text)
                    transaction["order_details"] = order_details
                    transaction["exchange_rate"] = exchange_rate
                    if order_details != None:
                        print("New Order Added")
                        scraped_orders.append(transaction)
                    else:
                        stop_search = True

        response = session.get("https://sell-api.goat.com/api/v1/users/transactions?includeMetadata=1&page={}".format(current_page), headers = header)
        current_page = int(response.json().get('metadata').get('next_page'))
        print(current_page)
        total_pages = int(response.json().get('metadata').get('total_pages'))
        print(total_pages)
        if current_page >= total_pages:
            ("REACHED")
            stop_search = True

        ################### End of scraping ###################

    formatted_orders = []

    for order in scraped_orders:
        if order["transaction_type"] == "SALE":

            sale_price_usd = round(float(order.get('order_details').get("purchase_order").get("listing").get("price_cents")) / 100, 2)
            provision = round(float(sale_price_usd*9.5/100), 2)
            payout_fee = float(round((sale_price_usd - provision - 6)*2.9/100, 2))
            payout_usd = float(round(sale_price_usd - provision - payout_fee - 6, 2))

            formatted_orders.append({
            "user_id": user_id,
            "order": order["order_details"]["purchase_order"]["number"],
            "sale_date": order["order_details"]["purchase_order"]["created_at"],
            "payout_date": order["order_details"]["purchase_order"]["created_at"], #need fix
            "product_name": order["order_details"]["purchase_order"]["listing"]["product"]["name"],
            "sku": order["order_details"]["purchase_order"]["listing"]["product"]["sku"],
            "product_size": order["order_details"]["purchase_order"]["listing"]["size"],
            "tracking": None if order.get('order_details').get( "purchase_order").get("shipping_info") is None else order.get('order_details').get("purchase_order").get("shipping_info").get("tracking_url"),
            "sale_price_usd": sale_price_usd,
            "provision": provision,
            "sales_fee": 6,
            "payout_fee": payout_fee,
            "payout_usd": payout_usd,
            "exchange_rate": order["exchange_rate"],
            "payout_eur": round(payout_usd*order["exchange_rate"], 2)
            })

    for record in formatted_orders:
        with conn.cursor() as c:
            c.execute("""
            INSERT INTO ALIAS_SALES (user_id, date, "order", sku, product_name, product_size, tracking, sale_price_usd, provision, sales_fee, payout_fee, payout_usd, exchange_rate, payout_eur, payout_date)
            SELECT %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
            WHERE NOT EXISTS (SELECT "order" FROM ALIAS_SALES WHERE "order" = %s)
            """,(user_id,record["sale_date"],record["order"],record["sku"],record["product_name"],record["product_size"],record["tracking"],record["sale_price_usd"],record["provision"],record["sales_fee"],record["payout_fee"],record["payout_usd"],record["exchange_rate"],record["payout_eur"],record["payout_date"],record["order"],))
            conn.commit()

    return {"data":200}

@app.route('/generate_alias_invoices')
@cross_origin()
def generate_alias():
    pass
@app.route('/generate_download_alias_invoices')
@cross_origin()
def generate_download_alias():
    pass

#############################################

@app.route('/upload_stockx_sales')
@cross_origin()
def upload_stockx():
    pass
@app.route('/genereate_stockx_invoices')
@cross_origin()
def generate_stockx():
    pass
@app.route('/generate_download_stockx_invoices')
@cross_origin()
def generate_download_stockx():
    pass

#############################################

@app.route('/save_user_settings', methods=["POST"])
@cross_origin()
def save_settings():

    user_id = request.headers["user_id"]

    request_data = json.loads(request.data)
    sevdesk_api_key = request_data["sevdesk_api_key"]
    alias_email = request_data["alias_email"]
    alias_password = request_data["alias_password"]
    sort_option = request_data["sort_option"]

    sevdesk_creator_id = None
    sevdesk_alias_id = None
    sevdesk_stockx_id = None

    if sevdesk_api_key == "" or sevdesk_api_key == "null":
        sevdesk_api_key=None

    if sevdesk_api_key != None:
        with conn.cursor() as c:
            c.execute("select user_settings.sevdesk_creator_id from user_settings where user_settings.user_id = %s",(user_id,))
            result = c.fetchall()[0][0]
            if result == None:
                sevdesk_creator_id = requests.get("https://my.sevdesk.de/api/v1/sevUser?token=" + str(sevdesk_api_key)).json()["objects"][0]["id"]
                contacts = requests.get("https://my.sevdesk.de/api/v1/Contact?token=" + str(sevdesk_api_key)).json()["objects"]
                for contact in contacts:
                    if "stockx" in contact["name"].lower():
                        sevdesk_stockx_id=contact["id"]
                    if "goat" in contact["name"].lower():
                        sevdesk_alias_id=contact["id"]
            conn.commit()

    save_settings_query = """
    update user_settings
    set
    sevdesk_api_key = %s,
    sevdesk_creator_id = %s,
    sevdesk_alias_id = %s,
    sevdesk_stockx_id = %s,
    alias_email = %s,
    alias_password = %s,
    sort_invoice_by_sale_date = %s
    where
    user_id = %s
    """

    with conn.cursor() as c:
        res = c.execute(save_settings_query,(sevdesk_api_key,sevdesk_creator_id,sevdesk_alias_id,sevdesk_stockx_id,alias_email,alias_password,sort_option,user_id,))
        conn.commit()

    return {
    "sevdesk_api_key": sevdesk_api_key,
    "alias_email": alias_email,
    "alias_password": alias_password,
    "sort_invoice_by_sale_date": sort_option,
    }

if __name__ == '__main__':
    app.run(host='10.0.0.9', port=5000,debug=True)
