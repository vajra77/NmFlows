from nmflows.backend import RRDBackend
from flask import Flask, request, make_response, render_template
from config import CONFIG


app = Flask(__name__, template_folder='static')


@app.route('/', methods=['GET'])
def index():
    response = make_response(render_template('index.html'), 200)
    return response

@app.route('/flow', methods=['GET'])
def get_flow():
    period = request.args.get('period')
    schedule = {
        'daily': 'd',
        'weekly': 'w',
        'monthly': 'm',
        'yearly': 'y',
    }
    src = request.args.get('src')
    dst = request.args.get('dst')
    proto = request.args.get('proto')

    if proto not in ['ipv4', 'ipv6']:
        return make_response(render_template("error.html", error="unknown protocol"), 500)

    try:
        backend = RRDBackend(CONFIG['rrd_base_path'])
        data = backend.graph_flow(schedule[period], src, dst, proto)
        response = make_response(data, 200)
        response.headers.set('Content-Type', 'image/png')
        return response
    except FileNotFoundError as e:
        return make_response(render_template("404.html", error=e), 404)
    except Exception as e:
        return make_response(render_template("error.html", error=e), 500)
