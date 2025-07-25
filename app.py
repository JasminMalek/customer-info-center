from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import requests
from datetime import datetime

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

# Ticket parser for Jira integration
ticket_parser = reqparse.RequestParser()
ticket_parser.add_argument('title', type=str, required=True, help='Ticket title is required.')
ticket_parser.add_argument('description', type=str, required=True, help='Ticket description is required.')
ticket_parser.add_argument('product_id', type=int, required=True, help='Product ID is required for Jira sync.')
ticket_parser.add_argument('priority', type=str, default='Medium')
ticket_parser.add_argument('customer_id', type=int, required=True, help='Customer ID is required.')

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


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    jira_project_key = db.Column(db.String(50), nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), default='Medium')
    status = db.Column(db.String(50), default='Open')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    jira_issue_key = db.Column(db.String(50), nullable=True)
    jira_synced = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship('Customer', backref='tickets')
    product = db.relationship('Product', backref='tickets')

    def __repr__(self):
        return f'<Ticket {self.title}>'


class JiraConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_url = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    api_token = db.Column(db.String(255), nullable=False)
    default_project_key = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<JiraConfig {self.server_url}>'


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


def serialize_ticket(ticket):
    return {
        'id': ticket.id,
        'title': ticket.title,
        'description': ticket.description,
        'priority': ticket.priority,
        'status': ticket.status,
        'customer_id': ticket.customer_id,
        'product_id': ticket.product_id,
        'jira_issue_key': ticket.jira_issue_key,
        'jira_synced': ticket.jira_synced,
        'created_at': ticket.created_at.isoformat() if ticket.created_at else None,
        'customer_name': ticket.customer.name if ticket.customer else None,
        'product_name': ticket.product.name if ticket.product else None
    }


def serialize_product(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'jira_project_key': product.jira_project_key,
        'active': product.active,
        'created_at': product.created_at.isoformat() if product.created_at else None
    }


def validate_ticket_for_jira_sync(ticket):
    """Validate that a ticket meets requirements for Jira sync"""
    if not ticket.product_id:
        return False, "Ticket must be linked to a product"
    
    if not ticket.product:
        return False, "Product not found"
    
    if not ticket.product.active:
        return False, "Product is not active"
    
    return True, "Validation passed"


def sync_ticket_to_jira(ticket_id):
    """Sync a ticket to Jira"""
    try:
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return {'success': False, 'error': 'Ticket not found'}
        
        # Validate ticket for Jira sync
        is_valid, message = validate_ticket_for_jira_sync(ticket)
        if not is_valid:
            return {'success': False, 'error': f'Failed to sync to Jira - {message}'}
        
        # Get Jira configuration
        jira_config = JiraConfig.query.filter_by(active=True).first()
        if not jira_config:
            return {'success': False, 'error': 'Jira configuration not found'}
        
        # Determine project key
        project_key = ticket.product.jira_project_key or jira_config.default_project_key
        
        # Prepare Jira issue data
        issue_data = {
            "fields": {
                "project": {"key": project_key},
                "summary": ticket.title,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": ticket.description
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {"name": "Task"},
                "priority": {"name": ticket.priority}
            }
        }
        
        # Make API call to Jira
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        auth = (jira_config.username, jira_config.api_token)
        
        response = requests.post(
            f"{jira_config.server_url}/rest/api/3/issue",
            json=issue_data,
            headers=headers,
            auth=auth
        )
        
        if response.status_code == 201:
            jira_issue = response.json()
            ticket.jira_issue_key = jira_issue['key']
            ticket.jira_synced = True
            db.session.commit()
            
            return {
                'success': True, 
                'jira_issue_key': jira_issue['key'],
                'message': 'Ticket successfully synced to Jira'
            }
        else:
            return {
                'success': False, 
                'error': f'Jira API error: {response.status_code} - {response.text}'
            }
            
    except Exception as e:
        return {'success': False, 'error': f'Unexpected error: {str(e)}'}


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


class TicketResource(Resource):
    
    def get(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if ticket:
            return serialize_ticket(ticket), 200
        return {'message': 'Ticket not found'}, 404
    
    def put(self, ticket_id):
        args = ticket_parser.parse_args()
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return {'message': 'Ticket not found'}, 404
        
        ticket.title = args['title']
        ticket.description = args['description']
        ticket.product_id = args['product_id']
        ticket.priority = args['priority']
        ticket.customer_id = args['customer_id']
        db.session.commit()
        return {'message': 'Ticket updated successfully'}, 200
    
    def delete(self, ticket_id):
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return {'message': 'Ticket not found'}, 404
        
        db.session.delete(ticket)
        db.session.commit()
        return {'message': 'Ticket deleted successfully'}, 200


class TicketListResource(Resource):
    
    def get(self):
        tickets = Ticket.query.all()
        ticket_list = [serialize_ticket(ticket) for ticket in tickets]
        return ticket_list, 200
    
    def post(self):
        args = ticket_parser.parse_args()
        ticket = Ticket(
            title=args['title'],
            description=args['description'],
            product_id=args['product_id'],
            priority=args['priority'],
            customer_id=args['customer_id']
        )
        db.session.add(ticket)
        db.session.commit()
        return {'message': 'Ticket created successfully', 'ticket_id': ticket.id}, 201


class TicketJiraSyncResource(Resource):
    
    def post(self, ticket_id):
        """Send ticket to Jira"""
        result = sync_ticket_to_jira(ticket_id)
        
        if result['success']:
            return result, 200
        else:
            return result, 400


class ProductListResource(Resource):
    
    def get(self):
        products = Product.query.filter_by(active=True).all()
        product_list = [serialize_product(product) for product in products]
        return product_list, 200
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Product name is required.')
        parser.add_argument('description', type=str, nullable=True)
        parser.add_argument('jira_project_key', type=str, nullable=True)
        
        args = parser.parse_args()
        product = Product(
            name=args['name'],
            description=args['description'],
            jira_project_key=args['jira_project_key']
        )
        db.session.add(product)
        db.session.commit()
        return {'message': 'Product created successfully', 'product_id': product.id}, 201


api.add_resource(CustomerListResource, '/customers')
api.add_resource(CustomerResource, '/customers/<int:customer_id>')
api.add_resource(TicketListResource, '/tickets')
api.add_resource(TicketResource, '/tickets/<int:ticket_id>')
api.add_resource(TicketJiraSyncResource, '/tickets/<int:ticket_id>/sync-to-jira')
api.add_resource(ProductListResource, '/products')

if __name__ == '__main__':
    app.run(debug=True)
