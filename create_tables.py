#!/usr/bin/env python3

"""
Database initialization script for Jira integration
Creates tables for tickets, products, and Jira configuration
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db, Customer, Product, Ticket, JiraConfig
    
    def create_tables():
        """Create all database tables"""
        with app.app_context():
            # Create tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create some sample data for testing
            create_sample_data()
            
    def create_sample_data():
        """Create sample data for testing"""
        try:
            # Check if sample data already exists
            if Product.query.first() is not None:
                print("📋 Sample data already exists, skipping creation.")
                return
                
            # Create sample products
            products = [
                Product(
                    name="Web Application Support",
                    description="Support for web applications and services",
                    jira_project_key="WEB"
                ),
                Product(
                    name="Mobile App Support", 
                    description="Support for mobile applications",
                    jira_project_key="MOB"
                ),
                Product(
                    name="Infrastructure Support",
                    description="Support for IT infrastructure and systems",
                    jira_project_key="INF"
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            # Create sample Jira configuration (placeholder)
            jira_config = JiraConfig(
                server_url="https://your-domain.atlassian.net",
                username="your-email@domain.com",
                api_token="your-api-token-here",
                default_project_key="SUPPORT",
                active=False  # Set to False until real credentials are added
            )
            db.session.add(jira_config)
            
            db.session.commit()
            print("✅ Sample data created successfully!")
            print("\n📋 Created products:")
            for product in products:
                print(f"  - {product.name} (Jira Project: {product.jira_project_key})")
                
            print("\n⚠️  To enable Jira integration:")
            print("   1. Update the JiraConfig with your actual Jira credentials")
            print("   2. Set active=True in the JiraConfig record")
            print("   3. Ensure your Jira projects exist and are accessible")
            
        except Exception as e:
            print(f"❌ Error creating sample data: {e}")
            db.session.rollback()

    if __name__ == "__main__":
        create_tables()
        
except ImportError as e:
    print(f"❌ Error importing modules: {e}")
    print("💡 Make sure to install dependencies: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)