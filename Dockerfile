FROM mambaorg/micromamba:2.9.0

WORKDIR /app

# Install precompiled packages.
# dlib comes prebuilt from conda-forge, so Render does NOT compile it.
RUN micromamba install -y -n base -c conda-forge \
    python=3.11 \
    dlib \
    flask=3.0.3 \
    gunicorn=22.0.0 \
    numpy \
    pillow \
    click \
    pip \
    "setuptools<81" \
    && micromamba clean --all --yes

# Install face_recognition without allowing pip to reinstall/compile dlib.
RUN pip install --no-cache-dir --no-deps \
    face_recognition_models==0.3.0 \
    face_recognition==1.3.0

COPY . .

CMD ["bash", "-lc", "exec gunicorn -w 1 -b 0.0.0.0:${PORT:-10000} --timeout 120 app:app"]
