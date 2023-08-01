from flask import Flask, render_template, request
import mysql.connector

def create_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='owner_details',
    )

app = Flask(__name__)

@app.route('/add_owner', methods=['POST'])
def add_owner():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    connection = create_db_connection()
    cursor = connection.cursor()

    sql = "INSERT INTO owner_details(name,email,phone,address) VALUES (%s, %s, %s, %s)"
    data = (name, email, phone, address)
    cursor.execute(sql, data)

    connection.commit()
    cursor.close()
    connection.close()

    return "Owner details added successfully!"







@app.route('/')
def welcome():
    return render_template("welcome_page.html")

@app.route('/add_owner_and_pets', methods=['GET','POST'])
def add_owner_and_pets():
    return render_template('add_owner_and_pets.html')


@app.route('/v')
def view_registered_owners():
    connection = create_db_connection()
    cursor = connection.cursor()

    sql = "SELECT * from owner_details;"
    cursor.execute(sql)
    owners = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('owners.html', owners=owners)


@app.route('/add_pets/<int:owner_id>', methods=['GET', 'POST'])
def add_pets(owner_id):
    connection = create_db_connection()
    cursor = connection.cursor()

    if request.method == 'POST':
        pet_name = request.form['pet_name']
        breed = request.form['breed']
        age = request.form['age']
        problem = request.form['problem']

        sql = "INSERT INTO pet_details(pet_name,breed,age, problem, owner_id) VALUES (%s, %s, %s, %s, %s) "
        data = (pet_name, breed, age, problem, owner_id)
        cursor.execute(sql, data)

        connection.commit()

    cursor.close()
    connection.close()

    return render_template('add_pets.html', owner_id=owner_id)


@app.route('/pet_list/<owner_id>', methods=['GET', 'POST'])
def pet_list(owner_id):
    connection = create_db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM pet_details WHERE owner_id= %s"
    cursor.execute(sql, (owner_id,))
    pets = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('pet_list.html', pets=pets)

if __name__ == "__main__":
  app.run(debug=True)