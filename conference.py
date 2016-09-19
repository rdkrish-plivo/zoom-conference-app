from flask import Flask, Response, request, make_response, render_template
import plivo
import plivoxml

from configmanager import config

app = Flask(__name__)

auth_id = config['Plivo']['auth_id']
auth_token = config['Plivo']['auth_token']


@app.route('/response/conference/', methods=['GET', 'POST'])
def conference():
    response = plivoxml.Response()
    response.addSpeak(
        'You will be transferred to the zoom conference number. \
        Hold on for a second')
    dial = response.addDial()
    dial.addNumber(config['Zoom']['number'])
    params = {
        'enterSound': 'beep:2',
        'record': 'true',
        'method': 'GET',
        'callbackMethod': 'GET',
        'callbackUrl': config['App']['url'] + '/response/conf_callback',
    }
    conference_name = 'demoConference'  # Conference Room name
    response.addConference(conference_name, **params)
    return Response(str(response), mimetype='text/xml')


@app.route('/response/conf_callback/', methods=['GET', 'POST'])
def conf_callback():
    response = make_response('OK')
    response.headers['Content-type'] = 'text/plain'
    return response


@app.route('/create_conference', methods=['GET'])
def create_conference():
    answer_url = config['App']['url'] + '/response/conference'
    p = plivo.RestAPI(auth_id, auth_token)
    call_params = {
        'to': request.values['phone'],
        'from': config['Plivo']['number'],
        'answer_url': answer_url,
        'answer_method': 'GET'
    }
    r = p.make_call(call_params)
    response = make_response('Conference created!')
    response.headers['Content-type'] = 'text/plain'
    return response


@app.route('/response/done_conference', methods=['GET'])
def done_conference():
    p = plivo.RestAPI(auth_id, auth_token)
    p.hangup_all_conferences()
    return Response('Conference ended')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
