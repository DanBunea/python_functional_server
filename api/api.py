import os
import sys
import traceback

from commons import debug
from database_read_services import collect_query_parameters, generate_queries, run_queries
from database_write_services import get_database_object, Session, save_database_object, Article
from lib.flask import jsonify
from transform_services import transform_from_json, transform_to_json

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from flask import Flask, request,jsonify
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import engine

app = Flask(__name__)
from immutable import Immutable, pi_change, change, pi_value, value
from functional import compose_list
from functools import wraps






def service():
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as err:
                traceback.print_exc(file=sys.stdout)
                if isinstance(err, NotImplementedError):
                    return jsonify(errors=["Not implemented error"]), 501
                # elif isinstance(err, basestring):
                #     return jsonify(errors=[err]), 501
                elif hasattr(err[0], "errors"):
                    return jsonify(errors=err[0].errors), 500
                return jsonify(errors=err[0]), 500


        return wrapped
    return wrapper


def to_json(state):
    debug(to_json.__name__, "json:", state.data)
    if len(state.errors) == 0:
        return jsonify(data=state.data)
    else:
        return jsonify(errors=state.errors), 500


@app.route("/api/1/save/Article", methods=["POST"])
@service()
def api_save():
    return save(request.json, get_session())

def save(json, session):

    initial_state = Immutable(data=None, errors=[])

    process = compose_list([
        change("json", json),
        change("session", session),
        change("type", Article),
        get_database_object,
        transform_from_json,
        save_database_object,
        transform_to_json,
        to_json
      ])

    final_state = process(initial_state)


    return final_state




@app.route("/api/1/query/Article", methods=["POST"])
@service()
def api_query():
    return query(request.json, get_session())




def query(json, session):
    initial_state = Immutable(data=None, errors=[])

    process = compose_list([
        change("json", json),
        change("session", session),
        change("type", Article),
        collect_query_parameters,
        generate_queries,
        run_queries
      ])


    # transform("data", "data"),

    final_state = process(initial_state)


    return final_state




def verify_measurement_exists(state):
    if "measurement" not in state.json.keys():
      raise Exception(pi_change("errors",state.errors+["measurement key is missing"], state))
    return state




def get_session():
    return request._get_current_object().db_session

@app.before_request
def before_request():
    request._get_current_object().db_session = Session()



@app.teardown_request
def teardown_request(exception):
    request._get_current_object().db_session.close()






if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')


