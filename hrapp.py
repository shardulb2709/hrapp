from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# PostgreSQL Connection
DB_CONFIG = {
    "dbname": "postgres",
    "user": "shardul",
    "password": "Admin@1234",
    "host": "pgfs3n.postgres.database.azure.com",  # This should match the Kubernetes Service name
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/employees', methods=['POST'])
def insert_employee():
    """Insert Employee Data"""
    data = request.json
    emp_id = data.get('emp_id')
    emp_name = data.get('emp_name')
    salary = data.get('salary')

    if not emp_id or not emp_name or not salary:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO employees (emp_id, emp_name, salary) VALUES (%s, %s, %s)", 
                    (emp_id, emp_name, salary))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Employee added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    """Fetch Employee Data"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT emp_id, emp_name, salary FROM employees WHERE emp_id = %s", (emp_id,))
        employee = cur.fetchone()
        cur.close()
        conn.close()

        if employee:
            return jsonify({"emp_id": employee[0], "emp_name": employee[1], "salary": employee[2]})
        else:
            return jsonify({"error": "Employee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
