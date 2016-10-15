import logging
import requests
import json
from operator import itemgetter

from spyne import Application, srpc, ServiceBase, Iterable, UnsignedInteger, \
    String, Double

from spyne.protocol.json import JsonDocument
from spyne.protocol.http import HttpRpc
from spyne.server.wsgi import WsgiApplication

class ReportCrime(ServiceBase):
    @srpc(Double, Double, Double, _returns=Iterable(String))
    def checkcrime(lat, lon, radius):
        """
        RPC application to check crime report for a location
        :param lat: latitude of a location
        :param lon: longitude of a location
        :param radius: radius distance in miles.
        :returns: crime summary of location
        """
        url = 'https://api.spotcrime.com/crimes.json?lat='+str(lat)+'&lon='+str(lon)+'&radius=' + str(radius) +'&key=.'
        num_streets = 3
        r = requests.get(url)
        content = json.loads(r.text)
        total_crime = len(content['crimes'])
        # For most dangerous streets
        street_dict = {}
        for x in range(0,total_crime):
            for street in content['crimes'][x]['address'].split("BLOCK BLOCK ")[-1].split("BLOCK OF ")[-1].split("BLOCK ")[-1].split(" & "):
                if street in street_dict:
                    street_dict[street] += 1
                else:
                    street_dict[street] = 1
        result = sorted(street_dict.items(), key=itemgetter(1), reverse = True)
        most_dangerous_streets = []
        for i in range(0,num_streets):
            most_dangerous_streets.append(result[i][0].encode('ascii','ignore'))

        crime_dict = {}
        crime_types = []
        for x in range(0,total_crime):
            if content['crimes'][x]['type'] in crime_types:
                continue
            else :
                crime_types.append(content['crimes'][x]['type'].encode('ascii','ignore'))

        for crime in crime_types:
            crime_dict[crime] = 0

        for x in range (0,total_crime):
            crime_dict[content['crimes'][x]['type']] += 1

        time_list = [0]*8
        for x in range(0,total_crime):
            time_of_crime = content['crimes'][x]['date']
            time_float = float(time_of_crime.split(" ")[-2].replace(":","."))
            if time_of_crime.split(" ")[-1] == 'AM':
                if time_float == 12.0:
                    time_float += 12
                elif time_float > 12.0:
                    time_float -= 12
            else:
                if time_float < 12.0:
                    time_float += 12
            time_float = time_float - 0.01
            time_list[int(time_float/3)] += 1

        crime_summary = {
            "total_crime" : total_crime,
            "the_most_dangerous_streets" : [ street for street in most_dangerous_streets],
            "crime_type_count" : crime_dict,
            "event_time_count" : {
                "12:01am-3am" : time_list[0],
                "3:01am-6am" : time_list[1],
                "6:01am-9am" : time_list[2],
                "9:01am-12noon" : time_list[3],
                "12:01pm-3pm" : time_list[4],
                "3:01pm-6pm" : time_list[5],
                "6:01pm-9pm" : time_list[6],
                "9:01pm-12midnight" : time_list[7]
            }
        }
        yield "%s" % crime_summary

if __name__ == '__main__':
    # Python daemon boilerplate
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)

    application = Application([ReportCrime], 'spyne.examples.hello.http',
        in_protocol=HttpRpc(validator='soft'),
        out_protocol=JsonDocument(ignore_wrappers=True),
    )

    wsgi_application = WsgiApplication(application)

    # More daemon boilerplate
    server = make_server('127.0.0.1', 8000, wsgi_application)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server.serve_forever()
