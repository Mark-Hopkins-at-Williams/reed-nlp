FROM python:3.7
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
# Tell nvidia-docker the driver spec that we need as well as to
# use all available devices, which are mounted at /usr/local/nvidia.
# The LABEL supports an older version of nvidia-docker, the env
# variables a newer one.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
LABEL com.nvidia.volumes.needed="nvidia_driver"
COPY . /app
WORKDIR /app
RUN pip install Cython==0.29.19 numpy==1.18.4
RUN pip install -r requirements.txt
RUN pip install -r requirements2.txt
RUN python ./download_models.py
EXPOSE 5000
CMD python ./api.py