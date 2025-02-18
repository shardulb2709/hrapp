from flask import Flask, render_template, request, jsonify
import psycopg2

#app = Flask(__name__)
app = Flask(__name__, template_folder="templates")

# Database Configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "shardul",
    "password": "Admin@1234",
    "host": "pgfs3n.postgres.database.azure.com",
    "port": "5432"
}

def connect_db():   
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template("index.html", employees=employees)
    except Exception as e:
        return jsonify({"error": str(e)})

# Insert Employee
@app.route('/insert', methods=['POST'])
def insert_employee():
    try:
        # Check if request contains JSON data
        if request.is_json:
            data = request.json
        else:
            # Extract form data from the HTML form submission
            data = request.form

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO employees (emp_name, salary, department) VALUES (%s, %s, %s) RETURNING emp_id",
            (data['emp_name'], data['salary'], data['department'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Employee inserted successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/find', methods=['GET'])
def find_employee():
    emp_name = request.args.get('emp_name', '')

    print(f"Searching for employee: {emp_name}")  # Debugging

    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE emp_name ILIKE %s", (emp_name,))
        employee = cursor.fetchall()
        cursor.close()
        conn.close()
        print("Employee found:", employee)  # Debugging
        return jsonify(employee)
    except Exception as e:
        return jsonify({"error": str(e)})    
# Fetch Employees
@app.route('/employees', methods=['GET','POST'])
def get_employees():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees")
        employees = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)