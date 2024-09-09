from datetime import datetime
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from adapters import repository

from domain import model
import config
from adapters import orm
import service_layer.services as services

app = Flask(__name__)


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))


@app.route("/add_batch", methods=["POST"])
def add_batch():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    eta = request.json["eta"]
    if eta is not None:
        eta = datetime.fromisoformat(eta).date()
    services.add_batch(
        request.json["ref"],
        request.json["sku"],
        request.json["qty"],
        eta,
        repo,
        session,
    )
    return "OK", 201


@app.route("/allocate", methods=["POST"])
def allocate_endpoint():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        batchref = services.allocate(
            request.json["orderid"],
            request.json["sku"],
            request.json["qty"],
            repo, 
            session,
        )
    except (model.OutOfStock, services.InvalidSku) as e:
        return {'message': str(e)}, 400
    
    return {'batchref': batchref}, 201