from dateutil.parser import isoparse
from geopy.geocoders import Nominatim
from math import sqrt
import math
import time
from flask import Flask, request
from xml.dom.minidom import parse
import xml.dom.minidom

app = Flask(__name__)


@app.route('/')
def data_set():
    """
    Return the entire data set
    :return: the entire data set
    """
    return dic


@app.route('/epochs/')
def get_epochs():
    """
    Return a list of all Epochs in the data set
    :return: a list of all Epochs
    """
    epochs = []
    for data in dic:
        epochs.append(data['EPOCH'])
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    print(f"epochs offset:{offset}, limit:{limit}")
    if offset and limit:
        try:
            offset = int(offset)
            limit = int(limit)
            return epochs[offset:offset+limit]
        except ValueError as e:
            return f"Exception occurred:{e}, will not send epochs for current query"
    elif offset or limit:
        return f"Not supporting single value provided, please provide both offset and limit"
    else:
        return epochs


@app.route('/epochs/<epoch>/')
def get_epoch_data(epoch: str):
    """
    Return state vectors for a specific Epoch from the data set
    :param epoch: specific Epoch
    :return: state vectors
    """
    for data in dic:
        if data['EPOCH'] == epoch:
            res = data.copy()
            res.pop('EPOCH')
            return res


@app.route('/epochs/<epoch>/speed')
def get_epoch_speed(epoch: str):
    """
    Return instantaneous speed for a specific Epoch in the data set
    :param epoch: specific Epoch
    :return: instantaneous speed
    """
    for data in dic:
        if data['EPOCH'] == epoch:
            res = sqrt(data['X_DOT'] ** 2 + data['Y_DOT']
                       ** 2 + data['Z_DOT'] ** 2)
            return str(res)


def read_file_stateVector(filename: str):
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    vectors = collection.getElementsByTagName("stateVector")
    res = []
    for vector in vectors:
        data = {}
        EPOCH = vector.getElementsByTagName('EPOCH')[0]
        X = vector.getElementsByTagName('X')[0]
        Y = vector.getElementsByTagName('Y')[0]
        Z = vector.getElementsByTagName('Z')[0]
        X_DOT = vector.getElementsByTagName('X_DOT')[0]
        Y_DOT = vector.getElementsByTagName('Y_DOT')[0]
        Z_DOT = vector.getElementsByTagName('Z_DOT')[0]
        data['EPOCH'] = EPOCH.childNodes[0].data
        data['X'] = float(X.childNodes[0].data)
        data['Y'] = float(Y.childNodes[0].data)
        data['Z'] = float(Z.childNodes[0].data)
        data['X_DOT'] = float(X_DOT.childNodes[0].data)
        data['Y_DOT'] = float(Y_DOT.childNodes[0].data)
        data['Z_DOT'] = float(Z_DOT.childNodes[0].data)
        res.append(data)
    return res


@app.route('/comment')
def get_comment():
    """
    Return comment of whole file
    :return: comment
    """
    return comment


@app.route('/help')
def help_doc():
    """
    Return the help message
    :return: the help message string
    """
    table_doc = """
    usage: http://host:port&lt;Route&gt;
    <table>
	<tbody>
		<tr>
			<td>Route</td>
			<td>Method</td>
			<td>Explain</td>
		</tr>
		<tr>
			<td>/</td>
			<td>GET</td>
			<td>Return entire data set</td>
		</tr>
		<tr>
			<td>/epochs</td>
			<td>GET</td>
			<td>Return list of all Epochs in the data set</td>
		</tr>
  		<tr>
			<td>/epochs?limit=int&offset=int</td>
			<td>GET</td>
			<td>Return modified list of Epochs given query parameters</td>
		</tr>
  		<tr>
			<td>/epochs/<epoch></td>
			<td>GET</td>
			<td>Return state vectors for a specific Epoch from the data set</td>
		</tr>
  		<tr>
			<td>/epochs/<epoch>/speed</td>
			<td>GET</td>
			<td>Return instantaneous speed for a specific Epoch in the data set</td>
		</tr>
  		<tr>
			<td>/help</td>
			<td>GET</td>
			<td>Return help text (as a string) that briefly describes each route</td>
		</tr>
  		<tr>
			<td>/delete-data</td>
			<td>DELETE</td>
			<td>Delete all data from the dictionary object</td>
		</tr>
        <tr>
			<td>/post-data</td>
			<td>POST</td>
			<td>Reload the dictionary object with data from the web</td>
		</tr>
	</tbody>
    </table>
    """
    return table_doc


