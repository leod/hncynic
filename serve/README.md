# Serving

## TensorFlow Serving
```
docker run \
  --rm \
  -p 9000:9000 \
  -v $PWD:/models \
  --name serving \
  --entrypoint tensorflow_model_server \
  tensorflow/serving:1.11.0 --enable_batching=true \
                            --batching_parameters_file=/models/batching_parameters.txt \
                            --port=9000 --model_base_path=/models/export1/1550276061 \
                            --model_name=1550276061
```
