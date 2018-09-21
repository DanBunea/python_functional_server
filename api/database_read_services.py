import os
import sys

from commons import debug
from database_write_services import Comment
from immutable import change

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

from sqlalchemy.orm.attributes import InstrumentedAttribute

from immutable import change


def collect_properties_and_relations(query_parameters, json, type_dict):
    for json_property in json:
        if isinstance(json_property, basestring):
            if type_dict.has_key(json_property) and isinstance(type_dict[json_property], InstrumentedAttribute):
                query_parameters["properties"].append(type_dict[json_property])
        elif isinstance(json_property,dict):
            relation = json_property.keys()[0]
            relation_properties = json_property[relation]

            collect_properties_and_relations(query_parameters, relation_properties, Comment.__dict__)
            query_parameters["joins"].append(type_dict[relation])

            return



def collect_query_parameters(state):
    query_parameters = {"properties":[],
                        "joins":[],
                        "conditions":[]}
    type_dict = state.type.__dict__

    collect_properties_and_relations(query_parameters, state.json["find"],type_dict)

    for where_key in state.json["where"].keys():
        val = state.json["where"][where_key]
        query_parameters["conditions"].append(type_dict[where_key]==val)

    query_parameters["first_property"]=query_parameters["properties"][0]
    return change("query_parameters", query_parameters)(state)



def generate_queries(state):
    query_parameters = state.query_parameters
    session = state.session
    properties = query_parameters["properties"]
    joins = query_parameters["joins"]
    where_clauses = query_parameters["conditions"]
    first_property = properties[0]

    query_ids = session.query(first_property).outerjoin(*joins)
    query = session.query(*properties).outerjoin(*joins)

    for where_clause in where_clauses:
        query_ids = query_ids.filter(where_clause)

    query = query.group_by(*properties)
    query_ids = query_ids.group_by(first_property)

    return change("queries", dict(query_ids=query_ids, query=query, first_property=first_property))(state)



def run_queries(state):
    debug("run_queries")
    queries = state.queries
    query_ids = queries["query_ids"]
    query = queries["query"]
    first_property=queries["first_property"]
    debug("    query_ids", str(query_ids))

    ids = query_ids.all()
    if len(ids)>0:
        query = query.filter(first_property.in_(map(lambda id:id[0],ids)))
        debug("    query", str(query))
        results = query.all()
    else:
        results=[]


    return change("data",results)(state)
