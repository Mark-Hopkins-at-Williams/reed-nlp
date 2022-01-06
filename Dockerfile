FROM python:3
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
RUN python3 -m pip install -U --force-reinstall pip
RUN pip install --upgrade pip
RUN pip install Cython numpy
RUN pip install Flask Flask-Cors benepar
RUN python ./download_models.py
EXPOSE 5000
CMD python ./api.py