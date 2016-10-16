# cmpe273-lab2

Simple RPC application to check crime report for a location using Spyne toolkit.

<b> Input (HttpRpc) </b>

* lat - latitude of a location
* lon - longitude of a location
* radius - radius distance in miles.

curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=0.02"

<b> Output (Json) </b>

{
    "total_crime" : 24,
    "the_most_dangerous_streets" : [ "E SANTA CLARA ST", "E SAN FERNANDO ST" , "N 11TH ST" ],
    "crime_type_count" : {
        "Assault" : 10,
        "Arrest" : 8,
        "Burglary" : 6,
        "Robbery" : 4,
        "Theft" : 2,
        "Other" : 1
    },
    "event_time_count" : {
        "12:01am-3am" : 5,
        "3:01am-6am" : 0,
        "6:01am-9am" : 1,
        "9:01am-12noon" : 2,
        "12:01pm-3pm" : 2,
        "3:01pm-6pm" : 1,
        "6:01pm-9pm" : 0,
        "9:01pm-12midnight" : 9
    } 
}

<b> Steps to be followed:</b>
* <b> easy_install spyne</b>

* To start the server: <b>python crime_report.py</b>

* Use <b>curl "http://localhost:8000/checkcrime?lat=37.334164&lon=-121.884301&radius=0.02"</b> to test the application
