FROM  mambaorg/micromamba:latest

WORKDIR /app

COPY environment.yml .

RUN micromamba install -f environment.yml -n base

ENV PATH=/opt/conda/bin:$PATH

COPY scripts/ .

ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]
