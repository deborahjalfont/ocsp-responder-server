from werkzeug.wrappers import Request, Response
from jsonrpc import JSONRPCResponseManager


class RPCServerRequest(object):
    def __init__(self):
        self.dispatcher = {}

    def register(self, **kwargs):
        self.dispatcher.update(kwargs)

    @Request.application
    def application(self, request):
        response = JSONRPCResponseManager.handle(request.data, self.dispatcher)
        return Response(response.json, mimetype="application/json")