@app.route('/delete-data', methods=['DELETE'])
def delete_data():
    dic.clear()
    return dic


@app.route('/post-data', methods=['POST'])
def post_data():
    dic = request.get_data(request.form)
    return dic


def read_comment(filename: str):
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    vectors = collection.getElementsByTagName('COMMENT')
    res = []
    for vector in vectors:
        if vector.firstChild:
            res.append(vector.firstChild.data)
        else:
            res.append("")
    return res


def read_header(filename: str):
    """
    Return header of whole file
    :return: header
    """
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    vectors = collection.getElementsByTagName('header')[0].childNodes
    print(vectors)
    res = {}
    for vector in vectors:
        if vector.nodeType == 1:
            print(f"{vector.tagName}, {vector.firstChild.data}")
            res[vector.tagName] = vector.firstChild.data
    return res


def read_metadata(filename: str):
    """
    Return metadata of whole file
    :return: header
    """
    DOMTree = xml.dom.minidom.parse(filename)
    collection = DOMTree.documentElement
    vectors = collection.getElementsByTagName('metadata')[0].childNodes
    res = {}
    for vector in vectors:
        if vector.nodeType == 1:
            print(f"{vector.tagName}, {vector.firstChild.data}")
            res[vector.tagName] = vector.firstChild.data
    return res


@app.route('/header')
def get_header():
    """
    Return header of whole file
    :return: header
    """
    return header


@app.route('/metadata')
def get_metadata():
    """
    Return metadata of whole file
    :return: metadata
    """
    return metadata


@app.route('/epochs/<epoch>/location')
def get_epoch_location(epoch: str):
    """
    Return state vectors for a specific Epoch from the data set
    :param epoch: specific Epoch
    :return: state vectors
    """
    for data in dic:
        if data['EPOCH'] == epoch:
            res = data.copy()
            break
    epoch_parse_res = isoparse(epoch)
    hours = int(epoch_parse_res.hour)
    minutes = int(epoch_parse_res.minute)
    MEAN_EARTH_RADIUS = 6371.0088
    res['latitude'] = math.degrees(math.atan2(data['Z'], math.sqrt(data['X']**2 + data['Y']**2)))
    res['longitude'] = math.degrees(math.atan2(data['Y'], data['X'])) - ((hours-12)+(minutes/60))*(360/24) + 24
    res['altitude'] = math.sqrt(data['X']**2 + data['Y']**2 + data['Z']**2) - MEAN_EARTH_RADIUS
    geocoder = Nominatim(user_agent='iss_tracker')
    geoloc = geocoder.reverse((res['latitude'], res['longitude']), zoom=15, language='en')
    if geoloc:
        res['geoposition'] = geoloc.address
        print(geoloc.address)
    return res


@app.route('/now')
def get_now_info():
    """
    Return real time position of the ISS
    :return: latitude, longitude, altidue, and geoposition for Epoch that is nearest in time
    """
    time_now = time.time()         # gives present time in seconds since unix epoch
    min_diff = time_now
    print(f"now time: {time_now}")
    min_epoch = ""
    for data in dic:
        epoch = data['EPOCH']
        time_epoch = time.mktime(time.strptime(epoch[:-5], '%Y-%jT%H:%M:%S'))
        temp_diff = time_now - time_epoch
        if temp_diff < min_diff:
            min_diff = temp_diff
            min_epoch = epoch
    print(f"seconds: {min_diff}")
    loc = get_epoch_location(min_epoch)
    print(loc)
    return loc


if __name__ == '__main__':
    dic = read_file_stateVector('ISS.OEM_J2K_EPH.xml')
    comment = read_comment('ISS.OEM_J2K_EPH.xml')
    header = read_header('ISS.OEM_J2K_EPH.xml')
    metadata = read_metadata('ISS.OEM_J2K_EPH.xml')
    app.run()
