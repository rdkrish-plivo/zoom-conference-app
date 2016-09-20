from flask import Flask, Response, request, make_response, render_template
import plivo
import plivoxml

from configmanager import config

app = Flask(__name__)


@app.route('/response/conference/', methods=['GET', 'POST'])
def conference():
    response = plivoxml.Response()
    response.addSpeak('Hold on for a second')
    dial = response.addDial()
    params = {
        'sendDigits': 'W' * 10 + request.values['meeting_id'] + '#' + 'W' * 8 + '#'
    }
    dial.addNumber(config['Zoom']['number'], **params)
    return Response(str(response), mimetype='text/xml')


@app.route('/create_conference', methods=['GET'])
def create_conference():
    answer_url = config['App']['url'] + '/response/conference/?meeting_id=' + request.values['meeting_id']
    call_params = {
        'to': request.values['phone'],
        'from': config['Plivo']['number'],
        'answer_url': answer_url,
        'answer_method': 'GET'
    }
    plivoApi.make_call(call_params)
    response = make_response('Conference created!')
    response.headers['Content-type'] = 'text/plain'
    return response


@app.route('/response/done_conference/', methods=['GET'])
def done_conference():
    plivoApi.hangup_all_conferences()
    return Response('Conference ended')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    auth_id = config['Plivo']['auth_id']
    auth_token = config['Plivo']['auth_token']
    plivoApi = plivo.RestAPI(auth_id, auth_token)
    app.run(host='0.0.0.0', debug=True)
