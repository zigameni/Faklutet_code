from site import abs_paths

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import sqlite3

from sqlalchemy import desc, asc, between, and_, or_, and_, distinct, not_

CONNECTION_STRING = "sqlite:///bank.sqlite3"

application = Flask(__name__)
application.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING

database = SQLAlchemy(application)


# Models definitions remain the same
class City(database.Model):
    __tablename__ = "Mesto"
    id = database.Column("IdMes", database.Integer, primary_key=True)
    postal_code = database.Column("PostBr", database.String(6), unique=True)
    name = database.Column("Naziv", database.String(50))
    has_seat_in_list = database.relationship("HasSeatIn", back_populates="city")
    branches = database.relationship("Branch", back_populates="city")

    def __repr__(self):
        return f"City ( {self.id}, {self.postal_code}, {self.name} )"


class Client(database.Model):
    __tablename__ = "Komitent"
    id = database.Column("IdKom", database.Integer, primary_key=True)
    name = database.Column("Naziv", database.String(50))
    address = database.Column("Adresa", database.String(50))
    has_seat_in = database.relationship("HasSeatIn", back_populates="client", uselist=False)
    accounts = database.relationship("Account", back_populates="client")

    def __repr__(self):
        return f"Client ( {self.id}, {self.name}, {self.address} )"

    def to_dict(self):
        return {
            'id': self.id,
            "name": self.name,
            'address': self.address
        }


class HasSeatIn(database.Model):
    __tablename__ = "ImaSediste"
    client_id = database.Column("IdKom", database.ForeignKey(Client.id), primary_key=True)
    city_id = database.Column("IdMes", database.ForeignKey(City.id))
    city = database.relationship("City", back_populates="has_seat_in_list")
    client = database.relationship("Client", back_populates="has_seat_in")

    def __repr__(self):
        return f"HasSeatIn ( {self.client_id}, {self.city_id} )"


class Branch(database.Model):
    __tablename__ = "Filijala"
    id = database.Column("IdFil", database.Integer, primary_key=True)
    name = database.Column("Naziv", database.String(50))
    address = database.Column("Adresa", database.String(50))
    city_id = database.Column("IDMes", database.ForeignKey(City.id))
    city = database.relationship("City", back_populates="branches")
    accounts = database.relationship("Account", back_populates="branch")
    account_items = database.relationship("AccountItem", back_populates="branch")

    def __repr__(self):
        return f"Branch ( {self.id}, {self.name}, {self.address}, {self.city_id} )"


class Account(database.Model):
    __tablename__ = "Racun"
    id = database.Column("IdRac", database.Integer, primary_key=True)
    status = database.Column("Status", database.String(1))
    number_of_account_items = database.Column("BrojStavki", database.Integer)
    allowed_overdraft = database.Column("DozvMinus", database.Integer)
    balance = database.Column("Stanje", database.Integer)
    branch_id = database.Column("IdFil", database.ForeignKey(Branch.id))
    client_id = database.Column("IdKom", database.ForeignKey(Client.id))
    branch = database.relationship("Branch", back_populates="accounts")
    client = database.relationship("Client", back_populates="accounts")
    account_items = database.relationship("AccountItem", back_populates="account")

    def __repr__(self):
        return f"Account ( {self.id}, {self.status}, {self.number_of_account_items}, {self.allowed_overdraft}, {self.balance} )"

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'number_of_account_items': self.number_of_account_items,
            'allowed_overdraft': self.allowed_overdraft,
            'balance': self.balance,
            'branch_id': self.branch_id,
            'client_id': self.client_id
            # Add more fields as needed
        }


class AccountItem(database.Model):
    __tablename__ = "Stavka"
    id = database.Column("IdSta", database.Integer, primary_key=True)
    serial_number = database.Column("RedBroj", database.Integer)
    date = database.Column("Datum", database.Date)
    time = database.Column("Vreme", database.Time)
    amount = database.Column("Iznos", database.Integer)
    branch_id = database.Column("IdFil", database.ForeignKey(Branch.id))
    account_id = database.Column("IdRac", database.ForeignKey(Account.id))

    branch = database.relationship("Branch", back_populates="account_items")
    account = database.relationship("Account", back_populates="account_items")
    deposit = database.relationship("Deposit", back_populates="account_item", uselist=False)
    withdrawal = database.relationship("Withdrawal", back_populates="account_item", uselist=False)

    def __repr__(self):
        return f"AccountItem ( {self.id}, {self.serial_number}, {self.date}, {self.time}, {self.amount} )"


