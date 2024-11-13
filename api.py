from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI  # Assuming config.py contains DATABASE_URI for SQLAlchemy

# Initialize Flask app and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Billing model based on the database schema
class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    billing_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'amount': self.amount,
            'billing_date': self.billing_date,
            'description': self.description
        }

# Create billing record
@app.route('/billing', methods=['POST'])
def create_billing():
    data = request.get_json()
    new_billing = Billing(
        customer_name=data['customer_name'],
        amount=data['amount'],
        billing_date=data['billing_date'],
        description=data.get('description')
    )
    db.session.add(new_billing)
    db.session.commit()
    return jsonify(new_billing.to_dict()), 201

# Get billing record by ID
@app.route('/billing/<int:id>', methods=['GET'])
def get_billing(id):
    billing = Billing.query.get_or_404(id)
    return jsonify(billing.to_dict())

# Update billing record by ID
@app.route('/billing/<int:id>', methods=['PUT'])
def update_billing(id):
    billing = Billing.query.get_or_404(id)
    data = request.get_json()
    billing.customer_name = data.get('customer_name', billing.customer_name)
    billing.amount = data.get('amount', billing.amount)
    billing.billing_date = data.get('billing_date', billing.billing_date)
    billing.description = data.get('description', billing.description)
    db.session.commit()
    return jsonify(billing.to_dict())

# Delete billing record by ID
@app.route('/billing/<int:id>', methods=['DELETE'])
def delete_billing(id):
    billing = Billing.query.get_or_404(id)
    db.session.delete(billing)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
