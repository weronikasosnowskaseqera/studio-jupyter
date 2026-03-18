ARG CONNECT_CLIENT_VERSION

FROM public.cr.seqera.io/platform/connect-client:0.11 AS connect


FROM mambaorg/micromamba:1.5.10-noble as micromamba


FROM ubuntu:24.04

ARG CONNECT_CLIENT_VERSION
LABEL io.seqera.connect.version="${CONNECT_CLIENT_VERSION}"

ARG MAMBA_USER=root
ARG MAMBA_USER_ID=0
ARG MAMBA_USER_GID=0
ENV MAMBA_USER=$MAMBA_USER
ENV MAMBA_ROOT_PREFIX="/opt/conda"
ENV MAMBA_EXE="/bin/micromamba"

USER $MAMBA_USER


RUN apt-get update --yes && apt-get install --yes --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    git \
    unzip \
    openssh-client \
    nano \
    bzip2 \
    vim \
    less \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-plain-generic \
    wget \
    libpq-dev \
    libgit2-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY --from=micromamba "$MAMBA_EXE" "$MAMBA_EXE"
COPY --from=micromamba /usr/local/bin/_activate_current_env.sh /usr/local/bin/_activate_current_env.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_shell.sh /usr/local/bin/_dockerfile_shell.sh
COPY --from=micromamba /usr/local/bin/_entrypoint.sh /usr/local/bin/_entrypoint.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_initialize_user_accounts.sh /usr/local/bin/_dockerfile_initialize_user_accounts.sh
COPY --from=micromamba /usr/local/bin/_dockerfile_setup_root_prefix.sh /usr/local/bin/_dockerfile_setup_root_prefix.sh

RUN /usr/local/bin/_dockerfile_initialize_user_accounts.sh && \
    /usr/local/bin/_dockerfile_setup_root_prefix.sh

SHELL ["/usr/local/bin/_dockerfile_shell.sh"]
COPY --chown=$MAMBA_USER:$MAMBA_USER ./docker/jupyter_4.2.5/env.yaml /tmp/env.yaml
# need to have lower ulimit given micromamba issue:
# https://github.com/mamba-org/micromamba-docker/issues/368#issuecomment-1706054594
# https://github.com/DaanDeMeyer/reproc/pull/103
RUN ulimit -n 262144 && \
    micromamba install --yes --file /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

COPY ./docker/jupyter_4.2.5/_start_jupyter.sh /init
RUN chmod +x /init

ENV SHELL=/usr/bin/bash
SHELL ["/usr/bin/bash", "-o", "pipefail", "-c"]

COPY ./docker/jupyter_4.2.5/seqera_identity_provider.py /root/.jupyter/jupyter_lab_config.py

# Add connect binary
COPY --from=connect /usr/bin/connect-client /usr/bin/connect-client
# Install connect dependencies
RUN /usr/bin/connect-client --install
# Optionally set tool identifier for metrics tracking purposes
RUN /usr/bin/connect-client --setToolIdentifier jupyter

ENTRYPOINT ["/usr/bin/connect-client", "--entrypoint"]
CMD ["/usr/bin/bash", "-c", "/init"]

