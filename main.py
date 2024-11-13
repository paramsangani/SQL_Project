# main.py

from flask import Flask, jsonify, request
import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

app = Flask(__name__)

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )

from flask import render_template

@app.route('/')
def index():
    return render_template('data.html')


# 1. Route to get all customers
@app.route('/customers', methods=['GET'])
def get_customers():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    db.close()
    return jsonify(customers)

# 2. Route to get a specific customer by ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()
    db.close()
    if customer:
        return jsonify(customer)
    else:
        return jsonify({"error": "Customer not found"}), 404

# 3. Route to create a new customer
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO Customers (customer_name, address, mobile, email) VALUES (%s, %s, %s, %s)",
        (data['customer_name'], data['address'], data['mobile'], data['email'])
    )
    db.commit()
    customer_id = cursor.lastrowid
    db.close()
    return jsonify({"message": "Customer created successfully", "customer_id": customer_id}), 201

# 4. Route to update an existing customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE Customers SET customer_name = %s, address = %s, mobile = %s, email = %s WHERE customer_id = %s",
        (data['customer_name'], data['address'], data['mobile'], data['email'], customer_id)
    )
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": "Customer updated successfully"})

# 5. Route to delete a customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify({"message": "Customer deleted successfully"})

# Route to search for a customer by criteria from the request body
@app.route('/customers/search', methods=['POST'])
def search_customer():
    data = request.json
    search_conditions = []
    params = []

    # Check for each field in the request body and add it to the query
    if 'customer_name' in data:
        search_conditions.append("customer_name LIKE %s")
        params.append(f"%{data['customer_name']}%")
    if 'address' in data:
        search_conditions.append("address LIKE %s")
        params.append(f"%{data['address']}%")
    if 'mobile' in data:
        search_conditions.append("mobile = %s")
        params.append(data['mobile'])
    if 'email' in data:
        search_conditions.append("email = %s")
        params.append(data['email'])

    if not search_conditions:
        return jsonify({"error": "No customer found"}), 400 

    query = "SELECT * FROM customers WHERE " + " AND ".join(search_conditions)
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    customers = cursor.fetchall()
    db.close()
    
    if customers:
        return jsonify(customers)
    else:
        return jsonify({"message": "No customers found matching the criteria"}), 404

# Route to search the information about the plan
@app.route('/service_plans', methods=['GET'])
def get_plan():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plan")
    plan = cursor.fetchall()
    db.close()
    return jsonify(plan)

#  Route to get a specific plan by ID
@app.route('/service_plans/<int:plan_id>', methods=['GET'])
def get_specific_plan(plan_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plan WHERE plan_id = %s", (plan_id,))
    plan= cursor.fetchone()
    db.close()
    if plan:
        return jsonify(plan)
    else:
        return jsonify({"error": "Plan not found"}), 404

# Route to get a specific plan by name
@app.route('/service_plans/name/<plan_name>', methods=['GET'])
def get_plan_by_name(plan_name):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plan WHERE plan_name = %s", (plan_name,))
    plan= cursor.fetchone()
    db.close()
    if plan:
        return jsonify(plan)
    else:
        return jsonify({"error": "Plan not found"}), 404


# Route to update an existing plan
@app.route('/service_plans/<int:plan_id>', methods=['PUT'])
def update_plan(plan_id):
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE service_plans SET plan_name = %s, speed = %s,data_limit = %s, validity = %s , price = %s WHERE plan_id = %s",
        (data['plan_name'], data['speed'], data['data_limit'], data['validity'], data['price'],plan_id)
    )
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Plan not found"}), 404
    return jsonify({"message": "Plan updated successfully"})

# Route to delete a plan
@app.route('/service_plans/<int:plan_id>', methods=['DELETE'])
def delete_plan(plan_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM service_plans WHERE plan_id = %s", (plan_id,))
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Plan not found"}), 404
    return jsonify({"message": "Plan deleted successfully"})


# Route to create a new Plan
@app.route('/service_plans', methods=['POST'])
def create_plan():
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO service_plans (plan_name, speed, data_limit, validity, price) VALUES (%s, %s, %s, %s,%s)",
        (data['plan_name'], data['speed'], data['data_limit'], data['validity'],data['price'])
    )
    db.commit()
    plan_id = cursor.lastrowid
    db.close()
    return jsonify({"message": "Plan created successfully", "plan_id": plan_id}), 201

# Route to search for a plans by criteria from the request body
@app.route('/service_plans/search', methods=['POST'])
def search_service_plans():
    data = request.json
    search_conditions = []
    params = []

    # Check for each field in the request body and add it to the query
    if 'data_limit' in data:
        search_conditions.append("data_limit LIKE %s")
        params.append(f"%{data['data_limit']}%")
    if 'validity' in data:
        search_conditions.append("validity LIKE %s")
        params.append(f"%{data['validity']}%")
    if 'price' in data:
        search_conditions.append("price = %s")
        params.append(data['price'])
    

    if not search_conditions:
        return jsonify({"error": "No plan found"}), 400 

    query = "SELECT * FROM service_plans WHERE " + " AND ".join(search_conditions)
    
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, params)
    plans = cursor.fetchall()
    db.close()
    
    if plans:
        return jsonify(plans)
    else:
        return jsonify({"message": "No plan found matching the criteria"}), 404


# Route to create new subscription 
@app.route('/subscription', methods=['POST'])
def create_subscription():
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO subscription (customer_id,plan_id, start_date, end_date, validity ) VALUES (%s, %s, %s, %s,%s)",
        (data['customer_id'], data['plan_id'], data['start_date'], data['end_date'],data['validity'])
    )
    db.commit()
    subscription_id = cursor.lastrowid
    db.close()
    return jsonify({"message": "subscription created successfully", "subscription_id": subscription_id}), 201

# Route to update an existing subscription
@app.route('/subscription/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    data = request.json
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE subscription SET customer_id = %s, plan_id = %s,start_date = %s, end_date = %s , validity = %s WHERE subscription_id = %s",
        (data['customer_id'], data['plan_id'], data['start_date'], data['end_date'], data['validity'],subscription_id)
    )
    db.commit()
    db.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "subscription not found"}), 404
    return jsonify({"message": "subscription updated successfully"})


if __name__ == '__main__':
    app.run(debug=True)

