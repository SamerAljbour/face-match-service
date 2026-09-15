FROM mambaorg/micromamba:2.8.1

WORKDIR /app

RUN micromamba install -y -n base -c conda-forge \
    python=3.11 \
    dlib \
    face_recognition=1.3.0 \
    face_recognition_models=0.3.0 \
    flask=3.0.3 \
    gunicorn=22.0.0 \
    && micromamba clean --all --yes

COPY . .

CMD ["bash", "-lc", "exec gunicorn -w 1 -b 0.0.0.0:${PORT:-10000} --timeout 120 app:app"]
