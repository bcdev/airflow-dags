FROM  mambaorg/micromamba:latest

ARG NEW_MAMBA_USER=xcube
ARG NEW_MAMBA_USER_ID=1000
ARG NEW_MAMBA_USER_GID=1000
USER root
# Magic taken from https://hub.docker.com/r/mambaorg/micromamba,
# section "Changing the user id or name"
RUN usermod "--login=${NEW_MAMBA_USER}" "--home=/home/${NEW_MAMBA_USER}" \
        --move-home "-u ${NEW_MAMBA_USER_ID}" "${MAMBA_USER}" && \
    groupmod "--new-name=${NEW_MAMBA_USER}" \
             "-g ${NEW_MAMBA_USER_GID}" "${MAMBA_USER}" && \
    # Update the expected value of MAMBA_USER for the
    # _entrypoint.sh consistency check.
    echo "${NEW_MAMBA_USER}" > "/etc/arg_mamba_user" && \
    :

ENV MAMBA_USER=$NEW_MAMBA_USER
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

USER $MAMBA_USER

COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml \
    && micromamba clean --all --yes

COPY --chown=$MAMBA_USER:$MAMBA_USER ./scripts /tmp/scripts

WORKDIR /home/$MAMBA_USER

# The micromamba entrypoint.
# Allows us to run container as an executable with
# base environment activated.
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh"]

