# Companion Toolkit


## Introduction

This repository is a collection of companion tooling for our `woodnet` deep learning pipeline and paper project.
It encompasses the following main purposes:
- provide visualization code and infrastructure for the described advanced sub-µ-CT imaging modality
  - planar visualizations with interactive widget controls $\rightarrow$ `SliceDisplay` class
  - volumetric visualizations with interactive widget controls $\rightarrow$ `VolumeDisplay` class
- data helper code performing an automated prediction 🤖

## Installation

You can first pull the repository to a location of your desire.
```bash
git pull https://github.com/stebix/wn-companiontools.git
```
Then - assuming the current working directory is the pulled repository - install the code via `pip` in editable mode.
```bash
pip install --editable .
```
> [!TIP]
> If you are using `conda` or `mamba` to manage your Python environments and packages, then it can be inadvisable to let `pip` install packages on its own (see e.g. [here](https://www.anaconda.com/blog/using-pip-in-a-conda-environment)).
> In this case, install the necessary dependencies manually via `conda/mamba` and add the `--no-deps` command to the above `pip install` command to inhibit `pip` installations.

### Dependencies

The code has these dependencies that can also be isntalled via `conda` or `mamba`:
```bash
conda install -c conda-forge numpy matplotlib k3d ipywidgets zarr h5py ipympl
```

## Further Information

If you are interested in wood science and the application of advanced computed tomography imaging and deep learning to it, you may find our paper manuscript (TODO: LINK) and the [`woodnet`](https://github.com/stebix/woodnet) pipeline implementation useful.

2024 Jannik Stebani
