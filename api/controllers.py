import logging
import requests
import time
import json
import arrow
import decimal
from api.model import db_access
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

@upepo.route('/latest')
def latest_readings():
    try:
        readings = "https://bahari2dev.azurewebsites.net/api/Test/Readings"
        readings_data = requests.request("GET", url=readings)
        output = readings_data.json()
        current_day = arrow.now().format('YYYY-MM-DD')
        current = []
        for i in output:
            time_obj = time.strptime(i['timeTaken'], "%Y-%m-%dT%H:%M:%S")
            json_day = time.strftime("%Y-%m-%d", time_obj)
            # compare current day with json
            if str(json_day) == current_day:
                current.append(lower_key(i))
        return jsonify(current)

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

@upepo.route('/current_readings')
def current():
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                return float(o)
            return super(DecimalEncoder, self).default(o)

    get_readings = "WITH LATEST_READINGS AS(Select m.Id AS MeterID, m.ZoneId AS ZoneID, m.Longitude AS Longitude, m.Latitude AS Latitude, max(r.TimeTaken) " \
                   "as TIME, max(r.Id) AS ID from Meters m join MeterReadings r on m.Id = r.MeterId " \
                   "group by m.Id, m.ZoneID, m.Latitude, m.Longitude) SELECT MeterReadings.*, LATEST_READINGS.MeterID,LATEST_READINGS.ZoneId,LATEST_READINGS.Latitude, LATEST_READINGS.Longitude FROM MeterReadings " \
                   "INNER JOIN LATEST_READINGS ON LATEST_READINGS.ID = MeterReadings.Id order by MeterReadings.TimeTaken desc"

    cursor = db_access()
    cursor.execute(get_readings)
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))

    data = json.dumps(json_data, cls=DecimalEncoder, default=str, indent=4)
    _json = json.loads(data)
    converted = []
    for i in _json:
        AccumulatedEffectiveRunningTime = i['AccumulatedEffectiveRunningTime']
        AccumulatedFlowRate = i['AccumulatedFlowRate']
        BateryVoltage = i['BateryVoltage']
        DaillyFowRate= i['DaillyFowRate']
        Humidity = i['Humidity']
        Id = i['Id']
        InstantaneousFlowRate = i['InstantaneousFlowRate']
        Latitude = i['Latitude']
        Longitude = i['Longitude']
        LowestFlowRate = i['LowestFlowRate']
        MeterID = i['MeterID']
        PeakFlowRate = i['PeakFlowRate']
        SignalStrength = i['SignalStrength']
        Status = i['Status']
        ZoneId = i['ZoneId']
        TimeTaken = i['TimeTaken']
        WaterTemperature = i['WaterTemperature']

        if Latitude != '':
            try:
                converted_data = {
                    "accumulatedeffectiverunningtime": float(AccumulatedEffectiveRunningTime),
                    "accumulatedflowtate": float(AccumulatedFlowRate),
                    "batteryvoltage": float(BateryVoltage),
                    "dailyflowrate": float(DaillyFowRate),
                    "id": Id,
                    "instantaneousflowfate": float(InstantaneousFlowRate),
                    "lowestflowrate": float(LowestFlowRate),
                    "humidity": float(Humidity),
                    "meterid": MeterID,
                    "signalstrength": float(SignalStrength),
                    "peakflowrate": float(PeakFlowRate),
                    "status": float(Status),
                    "zoneid": ZoneId,
                    "timetaken": TimeTaken,
                    "watertemperature": float(WaterTemperature),
                    "Latitude": float(Latitude),
                    "Longitude": float(Longitude),

                }
                converted.append(converted_data)
            except ValueError:
                pass

    return jsonify(converted)

def response(status=400, result=None, warnings=None, error=None):
    return jsonify(status=status, result=result, warnings=warnings, error=error), status
