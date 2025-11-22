
# Trippy Botanicals

This project is the final deliverable for the Rumos DevOps Academy.

### Overview
It's a comprehensive cloud software solution designed for botany enthusiasts. The platform facilitates online sales of flowers, various plants, and cultivation products, and includes a range of features to enhance the user experience.

### Features:
- Cart System: Users can add items to their cart for purchase.
- Checkout: A seamless checkout process for completing purchases.
- Inventory System: Efficient management of product stock and availability.
- Plant Identification Challenge: Users can participate in challenges to identify plants and earn points.
- Community Photo Upload: Users can upload photos of plants for community assistance in identification.

## Environment Variables

To run this project, create a `.flaskenv` configuration file in the root project folder and add the following variables:

`FLASK_APP` = Set the value to: `trippy.py`

`FLASK_ENV` - Set the environment. Use `development` to run it locally.

`FLASK_SECRET_KEY` - A secret key that will be used for securely signing the session cookie and can be used for any other security related needs by extensions or your application. It should be a long random string of bytes, although unicode is accepted too.

`WTF_CSRF_SECRET_KEY` - Random data for generating secure tokens for the WTForms library. If this is not set then SECRET_KEY is used.


#### Production specific environment variables:
In addition to the ones above, to run this project in production environment, the following variables are also required:

`AZURE_STORAGE_CONTAINER_NAME` - The name of the Azure Blob Storage container used to store application data such as images uploaded by users.

`AZURE_STORAGE_CONNECTION_STRING` - The connection string for accessing Azure Blob Storage service. It contains the credentials and the endpoint for connecting to the Azure Storage account.

`AZURE_DB_SERVER` - The hostname of the Azure SQL Database server. Example: <yourdbserver>.database.windows.net

`AZURE_DB_NAME` - The name of the specific database used by the application

`AZURE_DB_USERNAME` - The username for authenticating to the Azure SQL Database.

`AZURE_DB_PASSWORD` - The password for authenticating to the Azure SQL Database.

`SERVICE_BUS_CONNECTION_STRING` - The connection string for accessing Azure Service Bus.
## Setup

Install packages by running:

```bash
  pip install -r requirements.txt
```


Run database migrations:
```bash
  flask db upgrade
```
If you're using the development environment, this will create a SQLite database in `/tmp/trippy.db`.

If you need dummy data for development, then run:
```bash
  flask demo seed
```

## Development Environment vs. Production Environment
*Database Choice*

The project uses different databases for development and production to manage costs effectively and simplify setup:

- Production: Uses an Azure SQL Database for robust, scalable, and secure data storage.
- Development: Uses a SQLite database located at `/tmp/trippy.db` to minimize Azure cloud costs and allow quick setup.

*File Storage*
- Production: Uses Azure Blob Storage for file storage to ensure scalability and availability.
- Development: Stores files locally in the /app/static/uploads directory.
If you need to clean the local storage during development, you can run the following command:
 ```bash
  flask storage clean_local
```

## Building and Running the Docker Image

Building the Docker Image:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Run the following command to build the Docker image:
```bash
  docker build -t trippy-app .
```

Running the Docker Container:
```bash
docker run -d -p 8000:8000 --name trippy-container \
-e FLASK_ENV=development \
-e FLASK_SECRET_KEY=your_flask_secret_key \
-e WTF_CSRF_SECRET_KEY=your_csrf_secret_key \
-e AZURE_STORAGE_CONTAINER_NAME=your_storage_container_name \
-e AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string \
-e AZURE_DB_DRIVER=your_db_driver \
-e AZURE_DB_SERVER=your_db_server \
-e AZURE_DB_NAME=your_db_name \
-e AZURE_DB_USERNAME=your_db_username \
-e AZURE_DB_PASSWORD=your_db_password \
trippy-app
```
Or use a .env file (kept out of version control) with docker run --env-file .env <IMAGE_NAME>.

Once the container is running, you can access the application by navigating to http://localhost:8000 in your web browser.