import json

from PyQt5.QtCore import QUrl, QUrlQuery
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest


class Http:
    def __init__(self):
        self.manager = QNetworkAccessManager()

    def get(self, url, params: dict, headers, func=None, func_param_number=1):
        try:
            url = QUrl(url)
            query = QUrlQuery()
            for k, v in params.items():
                query.addQueryItem(k, v)
            url.setQuery(query)
            request = QNetworkRequest(url)
            for k, v in headers.items():
                request.setRawHeader(k.encode(), v.encode())
            reply = self.manager.get(request)
            if func_param_number < 0 or func_param_number > 1:
                return
            if func:
                if func_param_number == 0:
                    reply.finished.connect(lambda: func())
                elif func_param_number == 1:
                    reply.finished.connect(lambda: func(reply))
        except Exception as e:
            print(e)

    def post(self, url, data: dict, headers, func=None):
        try:
            url = QUrl(url)
            request = QNetworkRequest(url)
            for k, v in headers.items():
                request.setRawHeader(k.encode(), v.encode())
            json_data = bytes(json.dumps(data), encoding='utf-8')
            reply = self.manager.post(request, json_data)
            if func:
                reply.finished.connect(lambda: func(reply))
        except Exception as e:
            print(e)
