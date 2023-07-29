from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'customer_info',
    'charset': 'utf8mb4',
    # 'cursorclass': pymysql.cursors.DictCursor
}

# Create a connection to the database
connection = pymysql.connect(**db_config)

# Parser for POST and PUT requests
customer_parser = reqparse.RequestParser()
customer_parser.add_argument('name', type=str, required=True, help='Customer name is required.')
customer_parser.add_argument('first_name', type=str, nullable=True)
customer_parser.add_argument('last_name', type=str, nullable=True)
customer_parser.add_argument('email', type=str, required=True, help='Customer email is required.')
customer_parser.add_argument('gender', type=int, nullable=True)
customer_parser.add_argument('phone_number', type=str, nullable=True, default='')
customer_parser.add_argument('birthday', type=str, nullable=True)
customer_parser.add_argument('address', type=str, nullable=True)
customer_parser.add_argument('postcode', type=str, nullable=True)
customer_parser.add_argument('city', type=str, nullable=True)

# Configure SQLAlchemy
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['db']}?charset={db_config['charset']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    gender = db.Column(db.SmallInteger, nullable=True)
    phone_number = db.Column(db.String(20), default='', nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    postcode = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Customer {self.name}>'


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


def serialize_customer(customer):
    return {
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'gender': customer.gender,
        'phone_number': customer.phone_number,
        'birthday': customer.birthday,
        'address': customer.address,
        'postcode': customer.postcode,
        'city': customer.city,
    }


class CustomerResource(Resource):

    def get(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer:
            return serialize_customer(customer), 200
        return {'message': 'Customer not found'}, 404

    def put(self, customer_id):
        args = customer_parser.parse_args()
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'message': 'Customer not found'}, 404

        customer.name = args['name']
        customer.first_name = args['first_name']
        customer.last_name = args['last_name']
        customer.email = args['email']
        customer.gender = args['gender']
        customer.phone_number = args['phone_number']
        customer.birthday = args['birthday']
        customer.address = args['address']
        customer.postcode = args['postcode']
        customer.city = args['city']
        db.session.commit()
        return {'message': 'Customer updated successfully'}, 200

    def delete(self, customer_id):
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'message': 'Customer not found'}, 404

        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted successfully'}, 200


class CustomerListResource(Resource):

    def get(self):
        customers = Customer.query.all()
        customer_list = [serialize_customer(customer) for customer in customers]
        return customer_list, 200

    def post(self):
        args = customer_parser.parse_args()
        customer = Customer(name=args['name'], first_name=args['first_name'], last_name=args['last_name'],
                            email=args['email'], gender=args['gender'], phone_number=args['phone_number'],
                            birthday=args['birthday'], address=args['address'], postcode=args['postcode'],
                            city=args['city'])
        db.session.add(customer)
        db.session.commit()
        return {'message': 'Customer created successfully'}, 201


api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:customer_id>')

if __name__ == '__main__':
    app.run(debug=True)
