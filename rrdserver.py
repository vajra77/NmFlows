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
    src_asn, src_mac = src.split('-')
    dst_asn, dst_mac  = dst.split('-')
    try:
        backend = RRDBackend(CONFIG['rrd_base_path'])
        data = backend.graph_flow(schedule[period], src_asn, src_mac, dst_asn, dst_mac)
        response = make_response(data, 200)
        response.headers.set('Content-Type', 'image/png')
        return response, 200
    except FileNotFoundError:
        return make_response(render_template("404.html"), 404)
    except Exception as e:
        return make_response(render_template("error.html", error=e), 500)
