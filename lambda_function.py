import pg8000
import json

# Database connection details
DB_HOST = 'database-1-instance-1.cj8w4gsoqqs3.eu-north-1.rds.amazonaws.com'
DB_PORT = 5432  # Default PostgreSQL port
DB_NAME = 'postgres'  # Replace with your actual database name
DB_USER = 'postgres'  # Replace with your actual username
DB_PASSWORD = 'venkat123'  # Replace with your actual password

# Lambda function handler
def lambda_handler(event, context):
    cursor = None  # Initialize cursor
    conn = None  # Initialize connection
    try:
        # Check if 'httpMethod' exists in event
        if 'httpMethod' not in event:
            raise KeyError("'httpMethod' key not found in event")
        
        # Establish connection to the PostgreSQL database using pg8000
        conn = pg8000.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Check the HTTP method and perform actions based on it
        if event['httpMethod'] == 'GET':
            cursor.execute("SELECT * FROM clients;")  # Replace with your table name
            rows = cursor.fetchall()
            
            # Prepare response body
            data = []
            for row in rows:
                data.append({
                    'client_id': row[0],  # Assuming the first column is client_id
                    'client_name': row[1]  # Assuming the second column is client_name
                })
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Data retrieved successfully',
                    'data': data
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        elif event['httpMethod'] == 'POST':
            # Example for inserting data from the POST request body
            request_data = json.loads(event['body'])
            client_name = request_data.get('client_name')  # Assuming 'client_name' is passed in the body
            cursor.execute("INSERT INTO clients (client_name) VALUES (%s);", (client_name,))
            conn.commit()

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': 'Data inserted successfully!'
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        else:
            # Respond with an error message if the method is neither GET nor POST
            return {
                'statusCode': 405,  # Method Not Allowed
                'body': json.dumps({
                    'message': 'The method you are calling is not correct. Please use GET or POST.'
                }),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    finally:
        # Close the connection and cursor if they were initialized
        if cursor:
            cursor.close()
        if conn:
            conn.close()
