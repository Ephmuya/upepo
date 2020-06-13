import logging
import requests
import json
from flask import jsonify ,Blueprint

upepo = Blueprint("upepo", __name__)
logger = logging.getLogger(__name__)


def lower_key(in_dict):
    if type(in_dict) is dict:
        out_dict = {}
        for key, item in in_dict.items():
            out_dict[key.lower()] = lower_key(item)
        return out_dict
    elif type(in_dict) is list:
        return [lower_key(obj) for obj in in_dict]
    else:
        return in_dict


@upepo.route('/readings')
def readings():
    try:
        readings = "https://bahari2dev.azurewebsites.net/api/Test/Readings"
        readings_data = requests.request("GET", url=readings)
        output = readings_data.json()
        readings_lower = []
        for i in output:
            readings_lower.append(lower_key(i))
        return jsonify(readings_lower)

    except Exception as e:
        logger.error(e)
        return response(error=str(e))


@upepo.route('/meters')
def meters():
    meters = "https://bahari2dev.azurewebsites.net/api/Test/Meters"
    meters_data = requests.request("GET", url=meters)
    output = meters_data.json()
    meters_lower = []
    for i in output:
        meters_lower.append(lower_key(i))
    return jsonify(meters_lower)


def response(status=400, result=None, warnings=None, error=None):
    return jsonify(status=status, result=result, warnings=warnings, error=error), status
