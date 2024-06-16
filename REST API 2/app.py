from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    expenses_list = [{
        'id': expense.id,
        'title': expense.title,
        'amount': expense.amount,
        'date': expense.date.strftime('%Y-%m-%d')
    } for expense in expenses]
    return jsonify(expenses_list)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(
        title=data['title'],
        amount=data['amount'],
        date=datetime.strptime(data['date'], '%Y-%m-%d')
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'message': 'Expense added'}), 201

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expense(id):
    data = request.get_json()
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404
    
    expense.title = data.get('title', expense.title)
    expense.amount = data.get('amount', expense.amount)
    expense.date = datetime.strptime(data.get('date', expense.date.strftime('%Y-%m-%d')), '%Y-%m-%d')
    
    db.session.commit()
    return jsonify({'message': 'Expense updated'})

@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({'message': 'Expense not found'}), 404
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
