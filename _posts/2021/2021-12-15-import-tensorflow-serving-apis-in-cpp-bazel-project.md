---
layout: post
title: "How to import TensorFlow Serving APIs for C++ in Bazel project"
tags:
  - bazel
  - tensorflow
---

TensorFlow and TensorFlow Serving are built using [Bazel](https://bazel.build) and developing gRPC clients for TensorFlow Serving requires to import the TensorFlow project. That work is a little bit hard except for Python since [the prebuilt package](https://pypi.org/project/tensorflow-serving-api/) only exists for Python. We don't know what protobuf files we should import until looking into the protobuf files in the TF and TF-Serving.

In this blog post, I will write about integrating TF-Serving's gRPC interfaces for C++ in the Bazel project with sample client codes. All codes here are in GitHub (<https://github.com/jeongukjae/chips/tree/main/tf-serving-cpp-client-example>).

## Set up the environment

Before implementing a client, I launched a sample TF-Serving container in the local environment. I followed the guide [here](https://www.tensorflow.org/tfx/serving/docker) but exposed port for gRPC additionally.

```sh
docker pull tensorflow/serving

git clone https://github.com/tensorflow/serving
TESTDATA="$(pwd)/serving/tensorflow_serving/servables/tensorflow/testdata"

docker run -t --rm -p 8501:8501 -p 8500:8500 \
    -v "$TESTDATA/saved_model_half_plus_two_cpu:/models/half_plus_two" \
    -e MODEL_NAME=half_plus_two \
    tensorflow/serving
```

## Implement a client

### Set up Bazel Workspace

I added the below codes in the `WORKSPACE` file to add TensorFlow and TensorFlow Serving projects. For the version of TF, I just check the `WORKSPACE` file of the TensorFlow Serving repository and copied the commit and sha256 hash value.

```python
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

# TensorFlow Serving
# https://github.com/tensorflow/serving/blob/2.6.2/WORKSPACE
http_archive(
    name = "com_github_tensorflow_serving",
    sha256 = "193d2cf959d9444a2837fe13f3efa51127532ad9ee99585903301c1a4a4c21c9",
    strip_prefix = "serving-2.6.2",
    url = "https://github.com/tensorflow/serving/archive/2.6.2.tar.gz",
)

load("@com_github_tensorflow_serving//tensorflow_serving:repo.bzl", "tensorflow_http_archive")

# TensorFlow
tensorflow_http_archive(
    name = "org_tensorflow",
    git_commit = "c2363d6d025981c661f8cbecf4c73ca7fbf38caf",
    sha256 = "add5982a3ce3b9964b7122dd0d28927b6a9d9abd8f95a89eda18ca76648a0ae8",
)

load("@com_github_tensorflow_serving//tensorflow_serving:workspace.bzl", "tf_serving_workspace")

tf_serving_workspace()

load("@org_tensorflow//tensorflow:workspace3.bzl", "workspace")

workspace()

load("@org_tensorflow//tensorflow:workspace2.bzl", "workspace")

workspace()

load("@org_tensorflow//tensorflow:workspace1.bzl", "workspace")

workspace()

load("@org_tensorflow//tensorflow:workspace0.bzl", "workspace")

workspace()
```

### Add client codes

After that, I could use TF Serving APIs for my project. To show how to do it, I wrote a sample code to inference the `half_plus_two` model.

```c++
#include "grpcpp/grpcpp.h"
#include "tensorflow_serving/apis/prediction_service.grpc.pb.h"

#define HOST "0.0.0.0:8500"
#define MODEL_NAME "half_plus_two"
#define MODEL_SIGNATURE_NAME "serving_default"

int main() {
  tensorflow::serving::PredictRequest predictRequest;
  tensorflow::serving::PredictResponse predictResponse;
  grpc::ClientContext clientContext;

  predictRequest.mutable_model_spec()->set_name(MODEL_NAME);
  predictRequest.mutable_model_spec()->set_signature_name(MODEL_SIGNATURE_NAME);
  auto inputMap = predictRequest.mutable_inputs();

  tensorflow::TensorProto inputTensor;
  inputTensor.set_dtype(tensorflow::DataType::DT_FLOAT);
  inputTensor.mutable_tensor_shape()->add_dim()->set_size(1);
  inputTensor.mutable_tensor_shape()->add_dim()->set_size(3);
  inputTensor.add_float_val(1.0f);
  inputTensor.add_float_val(2.0f);
  inputTensor.add_float_val(5.0f);
  (*inputMap)["x"] = inputTensor;

  for (const auto& inputPair : *inputMap) {
    std::cout << "Input " << inputPair.first << std::endl;
    auto tensor = inputPair.second;

    for (const auto val : tensor.float_val()) {
      std::cout << "\t" << val;
    }
    std::cout << std::endl;
  }

  std::unique_ptr<tensorflow::serving::PredictionService::Stub> stub =
      tensorflow::serving::PredictionService::NewStub(
          grpc::CreateChannel(HOST, grpc::InsecureChannelCredentials()));

  grpc::Status status =
      stub->Predict(&clientContext, predictRequest, &predictResponse);

  if (!status.ok()) {
    std::cerr << "Error code: " << status.error_code()
              << ", message: " << status.error_message() << std::endl;
    return 1;
  }

  for (const auto& outputPair : predictResponse.outputs()) {
    std::cout << "Output " << outputPair.first << std::endl;
    auto tensor = outputPair.second;

    for (const auto val : tensor.float_val()) {
      std::cout << "\t" << val;
    }
    std::cout << std::endl;
  }
}
```

To build it, I linked it with `prediction_service_cc_proto` from the TensorFlow Serving project.

```python
cc_binary(
    name = "test_client",
    srcs = ["test_client.cc"],
    deps = [
        "@com_github_tensorflow_serving//tensorflow_serving/apis:prediction_service_cc_proto",
        "@com_github_grpc_grpc//:grpc",
    ],
)
```

### Build and run

Then I could successfully build and run it to inference `half_plus_two` model via gRPC

```sh
$ bazel run //:test_client
INFO: Analyzed target //:test_client (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:test_client up-to-date:
  bazel-bin/test_client
INFO: Elapsed time: 5.389s, Critical Path: 5.19s
INFO: 3 processes: 1 internal, 2 darwin-sandbox.
INFO: Build completed successfully, 3 total actions
INFO: Build completed successfully, 3 total actions
Input x
        1       2       5
Output y
        2.5     3       4.5
```
