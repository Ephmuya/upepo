import json
import api
import decimal
#FOR JSON AUTO

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

get_readings  = "WITH LATEST_READINGS AS(Select m.Id AS MeterID, m.Longitude AS Longitude, m.Latitude AS Latitude, m.IMENumber AS IMEI, max(r.TimeTaken) " \
                "as TIME, max(r.Id) AS ID from Meters m join MeterReadings r on m.Id = r.MeterId " \
                "group by m.Id, m.IMENumber, m.Latitude, m.Longitude) SELECT MeterReadings.*, LATEST_READINGS.MeterID,LATEST_READINGS.Latitude, LATEST_READINGS.Longitude FROM MeterReadings " \
                "INNER JOIN LATEST_READINGS ON LATEST_READINGS.ID = MeterReadings.Id order by MeterReadings.TimeTaken desc"

cursor = api.db_access()
cursor.execute(get_readings)
row_headers=[x[0] for x in cursor.description] #this will extract row headers
rv = cursor.fetchall()
json_data=[]
for result in rv:
    json_data.append(dict(zip(row_headers,result)))

data =json.dumps(json_data, cls= DecimalEncoder ,default=str , indent=4)
json = json.loads(data)
converted =[]
for i in json:
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
    TimeTaken = i['TimeTaken']
    WaterTemperature = i['WaterTemperature']

    if Latitude != '':
        try:
            converted_data = {
                "AccumulatedEffectiveRunningTime": float(AccumulatedEffectiveRunningTime),
                "AccumulatedFlowRate": float(AccumulatedFlowRate),
                "BateryVoltage": float(BateryVoltage),
                "DaillyFowRate": float(DaillyFowRate),
                "Id": Id,
                "InstantaneousFlowRate": float(InstantaneousFlowRate),
                "LowestFlowRate": float(LowestFlowRate),
                "Humidity": float(Humidity),
                "MeterID": MeterID,
                "PeakFlowRate": float(PeakFlowRate),
                "Status": float(Status),
                "TimeTaken": TimeTaken,
                "WaterTemperature": float(WaterTemperature),
                "Latitude": float(Latitude),
                "Longitude": float(Longitude),

            }
            converted.append(converted_data)
        except ValueError:
            pass


print(converted)