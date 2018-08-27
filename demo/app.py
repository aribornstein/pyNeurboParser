"""
Written By Ari Bornstein
Demo flask service written for semantic dependency parsing
Run in the context of the contained Dockerfile
"""
import sys
sys.path.append("/data/src/")
from SDP_eval import semantic_parse
from flask import Flask

app = Flask(__name__)

parser_file = '/opt/dynet/NeurboParser/NeurboParser/build/neurboparser'

dm_pruner = '/opt/dynet/NeurboParser/model/english_dm.pruner.model'
dm_model = '/opt/dynet/NeurboParser/model/dm.adadelta.lstm200.layer2.h100.drop0.25.model'

pas_pruner = '/opt/dynet/NeurboParser/model/english_pas.pruner.model'
pas_model = '/opt/dynet/NeurboParser/model/pas.adadelta.lstm200.layer2.h100.drop0.25.model'

psd_pruner = '/opt/dynet/NeurboParser/model/english_pas.pruner.model'
psd_model = '/opt/dynet/NeurboParser/model/psd.adadelta.lstm200.layer2.h100.drop0.25.model'

data_file = '/opt/dynet/NeurboParser/temp.sdp'
prediction = '/opt/dynet/NeurboParser/pred.sdp'

@app.route("/")
def hello():
    """
    Default path
    """
    return "Welcome to the pyNeurboParser Demo Web App!!<br><br>\
            To use pass your text data to the following endpoints: <br>\
            &nbsp-> \\dm\\`text` for dm format<br>\
            &nbsp-> \\pas\\`text` for pas format<br>\
            &nbsp-> \\psd\\`text` for psd format<br>\
            Please note that the demo service takes about 5 seconds to process text and return a response.\
            "

@app.route('/dm/<text>')
def dm(text):
    """
    Takes in a string of sentences and returns a DM parse JSON response
    """
    if (not dm_model) or (not dm_pruner):
        return "DM model not found"
    # show the user profile for that user
    return semantic_parse(text, parser_file, dm_pruner, data_file, dm_model, prediction)

@app.route('/psd/<text>')
def psd(text):
    if (not psd_model) or (not psd_pruner):
        return "PSD model not found"
    # show the user profile for that user
    return semantic_parse(text, parser_file, psd_pruner, data_file, psd_model, prediction)

@app.route('/pas/<text>')
def pas(text):
    if (not pas_model) or (not pas_pruner):
        return "PAS model not found"
    # show the user profile for that user
    return semantic_parse(text, parser_file, pas_pruner, data_file, pas_model, prediction)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
