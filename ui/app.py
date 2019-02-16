from flask import Flask, jsonify, request, abort

from serve.client import Generator

app = Flask(__name__)

HOST='localhost'
PORT=9000
MODEL_NAME='1550285931'
PREPROCESSOR='../data/preprocess.sh'
POSTPROCESSOR='../data/mosesdecoder/scripts/tokenizer/detokenizer.perl'
BPE_CODES='../exps/data/bpecodes'

generator = Generator(host=HOST,
                      port=PORT,
                      model_name=MODEL_NAME,
                      preprocessor=PREPROCESSOR,
                      postprocessor=POSTPROCESSOR,
                      bpe_codes='../exps/data/bpecodes')

@app.route('/gen', methods=['GET'])
def gen():
  if 'title' not in request.args:
    abort(400)

  title = request.args.get('title')
  hyps = generator(title, n=4)

  return jsonify(hyps)

if __name__ == '__main__':
  app.run(debug=True)
