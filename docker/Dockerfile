# Use NVIDIA L4T 36.2 with TensorRT as base
FROM nvcr.io/nvidia/l4t-tensorrt:r8.6.2-devel

WORKDIR /

# Install compilers and build tools
ENV DEBIAN_FRONTEND=noninteractive \
    LANGUAGE=en_US:en \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8

RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        locales \
        locales-all \
        tzdata \
    && locale-gen en_US $LANG \
    && update-locale LC_ALL=$LC_ALL LANG=$LANG \
    && locale \
    \
    && apt-get install -y --no-install-recommends \
        build-essential \
        software-properties-common \
        apt-transport-https \
        lsb-release \
        pkg-config \
        git \
        gdb \
        curl \
	wget \
        zip \
        unzip \
        time \
	   sshpass \
	   ssh-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    \
    && gcc --version \
    && g++ --version

ARG TARPACK_TMPDIR="/tmp/tarpack" \
    TARPACK_PREFIX="/usr/local" \
    WGET_OPTIONS="--quiet --show-progress --progress=bar:force:noscroll"

# Install python
ARG PYTHON_VERSION_ARG="3.10"

ENV PYTHON_VERSION=${PYTHON_VERSION_ARG} \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_CACHE_PURGE=true \
    PIP_ROOT_USER_ACTION=ignore \
    TWINE_NON_INTERACTIVE=1 \
    DEBIAN_FRONTEND=noninteractive

RUN set -x \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
	python${PYTHON_VERSION} \
	python${PYTHON_VERSION}-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python${PYTHON_VERSION} || \
       curl -sS https://bootstrap.pypa.io/pip/3.6/get-pip.py | python3.6 \
    && ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3 \
    && which python3 \
    && python3 --version \
    && which pip3 \
    && pip3 --version \
    && python3 -m pip install --upgrade pip --index-url https://pypi.org/simple \
    && pip3 install --no-cache-dir --verbose --no-binary :all: psutil \
    && pip3 install --upgrade --no-cache-dir \
       	    setuptools \
   	    packaging \
   	    'Cython<3' \
   	    wheel \
   	    twine

# Install cmake with pip
RUN set -ex \
    && pip3 install --upgrade --force-reinstall --no-cache-dir --verbose cmake \
    \
    && cmake --version \
    && which cmake

ARG OPENCV_VERSION="4.8.1" \
    OPENCV_PYTHON="4.x" \
    CUDA_ARCH_BIN="8.7" \
    ARCH=$(uname -i)
RUN pip3 install --no-cache-dir \
    	opencv-contrib-python~=${OPENCV_VERSION}

# Installing gstreamer
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
		  libgstreamer1.0-dev \
		  gstreamer1.0-libav \
		  gstreamer1.0-rtsp \
		  gstreamer1.0-plugins-bad \
		  libgstreamer-plugins-base1.0-dev \
		  libgstreamer-plugins-good1.0-dev \
		  libgstreamer-plugins-bad1.0-dev \
		  libgstrtspserver-1.0-0 \
		  python3-gi \
		  python3-gst-1.0 \
		  gstreamer1.0-plugins-rtp \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install onnx
ARG ONNX_VERSION="main"

RUN pip3 install numpy==1.26.4 --upgrade --no-cache-dir --verbose

RUN pip3 install --no-cache-dir --verbose onnx || \
    pip3 install --no-cache-dir --verbose git+https://github.com/onnx/onnx@${ONNX_VERSION} && \
    pip3 show onnx && \
    python3 -c 'import onnx; print(onnx.__version__)'

# Installing onnxruntime
ARG ONNXRUNTIME_VERSION="1.17.0" \
    ONNXRUNTIME_BRANCH="v1.17.0" \
    ONNXRUNTIME_FLAGS="--allow_running_as_root" \
    TAR_INDEX_URL="http://jetson.webredirect.org:8000/jp6/cu122" \
    PIP_INDEX_REPO="http://jetson.webredirect.org/jp6/cu122" \
    PIP_UPLOAD_REPO="http://localhost/jp6/cu122" \
    PIP_UPLOAD_USER="jp6" \
    PIP_UPLOAD_PASS="none" \
    PIP_TRUSTED_HOSTS="jetson.webredirect.org"

