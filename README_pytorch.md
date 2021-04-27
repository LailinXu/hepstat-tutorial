## PyTorch

Thanks to Tairan Xu(tairan.xu@cern.ch) for preparing this tutorial.

### Docker setup

```
docker pull nyanyanyanyanyanya/ml_anaconda:latest
```
This docker has both `ROOT TMVA` and `PyTorch` environments available.

### Start the docker

Launch the docker:
```
docker run -it --name="anaconda" -p 8888:8888 -v $PWD:/host nyanyanyanyanyanya/ml_anaconda  /bin/bash
```

Then do the following in the command line:
```
conda activate MLexample
cd home/DNN
```

### Running the notebooks

Within the command line, open the notebook
```
jupyter notebook --ip='*' --port=8888  --allow-root DNN_regression_example.ipynb
```

Then open your browser that you can work with the notebook