class Deposit(database.Model):
    __tablename__ = "Uplata"
    account_item_id = database.Column("IdSta", database.ForeignKey(AccountItem.id), primary_key=True)
    basis = database.Column("Osnov", database.String(10))

    account_item = database.relationship("AccountItem", back_populates="deposit")

    def __repr__(self):
        return f"Deposit ( {self.account_item}, {self.basis} )"


class Withdrawal(database.Model):
    __tablename__ = "Isplata"
    account_item_id = database.Column("IdSta", database.ForeignKey(AccountItem.id), primary_key=True)
    commission = database.Column("Provizija", database.Float)
    account_item = database.relationship("AccountItem", back_populates="withdrawal")

    def __repr__(self):
        return f"Withdrawal ( {self.account_item}, {self.commission} )"


# zd4
# -- SELECT all data from Komitent table
# SELECT * FROM Komitent;

@application.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all();

    output = [];
    for client in clients:
        client_data = {'id': client.id, 'name': client.name, "address": client.address}
        output.append(client_data)

    return jsonify({'clients': output})


# zd2
# -- SELECT all data from Racun table
# SELECT * FROM Racun;

@application.route("/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()

    output = []

    for acc in accounts:
        acc_data = {'id': acc.id, 'status': acc.status, "number_of_account_items": acc.number_of_account_items,
                    'allowed_overdraft': acc.allowed_overdraft}
        output.append(acc_data)

    return jsonify({"accounts": output})


# zd3
# -- SELECT names of all komitenata
# SELECT Naziv FROM Komitent;
@application.route('/client_names', methods=["GET"])
def get_client_names():
    clients = database.session.query(Client.name).all();  # we are getting rows not json
    output = [name[0] for name in clients];
    return output;


# zd4
# -- SELECT name and address of each komitent
# SELECT Naziv, Adresa FROM Komitent;
@application.route('/client_names_address', methods=["GET"])
def get_client_names_address():
    # clients = database.session.query(Client.name, Client.address).all();
    clients = Client.query.order_by(Client.name, desc(Client.address)).all();
    output = [name.to_dict() for name in clients]
    return jsonify(output);


# zd 5
# -- SELECT all data from Komitent table ordered by Naziv ascending
# SELECT * FROM Komitent
# ORDER BY Naziv;

@application.route('/clients_orderd_by_name', methods=["GET"])
def get_clients_orderd_by_name():
    # clients = Client.query.order_by(Client.name).all();
    # decending
    clients = Client.query.order_by(desc(Client.name)).all();

    output = [client.to_dict() for client in clients];
    return jsonify(output);


@application.route('/accounts_5000', methods=["GET"])
def get_accounts_5000():
    accounts = Account.query.filter(Account.balance == -55000).all();
    output = [acc.__repr__() for acc in accounts];
    return jsonify(output);


@application.route('/accoute_status_b', methods=["GET"])
def get_accoute_status_b():
    accounts = Account.query.filter(Account.status=="B", Account.balance<=-55000).all();
    output = [acc.to_dict() for acc in accounts];
    return jsonify(output);

@application.route('/accounts_10000_12000', methods=["GET"])
def get_accounts_10000_12000():
    accounts = Account.query.filter(between(Account.balance, 10000, 12000)).all();
    output = [acc.to_dict() for acc in accounts];
    return jsonify(output)

# -- SELECT balance from Racun table for blocked accounts with balance less than -50000 dinara
# SELECT Stanje
# FROM Racun
# WHERE Status = 'B' AND Stanje < -50000;
@application.route('/accounts_blocked_5000')
def get_accounts_blocked_5000():
    accounts = Account.query.filter( and_ (Account.balance<= -50000, Account.status == "B"))
    output = [acc.to_dict() for acc in accounts];
    return jsonify(output)




# -- SELECT all data from Racun table for accounts with positive balance
# SELECT * FROM Racun
# WHERE Stanje > 0;

@application.route("/accounts_positive", methods=["GET"])
def get_accounts_positive():
    accounts = Account.query.filter(Account.balance >=0)
    output = [acc.to_dict() for acc in accounts]
    return jsonify({"accounts": output})



def init_db():
    db_path = os.path.join('instance', 'bank.sqlite3')

    # Ensure the instance directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        with open('init.sql', 'r') as f:
            try:
                conn.executescript(f.read())
            except sqlite3.IntegrityError as e:
                print(f"IntegrityError: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")


if __name__ == "__main__":
    with application.app_context():
        database.drop_all()  # Drop all tables to avoid conflicts
        database.create_all()  # Create tables based on models
        init_db()  # Execute SQL script to initialize the database
    application.run(debug=True)
