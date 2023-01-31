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

    license_key = request.headers.get('key')

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
                print(sales)
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

@app.route('/refresh_alias_sales')
@cross_origin()
def upload_alias():
    return {"data":"data"}



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
    sevdesk_api_key = request.headers["sevdesk_api_key"]
    alias_email = request.headers["alias_email"]
    alias_password = request.headers["alias_password"]
    sort_option = request.headers["sort_option"]

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

def request_sevdesk_data():
    pass

def idk():
    inventory_list = []
    searchText = request.headers["searchText"].lower()
    addition = ""

    if searchText != "":
        addition = " WHERE (LOWER ( name ) LIKE '%" + searchText + "%') OR (LOWER ( sku )  LIKE '%" + searchText + "%')"
    else:
        addition = ""

    sql_query = "select id, picture_src, name, sku, size, buying_price, payout_price, profit, listed_restocks, listed_alias, listed_klekt, listed_stockx, status from inventory" + addition + " ORDER BY id ASC;"
    #print(sql_query)

    c.execute(sql_query)
    res = c.fetchall()

    for x in res:
        datablock = {
        "id": x[0],
        "picture_src": x[1],
        "name": x[2],
        "sku": x[3],
        "size": x[4],
        "buying_price": x[5],
        "payout_price": x[6],
        "profit": x[7],
        "listed_restocks": x[8],
        "listed_alias": x[9],
        "listed_klekt": x[10],
        "listed_stockx": x[11],
        "status": x[12],
        }
        inventory_list.append(datablock)

    return jsonify(inventory_list)

@app.route('/remove_item')
@cross_origin()
def remove_item():

    selectedId = request.headers["ID"]

    c.execute('DELETE FROM inventory WHERE id = ' + str(selectedId) + ';')
    conn.commit()

    return 'Successfully removed item!'

@app.route('/add_item', methods=["POST"])
@cross_origin()
def add_item():

    item = request.json

    x = { "picture_src": item["picture_src"], "name": item["name"], "sku": item["sku"], "size": item["size"], "buying_price": item["buying_price"], "payout_price": item["payout_price"], "profit": item["profit"], "listed_restocks": item["listed_restocks"], "listed_alias": item["listed_alias"], "listed_klekt": item["listed_klekt"], "listed_stockx": item["listed_stockx"], "status": item["status"] }

    c.execute('INSERT INTO inventory (picture_src, name, sku, size, buying_price, payout_price, profit, listed_restocks, listed_alias, listed_klekt, listed_stockx, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (x["picture_src"], x["name"], x["sku"], x["size"], x["buying_price"], x["payout_price"], x["profit"], x["listed_restocks"], x["listed_alias"], x["listed_klekt"], x["listed_stockx"], x["status"]))

    conn.commit()

    return 'Added Item Successful!'

@app.route('/update_status', methods=["PUT"])
@cross_origin()
def update_status():

    id = request.json["id"]
    selected_status = request.json["selected_status"]

    c.execute("UPDATE inventory SET status = " + str(selected_status) + " WHERE id = " + str(id) + ";")

    conn.commit()

    return 'Successfully updated item status!'

@app.route('/update_listing', methods=["PUT"])
@cross_origin()
def update_listing():

    identifier = request.json["identifier"]
    id = request.json["id"]
    selected_status = request.json["selected_status"]

    c.execute("UPDATE inventory SET " + identifier + " = " + str(selected_status) + " WHERE id = " + str(id) + ";")

    conn.commit()

    return 'Successfully updated item listing!'

if __name__ == '__main__':
    app.run(host='10.0.0.9', port=5000,debug=True)
