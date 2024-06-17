

from flask import Flask, request, jsonify;

app = Flask(__name__);

@app.route('/', methods=["GET"])
def hello_world():
    return "<h1>Hello World!</h1>";

# add an employees class:
class Employee:
    def __init__(self, first_name, last_name, email, gender, language, position):
        self.first_name = first_name;
        self.last_name = last_name;
        self.email=email;
        self.gender = gender;
        self.language = language;
        self.postion = position;

    def __repr__(self) -> str:
        return f"<Employee {self.first_name}, {self.last_name}, {self.email}, {self.gender}, {self.language}, {self.postion}";


employees = []; # adding list of emplyees


# add a route to add employees
@app.route("/add", methods=["POST"])
def add ():
    new_emp = Employee(
        first_name = request.json["first_name"],
        last_name = request.json ["last_name"],
        email = request.json ["email"],
        gender= request.json ["gender"],
        language = request.json ["language"],
        position = request.json ["position"]
    );

    employees.append(new_emp);
    return jsonify (employees=[str(emp) for emp in employees]);

# add route to upload employees from file. 
@app.route("/upload", methods=["POST"])
def upload():
    content = request.files['file'].stream.read().decode();

    for line in content.split("\n"):
        new_emp = Employee(*line.split(","));
        employees.append(new_emp);
    
    return jsonify(employees=[str(empl for empl in employees)]);

# Search for employee
@app.route("/search", methods=["GET"])
def search():
    result = employees  # Corrected variable name
    criteria = ["first_name", "last_name", "email", "gender", "language", "position"]

    for criterium in criteria:
        if criterium in request.args:
            result = [
                employee
                for employee in result
                if request.args[criterium] in getattr(employee, criterium)
            ]

    return jsonify(employees=[str(employee) for employee in result])  # Corrected JSON key



if __name__ == "__main__":
    app.run(debug=True);

