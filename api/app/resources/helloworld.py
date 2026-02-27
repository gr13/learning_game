from flask_restful import Resource


class HelloWorld(Resource):
    """ The HelloWorld view """
    def __init(self):
        pass

    def get(self):
        """ Returns test screen """
        return {
            "Hello World": "Hello World"
        }
