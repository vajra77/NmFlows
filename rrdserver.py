from nmflows.backend import RRDBackend
from nmflows.utils.mac_directory import MACDirectory
from flask import Flask, request, make_response, render_template, jsonify
from config import CONFIG
import os


app = Flask(__name__, template_folder='static')


@app.route('/', methods=['GET'])
def index():
    response = make_response(render_template('index.html'), 200)
    return response


@app.route('/directory', methods=['GET'])
def get_directory():
    directory = MACDirectory(CONFIG['ixf_url'])
    entries = []
    for entry in directory:
        entries.append({
            'name': entry.name,
            'asnum': entry.asnum,
            'mac': entry.mac,
            'ipv4_addr': entry.ipv4,
            'ipv6_addr': entry.ipv6
        })
    response = make_response(jsonify(entries), 200)
    return response

@app.route('/as/<asnum>', methods=['GET'])
def asn_summary(asnum):
    period = request.args.get('period')
    proto = request.args.get('proto')
    flows = []
    ifaces = []
    path = CONFIG['rrd_base_path'] + f"/AS{asnum}"
    for fn in os.listdir(path):
        if os.path.isfile(path + '/' + fn):
            if 'flow' in fn:
                tokens = fn.split('__')
                src = tokens[1]
                dst = tokens[3].strip('.rrd')
                flows.append({
                    'filename': fn,
                    'src': src,
                    'dst': dst,
                    'url': f"/flow?src={src}&dst={dst}&period={period}&proto={proto}",
                    'title': f"From {src} to {dst}",
                })
            elif 'peer' in fn:
                tokens = fn.split('__')
                src = tokens[1].strip('.rrd')
                ifaces.append({
                    'filename': fn,
                    'src': src,
                    'url': f"/peer?src={src}&period={period}&proto={proto}",
                    'title': f"Total traffic for {src} interface",
                })
            else:
                pass
    response = make_response(render_template('as.html', asn=asnum, flows=flows, ifaces=ifaces), 200)
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
        backend = RRDBackend(CONFIG['rrd_base_path'], CONFIG['rrd_graph_gamma'])
        data = backend.graph_flow(schedule[period], src, dst, proto)
        response = make_response(data, 200)
        response.headers.set('Content-Type', 'image/png')
        return response
    except FileNotFoundError as e:
        return make_response(render_template("404.html", error=e), 404)
    except Exception as e:
        return make_response(render_template("error.html", error=e), 500)

@app.route('/peer', methods=['GET'])
def get_peer():
    period = request.args.get('period')
    schedule = {
        'daily': 'd',
        'weekly': 'w',
        'monthly': 'm',
        'yearly': 'y',
    }
    src = request.args.get('src')
    proto = request.args.get('proto')

    if proto not in ['ipv4', 'ipv6']:
        return make_response(render_template("error.html", error="unknown protocol"), 500)

    try:
        backend = RRDBackend(CONFIG['rrd_base_path'], CONFIG['rrd_graph_gamma'])
        data = backend.graph_peer(schedule[period], src, proto)
        response = make_response(data, 200)
        response.headers.set('Content-Type', 'image/png')
        return response
    except FileNotFoundError as e:
        return make_response(render_template("404.html", error=e), 404)
    except Exception as e:
        return make_response(render_template("error.html", error=e), 500)
