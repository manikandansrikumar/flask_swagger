import os
from flask import Flask, jsonify, request
import psutil
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.wrappers import response

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Flask-REST"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

@app.route('/cpu_utilization')
def cpu():
    # Calling psutil.cpu_precent() for 4 seconds
    ### cpu = {'The CPU usage is' : psutil.cpu_percent(4)}

    response = {}
    # let's print CPU information
    print("="*40, "CPU Info", "="*40)
    # number of cores
    response["Physical cores"] = psutil.cpu_count(logical=False)
    response["Total cores"] = psutil.cpu_count(logical=True)
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(response)
    response["Max Frequency"] = f"{cpufreq.max:.2f}Mhz"
    response["Min Frequency"] = f"{cpufreq.min:.2f}Mhz"
    response["Current Frequency"] = f"{cpufreq.current:.2f}Mhz"
    # CPU usage
    
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    response["Total CPU Usage"] = f"{psutil.cpu_percent()}%"
    return jsonify(response)


@app.route('/memory_utilization')
def ram():
# Getting % usage of virtual_memory ( 3rd field)
    ram = {'RAM memory % used' : psutil.virtual_memory()[2]}

    response = {}

    # Memory Information
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    response["Total"]  = f"{get_size(svmem.total)}"
    response["Available"] = f"{get_size(svmem.available)}"
    response["Used"] = f"{get_size(svmem.used)}"
    response["Percentage"] =  f"{svmem.percent}%"
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    # swap = psutil.swap_memory()
    # response["Total"] = f"{get_size(swap.total)}"
    # response["Free"] =  f"{get_size(swap.free)}"
    # response["Used"] = f"{get_size(swap.used)}"
    # response["Percentage"] = f"{swap.percent}%"
    return jsonify(response)

@app.route('/execute_in_target', methods=['GET', 'POST'])
def command():
    if request.method == "POST":
        cmd = request.json.get('command')
        print(cmd, '********')
        os.system(cmd)
        # import subprocess
        # process = subprocess.run(['dir', 'Even more output'], 
        #                  stdout=subprocess.PIPE, 
        #                  universal_newlines=True)
        # print(process)
        # print('&&&&&')
        response = {'message': 'command executed successfully'}
        return jsonify(response)

@app.route('/ping')
def pong():
    return "<h1>Ping Pong</h1>"

if __name__ == '__main__':
    app.run(debug=True)