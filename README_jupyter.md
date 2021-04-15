
## Jupyter Notebook

Some instruction to use [Jupyter Notebook](https://jupyter.org/).
For CERN users, it's also possible to use [SWAN](https://swan.web.cern.ch/) directly with ROOT+Python+Jupyter binding and kernel service.

### Jupyter

#### Installation
```
pip3 install jupyter
```

Other options of installation can be found [here](https://jupyter.readthedocs.io/en/latest/install.html).

#### Running the Notebook
```
jupyter notebook
```
This will print some information about the notebook server in your terminal, and open your default web browser to this URL.

The following code should open the given notebook in the currently running notebook server, starting one if necessary.
```
jupyter notebook notebook.ipynb
```

More details can be found from the official [users guide](https://jupyter.readthedocs.io/en/latest/running.html).


### Convert `C` marcos or `pyroot` macros to notebooks

Here is a script [converttonotebook.py](https://github.com/root-project/root/blob/master/documentation/doxygen/converttonotebook.py) used to convert ROOT official tutorial codes to notebooks.

But it requires some header lines at the beginning of the macros:
```
/// \file
/// \ingroup tutorial_fit
/// \notebook
/// Simple fitting example (1-d histogram with an interpreted function)
///
/// \macro_image
/// \macro_output
/// \macro_code
///
/// \author XXX
```
or for pyroot
```
## \file
## \ingroup tutorial_pyroot
## \notebook
## Fit example.
##
## \macro_image
## \macro_output
## \macro_code
##
## \author XXX
```


