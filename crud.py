from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Derivative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pricePerUnit = db.Column(db.String(80), unique=True)
    currency = db.Column(db.String(2), unique=True)
    riskLevel = db.Column(db.String(16), unique=True)
    trend = db.Column(db.String(15), unique=True)
    duration = db.Column(db.Integer, unique=True)
    emitent = db.Column(db.String(80), unique=True)
    owner = db.Column(db.String(80), unique=True)
    asset = db.Column(db.String(80), unique=True)

    def __init__(self,
                 pricePerUnit=0, currency="$",
                 riskLevel=None, trend=None,
                 duration=0, emitent="NoEmitent",
                 owner="NoOwner",asset="NoAsset"
                 ):
        self.pricePerUnit = pricePerUnit
        self.currency = currency
        self.riskLevel = riskLevel
        self.trend = trend
        self.duration = duration
        self.emitent = emitent
        self.owner = owner
        self.asset = asset

    def __str__(self):
        return ', '.join((f"{name} = {value}" for name, value in self.__dict__.items()))

class DerivativeSchema(ma.Schema):
    class Meta:
        fields = (
            'pricePerUnit', 'currency',
            'riskLevel', 'trend', 'duration',
            'emitent', 'owner', 'asset'
        )


derivative_schema = DerivativeSchema()
derivatives_schema = DerivativeSchema(many=True)


# endpoint to create new derivative
@app.route("/derivative", methods=["POST"])
def add_derivative():
    pricePerUnit = request.json['pricePerUnit']
    currency = request.json['currency']
    riskLevel = request.json['riskLevel']
    trend = request.json['trend']
    duration = request.json['duration']
    emitent = request.json['emitent']
    owner = request.json['owner']
    asset = request.json['asset']

    new_derivative = Derivative(
        pricePerUnit, currency,
        riskLevel, trend, duration,
        emitent, owner, asset
        )

    db.session.add(new_derivative)
    db.session.commit()

    return jsonify(new_derivative)


# endpoint to show all derivatives
@app.route("/derivative", methods=["GET"])
def get_derivative():
    all_derivatives = Derivative.query.all()
    result = derivatives_schema.dump(all_derivatives)
    return jsonify(result.data)


# endpoint to get derivative detail by id
@app.route("/derivative/<id>", methods=["GET"])
def derivative_detail(id):
    derivative = Derivative.query.get(id)
    return derivative_schema.jsonify(derivative)


# endpoint to update derivative
@app.route("/derivative/<id>", methods=["PUT"])
def derivative_update(id):
    derivative = Derivative.query.get(id)
    derivative.pricePerUnit = request.json['pricePerUnit']
    derivative.currency = request.json['currency']
    derivative.riskLevel = request.json['riskLevel']
    derivative.trend = request.json['trend']
    derivative.duration = request.json['duration']
    derivative.emitent = request.json['emitent']
    derivative.owner = request.json['owner']
    derivative.asset = request.json['asset']

    db.session.commit()
    return derivative_schema.jsonify(derivative)


# endpoint to delete derivative
@app.route("/derivative/<id>", methods=["DELETE"])
def derivative_delete(id):
    derivative = Derivative.query.get(id)
    db.session.delete(derivative)
    db.session.commit()

    return derivative_schema.jsonify(derivative)


if __name__ == '__main__':
    app.run(debug=True)
