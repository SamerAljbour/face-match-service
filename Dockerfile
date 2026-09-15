FROM mambaorg/micromamba:2.8.1

WORKDIR /app

RUN micromamba install -y -n base -c conda-forge \
    python=3.11 \
    dlib \
    face_recognition=1.3.0 \
    face_recognition_models=0.3.0 \
    flask=3.0.3 \
    gunicorn=22.0.0 \
    setuptools=80.10.2 \
    && micromamba clean --all --yes

# Verify everything before Render starts the service
RUN micromamba run -n base python -c "import pkg_resources; print('pkg_resources OK')"
RUN micromamba run -n base python -c "import face_recognition_models; print('models OK')"
RUN micromamba run -n base python -c "import face_recognition; print('face_recognition OK')"
RUN micromamba run -n base gunicorn --version

COPY . .

CMD ["bash", "-lc", "exec micromamba run -n base gunicorn -w 1 -b 0.0.0.0:${PORT:-10000} --timeout 120 app:app"]
