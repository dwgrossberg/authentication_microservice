from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import csv


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config.from_object(Config())


CORS(app)


@app.route('/authentication', methods=['POST'])
@cross_origin()
def authenticate():
    data = request.get_json()  # {IP address, is_human? <bool>}
    with open(data.csv, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if data in row:
                return redirect(url_for('human'))
    return redirect(url_for('not_human'))


@app.route('/whitelist', methods=['POST'])
@cross_origin()
def whitelist():
    data = request.get_json()  # {IP address, is_human? <bool>}
    with open(data.csv, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([data])
    return redirect(url_for('human'))


@app.route('/not_human', methods=['GET'])
@cross_origin()
def not_human():
    data = 'Not human'
    return jsonify(data)


@app.route('/human', methods=['GET'])
@cross_origin()
def human():
    data = 'Verified human'
    return jsonify(data)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
