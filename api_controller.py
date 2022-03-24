from flask import Flask, abort, Response
import sqliteDatabase
import dataclasses
import json

app = Flask("FlaskApp")


@app.route("/status")
def get_status():
    (dynuResp, ipfyResp) = sqliteDatabase.get_from_db()

    if dynuResp is not None:
        dynuDict = dataclasses.asdict(dynuResp)
    else:
        dynuDict = {"error": "Cannot find dynu record"}

    if dynuResp is not None:
        ipfyDict = dataclasses.asdict(ipfyResp)
    else:
        ipfyDict = {"error": "Cannot find ipfy record"}

    jsonResponse = json.dumps({"Ipfy Response": ipfyDict, "Dynu Response": dynuDict})

    if dynuResp is None or ipfyResp is None or (
            dynuResp.code != 200 or (dynuResp.msg != "nochg" and dynuResp.msg != "good")) or ipfyResp.code != 200:
        abort(Response(jsonResponse, status=400, content_type='application/json'))

    return Response(jsonResponse, mimetype='application/json')


def runApi():
    from waitress import serve
    serve(app, host='0.0.0.0', port=1050)
