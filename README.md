## Seqera Studio Jupyter

This repository contains the definition of Seqera Studio Jupyter. The `main` branch contains the
latest supported version of Jupyter with connect-client. To use an older version of any component,
check the existing tags using the pattern: `jupyter/<version>/connect/<version>`.

## Components

- **[JupyterLab](https://jupyterlab.readthedocs.io/) 4.2.5** — browser-based interactive notebook environment
- **Python 3.13** — via micromamba/conda-forge
- **Data science libraries** — pandas, scikit-learn, statsmodels, seaborn, plotly, altair, r-ggplot2, ipywidgets, itables
- **Jupyter extensions** — jupyterlab-git, jupytext, jupyter-collaboration, jupyter-dash
- **connect-client** — Seqera connect client for studio integration

## Repository Structure

`.seqera/` contains:

- `studio-config.yaml` — references the pre-built image; studios using this branch will not require a build step
- `Dockerfile` — shows how the image was built; fork this repository and modify it to create a custom image
- `env.yaml` — conda environment specification (Python 3.13 and all dependencies)
- `_start_jupyter.sh` — startup script that launches JupyterLab
- `seqera_identity_provider.py` — JupyterLab identity provider configuration

## Customization

To create a customized version:

1. Fork this repository
2. Modify the `Dockerfile` and/or `env.yaml` to add your tools or dependencies
3. Build and push your custom image
4. Update `studio-config.yaml` to reference your custom image

## Pre-built Image

The pre-built image is available at:

```
public.cr.seqera.io/platform/data-studio-jupyter:4.2.5-0.12.0
```
