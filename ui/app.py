#!/usr/bin/env python3

from flask import Flask, jsonify, request, abort, send_from_directory

from serve.client import Generator

app = Flask(__name__, static_url_path='/static')

HOST='localhost'
PORT=9000
MODEL_NAME='aws-first-model'
PREPROCESSOR='/home/host/src/hncynic/data/preprocess.sh'
POSTPROCESSOR='/home/host/src/hncynic/data/mosesdecoder/scripts/tokenizer/detokenizer.perl'
BPE_CODES='/home/serve/models/aws-first-model/bpecodes'

generator = Generator(host=HOST,
                      port=PORT,
                      model_name=MODEL_NAME,
                      preprocessor=PREPROCESSOR,
                      postprocessor=POSTPROCESSOR,
                      bpe_codes=BPE_CODES)

@app.route('/gen', methods=['GET'])
def gen():
  if 'title' not in request.args:
    abort(400)

  title = request.args.get('title')
  hyps = generator(title, n=6)

  return jsonify(hyps)

@app.route('/')
def index():
  return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')