ENV TAR_INDEX_URL=${TAR_INDEX_URL} \
    PIP_INDEX_URL=${PIP_INDEX_REPO} \
    PIP_TRUSTED_HOST=${PIP_TRUSTED_HOSTS}

RUN mkdir -p  ${TARPACK_TMPDIR}/uploads \
    && wget ${WGET_OPTIONS} ${TAR_INDEX_URL}/onnxruntime-gpu-${ONNXRUNTIME_VERSION}.tar.gz \
    && wget ${WGET_OPTIONS} ${TAR_INDEX_URL}/onnxruntime-gpu-${ONNXRUNTIME_VERSION}.sha256 \
    && sha256sum --check onnxruntime-gpu-${ONNXRUNTIME_VERSION}.sha256 \
    && tar -xzvf onnxruntime-gpu-${ONNXRUNTIME_VERSION}.tar.gz -C ${TARPACK_PREFIX} \
    && rm onnxruntime-gpu-${ONNXRUNTIME_VERSION}.tar.gz \
    && rm onnxruntime-gpu-${ONNXRUNTIME_VERSION}.sha256 \
    && pip3 install --no-cache-dir --verbose onnxruntime-gpu==${ONNXRUNTIME_VERSION} \
    && python3 -c 'import onnxruntime; print(onnxruntime.__version__);'

#Installing jetson-inference
RUN pip3 install torchvision==0.18.0a0+6043bc2

ADD https://api.github.com/repos/dusty-nv/jetson-inference/git/refs/heads/master /tmp/jetson_inference_version.json

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
	    libglew-dev \
	    glew-utils \
	    libsoup2.4-dev \
	    libjson-glib-dev \
	    libgstrtspserver-1.0-dev \
	    avahi-utils \
	    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# build from source
RUN git clone --recursive --depth=1 https://github.com/dusty-nv/jetson-inference /opt/jetson-inference \
    && cd /opt/jetson-inference \
    && mkdir build \
    && cd build \
    && cmake ../ \
    && make -j$(nproc) \
    && make install \
    # clean build files
    && /bin/bash -O extglob -c "cd /opt/jetson-inference/build; rm -rf -v !($(uname -m)|download-models.*)"

# the jetson-inference installer calls apt-update
RUN rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# install optional dependencies
RUN pip3 install --no-cache-dir --ignore-installed blinker \
    && pip3 install --no-cache-dir --verbose -r /opt/jetson-inference/python/training/detection/ssd/requirements.txt \
    && pip3 install --no-cache-dir --verbose -r /opt/jetson-inference/python/www/flask/requirements.txt \
    && pip3 install --no-cache-dir --verbose -r /opt/jetson-inference/python/www/dash/requirements.txt

ENV LD_PRELOAD=/lib/aarch64-linux-gnu/libGLdispatch.so.0:${LD_PRELOAD}


# Installing huggingface hub
# set the model cache dir
ENV TRANSFORMERS_CACHE=/data/models/huggingface \
    HUGGINGFACE_HUB_CACHE=/data/models/huggingface \
    HF_HOME=/data/models/huggingface

# install huggingface_hub package (with CLI)
RUN set -ex \
    && pip3 install --no-cache-dir --verbose \
        huggingface_hub[cli] \
        dataclasses \
    \
    # make sure it loads \
    && huggingface-cli --help \
    && pip3 show huggingface_hub \
    && python3 -c 'import huggingface_hub; print(huggingface_hub.__version__)' \
    \
    # for benchmark timing \
    && apt-get update \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Installing llm transformers
ARG TRANSFORMERS_PACKAGE=transformers==4.40.2

