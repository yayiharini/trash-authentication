import pyodbc
from geopy.geocoders import Nominatim
import requests


def location():
    conn = pyodbc.connect(
        'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;')
    cursor = conn.cursor()

    cursor.execute("select * from Test.record_main where y_value!=0.0")
    result = cursor.fetchall()
    print("result", result)
    for row in result:
        x = row.x_value
        y = row.y_value
        id = row.RecordID


        #  WaterShed
        url = "https://services.arcgis.com/aa38u6OgfNoCkTJ6/arcgis/rest/services/HUC8_CA_Simplified/FeatureServer/0" \
              "/query?where=1%3D1&outFields=Name,HUC8&geometryType=esriGeometryPoint&" \
              "geometry={0},{1}&inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json".format(x, y)
        response = requests.get(url)
        if response.status_code == 200:

            try:

                name = response.json()['features'][0]['attributes']['Name']
                huc8 = response.json()['features'][0]['attributes']['HUC8']
            except Exception as e:

                name = ''
                huc8 = ''
            print(name, huc8)
        else:
            name = ''
            huc8 = ''

        # Waterboard
        water_board_url = f"https://services1.arcgis.com/8CpMUd3fdw6aXef7/arcgis/rest/services/RWQCB_bndy/FeatureServer/0/" \
                        f"query?where=1%3D1&outFields=RB,RB_NAME,AgencyOffice&geometryType=esriGeometryPoint&geometry={x},{y}&" \
                        f"inSR=4326&spatialRel=esriSpatialRelIntersects&outSR=4326&f=json"

        res = requests.get(water_board_url)
        if res.status_code == 200:
            print("entered board 200", id)
            try:
                print("entered board try", id)
                water_board_name = res.json()['features'][0]['attributes']['RB_NAME']
            except Exception as e:
                print("entered board e", id)
                print(e)
                water_board_name = ''

        else:
            water_board_name = ''
        print("waterboard", water_board_name)

        # Citycounty

        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(str(y) + "," + str(x))
        if location is None:
            continue
        address = location.raw['address']
        if address is None:
            continue
        city = address.get('city', '')
        state = address.get('state', '')
        county = address.get('county', '')
        town = address.get('town', '')
        if city == "":
            city = town

        connection = pyodbc.connect(
            'Driver= {ODBC Driver 17 for SQL Server};SERVER=UL-ARC1003-1416;DATABASE=TradeDB;UID=project_user;PWD=project_password;Trusted_Connection=yes;')
        cursor = connection.cursor()
        val = cursor.execute(
            "update Test.record_main set city='" + city + "',county='" + county + "',HUC8_code='" + huc8 + "',"
                                                                                                           "Watershed_Name='" + name + "',Waterboard_Name='" + water_board_name + "' where x_value=" + str(
                x) + " and y_value=" + str(y))
        connection.commit()
        print(val)
        print('city', city)
        print('county', county)
    # print(result)
