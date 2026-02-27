from flask_restful import Resource


class HelloWorld(Resource):
    """ The HelloWorld view """
    def __init__(self):
        pass

    def get(self):
        """ Returns test screen """
        return {
            "message": "Hello World"
        }
