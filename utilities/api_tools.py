from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class CitiesAPI(Resource):
    def get(self):
        params = request.get_json()
        return params

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(CitiesAPI, '/api')

if __name__ == '__main__':
    app.run()
