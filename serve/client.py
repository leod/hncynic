#!/usr/bin/env python3
""" Client for TensorFlow serving.

Reads titles from STDIN, and writes comment samples to STDOUT.
"""

# adapted from https://github.com/OpenNMT/OpenNMT-tf/blob/master/examples/serving/ende_client.py

import sys

import argparse

import tensorflow as tf
import subprocess

import grpc

import subword_nmt.apply_bpe as apply_bpe

from tensorflow_serving.apis import predict_pb2, prediction_service_pb2_grpc

class Generator:
  def __init__(self, preprocessor, bpe_codes, stub, model_name, postprocessor):
    self.preprocessor = preprocessor
    with open(bpe_codes) as f:
      self.bpe = apply_bpe.BPE(f)
    self.stub = stub
    self.model_name = model_name
    self.postprocessor = postprocessor

  def __call__(self, title, n=8, timeout=50.0):
    # TODO: Tried to reuse the process, but something seems to be buffering
    preprocessor = subprocess.Popen([self.preprocessor],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL)

    title_pp = preprocessor.communicate((title.strip() + '\n').encode())[0].decode('utf-8')
    title_bpe = self.bpe.segment_tokens(title_pp.strip().lower().split(' '))

    sys.stdout.write(str(title_bpe) + '\n')

    request = predict_pb2.PredictRequest()
    request.model_spec.name = self.model_name
    request.inputs['tokens'].CopyFrom(
      tf.make_tensor_proto([title_bpe] * n, shape=(n, len(title_bpe))))
    request.inputs['length'].CopyFrom(
      tf.make_tensor_proto([len(title_bpe)] * n, shape=(n,)))
    future = self.stub.Predict.future(request, timeout)

    result = future.result()

    batch_predictions = tf.make_ndarray(result.outputs["tokens"])
    batch_lengths = tf.make_ndarray(result.outputs["length"])
    batch_scores = tf.make_ndarray(result.outputs["log_probs"])

    hyps = []
    for (predictions, lengths, scores) in zip(batch_predictions, batch_lengths, batch_scores):
      # ignore </s>
      prediction = predictions[0][:lengths[0]-1]

      comment = ' '.join([token.decode('utf-8') for token in prediction])

      # TODO: Tried to reuse the process, but something seems to be buffering
      postprocessor = subprocess.Popen([self.postprocessor],
                                       stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE,
                                       stderr=subprocess.DEVNULL)
      prediction_ready = postprocessor.communicate((comment + '\n').encode())[0].decode('utf-8')

      hyps.append((prediction_ready.strip(), scores[0]))

    hyps.sort(key=lambda hyp: hyp[1] / len(hyp), reverse=True)

    return hyps

def main():
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--model_name', required=True, help='model name')
  parser.add_argument('--preprocessor', required=True, help='tokenization script')
  parser.add_argument('--bpe_codes', required=True, help='BPE codes')
  parser.add_argument('--host', default='localhost', help='model server host')
  parser.add_argument('--port', type=int, default=9000, help='model server port')
  parser.add_argument('--postprocessor', required=True, help='postprocessing script')

  args = parser.parse_args()

  channel = grpc.insecure_channel("%s:%d" % (args.host, args.port))
  stub = prediction_service_pb2_grpc.PredictionServiceStub(channel)
  
  generator = Generator(preprocessor=args.preprocessor,
                        bpe_codes=args.bpe_codes,
                        stub=stub,
                        model_name=args.model_name,
                        postprocessor=args.postprocessor)

  for title in sys.stdin:
    hyps = generator(title)

    for prediction, score in hyps:
      sys.stdout.write('{}\t{}\n'.format(score, prediction))
  
if __name__ == "__main__":
  main()
