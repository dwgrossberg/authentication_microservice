from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import csv


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__, static_folder='frontend', static_url_path='')
app.config.from_object(Config())


CORS(app)


def check_in_csv(s):
    with open('data.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if s in row:
                return True
        return False


@app.route('/authentication', methods=['POST'])
@cross_origin()
def authenticate():
    data = request.get_json()  # {IP address}
    print(data)
    if check_in_csv(data["IP"]):
        # IP already on file
        return jsonify({'message': 'Human authenticated'})
    # IP must be authenticated
    return jsonify({'message': 'Not authenticated'})


@app.route('/whitelist', methods=['POST'])
@cross_origin()
def whitelist():
    data = request.get_json()  # {IP address, is_human? <bool>}
    # check for is_human identifier
    if not data['is_human']:
        return jsonify({'message': 'Not authenticated'})
    # save IP for future checks
    with open('data.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([data["IP"]])
    return jsonify({'message': 'Human authenticated'})


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run()
