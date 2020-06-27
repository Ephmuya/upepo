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
                "group by m.Id, m.IMENumber) SELECT MeterReadings.*, LATEST_READINGS.MeterID FROM MeterReadings " \
                "INNER JOIN LATEST_READINGS ON LATEST_READINGS.ID = MeterReadings.Id order by MeterReadings.TimeTaken desc"

cursor = api.db_access()
cursor.execute(get_readings)
row_headers=[x[0] for x in cursor.description] #this will extract row headers
rv = cursor.fetchall()
json_data=[]
for result in rv:
    json_data.append(dict(zip(row_headers,result)))

data =json.dumps(json_data, cls= DecimalEncoder ,default=str , indent=4)
cow = json.loads(data)
print(cow)

