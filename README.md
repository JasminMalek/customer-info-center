# Customer Information Management with Jira Integration

Customer Information Management is a web application built using Python Flask as the backend and Vue.js as the frontend. The project includes Jira integration functionality to sync support tickets with Jira issues.

## 🚨 Jira Integration Error Fix

If you're seeing the error **"Failed to sync to Jira - Ticket must be linked to a product"**, this means:

1. **Root Cause**: Tickets require a product association before they can be synced to Jira
2. **Solution**: Ensure all tickets have a product assigned before attempting Jira synchronization
3. **Prevention**: Use the updated ticket creation form that enforces product selection

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [Jira Configuration](#jira-configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Features

### Core Features:
- **CRUD operations** for managing customer data using RESTful API
- **Support Ticket Management** with full lifecycle tracking
- **Product Management** for categorizing tickets and services
- **Jira Integration** with automatic ticket synchronization
- **Vue.js SPA** for responsive user interface

### Jira Integration Features:
- ✅ **Product Validation**: Prevents sync errors by enforcing product links
- ✅ **Automatic Sync**: Optional auto-sync to Jira on ticket creation  
- ✅ **Manual Sync**: Send individual tickets to Jira with one click
- ✅ **Status Tracking**: Visual indicators for Jira sync status
- ✅ **Error Handling**: Detailed error messages for troubleshooting

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python** (version 3.11.4 or higher)
- **Node.js** (version 18.17.0 or higher)
- **NPM** (version 9.6.7 or higher)
- **MySQL** database server
- **Jira Cloud** instance (for Jira integration)

### Installation

Follow these steps to set up the project:

1. **Clone the repository**
    ```bash
    git clone https://github.com/JasminMalek/customer-info-center.git
    cd customer-info-center
    ```

2. **Install backend dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Install frontend dependencies**
    ```bash
    cd client
    npm install
    cd ..
    ```

### Database Setup

1. **Create MySQL database**
    ```sql
    CREATE DATABASE customer_info CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

2. **Initialize database tables**
    ```bash
    python3 create_tables.py
    ```

   This will create all necessary tables and sample data including:
   - Customer management tables
   - Product catalog
   - Support tickets  
   - Jira configuration

### Jira Configuration

To enable Jira integration:

1. **Get Jira API credentials**:
   - Go to your Jira Cloud instance
   - Navigate to Account Settings → Security → API tokens
   - Create a new API token

2. **Update Jira configuration** in the database:
   ```sql
   UPDATE jira_config SET 
       server_url = 'https://your-domain.atlassian.net',
       username = 'your-email@domain.com', 
       api_token = 'your-api-token-here',
       active = TRUE 
   WHERE id = 1;
   ```

3. **Verify Jira projects exist**:
   - Ensure the projects referenced in your products exist in Jira
   - Default project key in config should match an existing Jira project

## Usage

### Starting the Application

1. **Start the backend server**
    ```bash
    python3 app.py
    # Or using flask
    flask run
    ```

2. **Start the frontend development server**
    ```bash
    cd client
    npm run serve
    ```

3. **Access the application**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000

### Creating Tickets with Jira Integration

1. **Navigate to Tickets** → "Create New Ticket"
2. **Fill required fields**:
   - Title and description
   - Select a customer
   - **⚠️ IMPORTANT**: Select a product (required for Jira sync)
   - Set priority level
3. **Optional**: Enable "Automatically sync to Jira after creation"
4. **Submit** the ticket

### Manual Jira Synchronization

1. Go to the **Tickets List**
2. Find tickets with "Not Synced" status
3. Click **"Send to Jira"** button
4. Review sync results in the modal dialog

## API Endpoints

### Tickets
- `GET /tickets` - List all tickets
- `POST /tickets` - Create new ticket  
- `GET /tickets/<id>` - Get ticket details
- `PUT /tickets/<id>` - Update ticket
- `DELETE /tickets/<id>` - Delete ticket
- `POST /tickets/<id>/sync-to-jira` - Sync ticket to Jira

### Products  
- `GET /products` - List all products
- `POST /products` - Create new product

### Customers
- `GET /customers` - List all customers
- `POST /customers` - Create new customer
- `GET /customers/<id>` - Get customer details
- `PUT /customers/<id>` - Update customer
- `DELETE /customers/<id>` - Delete customer

## Troubleshooting

### Common Jira Integration Issues

1. **"Ticket must be linked to a product"**
   - ✅ **Solution**: Assign a product to the ticket before syncing
   - ✅ **Prevention**: Use the new ticket form that requires product selection

2. **"Jira configuration not found"**
   - Check if JiraConfig record exists and is active
   - Verify database connection

3. **"Jira API error: 401"**
   - Verify API token is correct and not expired  
   - Check username/email is correct

4. **"Jira API error: 404"**
   - Verify Jira project key exists
   - Check server URL is correct

### Debug Mode

Enable debug logging by setting `debug=True` in `app.py` for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the Jira integration
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).