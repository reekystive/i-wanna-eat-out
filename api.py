import flask
import json
from oa import OAConfig, OA

server = flask.Flask('apply')


@server.route('/apply', methods=['get', 'post'])
def apply():
    username = flask.request.values.get('username')
    password = flask.request.values.get('password')

    if (not username) or (not password):
        info = {'code': 1001, 'message': 'parameter error'}
        print(info)
        return json.dumps(info, ensure_ascii=False)
    else:
        info = {}
        config = OAConfig(str(username), str(password))
        obj = OA(config)
        obj.login()
        if (not obj.is_logged_in):
            info = {'code': 1002,
                    'message': 'username or password is incorrect'}
            print(info)
            return json.dumps(info, ensure_ascii=False)
        obj.login_oa()
        obj.apply()
        info = {'code': 2001, 'message': 'success'}
        print(info)
        return json.dumps(info, ensure_ascii=False)


if __name__ == '__main__':
    server.run(debug=False, port=6991, host='0.0.0.0')
