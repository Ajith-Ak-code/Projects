from flask import Flask, jsonify, request
import mysql.connector
import json

app = Flask(__name__)

con = mysql.connector.connect(database="demo1", user="root", password="root", host="localhost")


@app.route('/students', methods=['GET'])
def get_student_details():
    cur = con.cursor()
    cur.execute("SELECT * from mytable")
    response = cur.fetchall()
    return jsonify(response)


@app.route('/student/<int:Register_Number>', methods=['GET'])
def get_id_student_details(Register_Number):
    cur = con.cursor()
    qury = cur.execute("SELECT * FROM mytable WHERE Register_Number=%s", (Register_Number,))
    student_data = cur.fetchone()
    if student_data:
        response = ({
            "student details": student_data
        }), 201
    else:
        response = ({
            "Result": "Register Number doesn't exist",
            "status": 400
        }), 404

    return response


@app.route('/student', methods=['POST'])
def post():
    cur = con.cursor()
    if request.method == "POST":
        req_data = request.get_json()
        Name = req_data['Name']
        Register_Number = req_data['Register_Number']
        Department = req_data['Department']
        data = request.json['Sem_Result']
        Sem_Result = json.dumps(data)
        cur.execute("insert into mytable(Name,Register_Number,Department,Sem_Result)values(%s,%s,%s,%s)",
                    (Name, Register_Number, Department, Sem_Result))
        con.commit()
        return jsonify(Name=Name, Register_Number=Register_Number, Department=Department, Sem_Result=Sem_Result), 201
    return jsonify('Error')


@app.route('/update/<int:Register_Number>', methods=['PUT'])
def put(Register_Number):
    if request.method == "PUT":
        req_data = request.get_json()
        Name = req_data['Name']
        Department = req_data['Department']
        data = request.json['Sem_Result']
        Sem_Result = json.dumps(data)
        cur = con.cursor()
        cur.execute("UPDATE mytable SET Name=%s,Department=%s,Sem_Result=%s WHERE Register_Number=%s",
                    (Name, Department, Sem_Result, Register_Number))
        con.commit()
        return jsonify(Name=Name, Register_Number=Register_Number, Department=Department, Sem_Result=Sem_Result), 201
    return jsonify("Error")


if __name__ == "__main__":
    app.run(debug=True)