# if you want optimum[exporters,onnxruntime] see the optimum package
RUN pip3 install --no-cache-dir --verbose \
	accelerate \
	optimum \
	sentencepiece && \
    \
    # install from pypi, git, ect (sometimes other version got installed)
    pip3 uninstall -y transformers && \
    pip3 install --no-cache-dir --verbose ${TRANSFORMERS_PACKAGE} && \
    \
    # "/usr/local/lib/python3.8/dist-packages/transformers/modeling_utils.py", line 118
    # AttributeError: module 'torch.distributed' has no attribute 'is_initialized'
    PYTHON_ROOT=`pip3 show transformers | grep Location: | cut -d' ' -f2` && \
    sed -i 's|torch.distributed.is_initialized|torch.distributed.is_available|g' -i ${PYTHON_ROOT}/transformers/modeling_utils.py

# make sure it loads
RUN pip3 show transformers && python3 -c 'import transformers; print(transformers.__version__)'

# Installing mlc
ARG TVM_VERSION="0.15.0" \
    MLC_VERSION="0.1.0" \
    MLC_COMMIT="607dc5a" \
    MLC_PATCH="patches/607dc5a.diff" \
    LLVM_VERSION=17

ENV LD_LIBRARY_PATH="/usr/local/lib/python${PYTHON_VERSION}/dist-packages/tvm:${LD_LIBRARY_PATH}" \
    TVM_HOME=/opt/mlc-llm/3rdparty/tvm

# install the wheels
RUN pip3 install --no-cache-dir --verbose tvm==${TVM_VERSION} mlc-llm==${MLC_VERSION} \
    && pip3 install --no-cache-dir --verbose mlc-chat==${MLC_VERSION} || echo "failed to pip install mlc-chat==${MLC_VERSION} (this is expected for mlc>=0.1.1)" \
    && pip3 install --no-cache-dir --verbose 'pydantic>2'

# we need the source because the MLC model builder relies on it
RUN git clone https://github.com/mlc-ai/mlc-llm /opt/mlc-llm \
    && cd /opt/mlc-llm \
    && git checkout ${MLC_COMMIT} \
    && git submodule update --init --recursive

RUN ln -s /opt/mlc-llm/3rdparty/tvm/3rdparty /usr/local/lib/python${PYTHON_VERSION}/dist-packages/tvm/3rdparty

# make sure it loads
RUN pip3 show tvm mlc_llm

# Installing nano llm

ARG NANO_LLM_BRANCH=main \
    NANO_LLM_PATH=/opt/NanoLLM

ENV PYTHONPATH=${PYTHONPATH}:${NANO_LLM_PATH} \
    SSL_KEY=/etc/ssl/private/localhost.key.pem \
    SSL_CERT=/etc/ssl/private/localhost.cert.pem

ADD https://api.github.com/repos/dusty-nv/NanoLLM/git/refs/heads/${NANO_LLM_BRANCH} /tmp/nano_llm_version.json
RUN git clone --branch=${NANO_LLM_BRANCH} --recursive https://github.com/dusty-nv/NanoLLM ${NANO_LLM_PATH} \
    && cd ${NANO_LLM_PATH} \
    && git checkout 0c297a13bf45e90c1f7de640f58071a5e4a79fb7

RUN pip3 install --ignore-installed --no-cache-dir blinker && \
    pip3 install --no-cache-dir --verbose -r ${NANO_LLM_PATH}/requirements.txt && \
    openssl req \
	-new \
	-newkey rsa:4096 \
	-days 3650 \
	-nodes \
	-x509 \
	-keyout ${SSL_KEY} \
	-out ${SSL_CERT} \
	-subj '/CN=localhost'

RUN mkdir -p /data/models/mlc/dist/models/

# Copy rrms-utils
COPY rrms-utils /rrms-utils
RUN cd /rrms-utils/ && pip3 install .

# Copy ai-agent
COPY ai-agent /ai-agent
RUN cd /ai-agent && pip3 install .
