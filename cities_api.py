from flask import Flask, request
from flask_restful import Api, Resource

from utilities.db_tools import DBMaster

app = Flask(__name__)
api = Api(app)


class CitiesAPI(Resource):
    def get(self):
        params = request.get_json()
        if len(params) == 0:
            return 'Bad request', 400
        try:
            city_name = params['CityName'].lower()
        except KeyError:
            return 'Bad request', 400
        prov_filt_nest = ''
        prov_filt = ''
        year_filt = 9999
        if 'year' in params.keys():
            try:
                year_filt = int(params["year"])
            except ValueError:
                return 'Bad request', 400
        if 'includeProvisional' in params.keys():
            prov_val = params['includeProvisional']
            if prov_val not in ('true', 'false'):
                return 'Bad request', 400
            elif prov_val == 'false':
                prov_filt_nest = 'AND reliability = "Final figure, complete" '
                prov_filt = 'AND p.reliability = "Final figure, complete" '
        query_path = 'db_files/queries/city_population.sql'
        with open(query_path, 'r') as query_file:
            query_base = query_file.read()
        with DBMaster('cities_api_db') as dbm:
            sql_res = dbm.fetch_data(query=query_base.format(city_name, year_filt, prov_filt_nest, prov_filt))
        return {'population': sql_res[0][0]}

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(CitiesAPI, '/api')

if __name__ == '__main__':
    app.run()
