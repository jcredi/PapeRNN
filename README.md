# Article titles generator

This is an overnight project where I had a lot of fun mining scientific article data from the [arXiv](https://arxiv.org/) and training an [LSTM](https://www.google.it/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwj1vtjD6vnQAhUGWxQKHQ42B48QFggzMAM&url=http%3A%2F%2Fdeeplearning.cs.cmu.edu%2Fpdfs%2FHochreiter97_lstm.pdf&usg=AFQjCNGoFvqrva4rDCNIcqNe_SiPL_VPxg) for generating new article titles.

## Requirements

* [Python 2.7](https://www.python.org/downloads/) (tested on 2.7.12 on Ubuntu 16.04)
* [Keras](https://keras.io/), a high-level neural networks library. See the [documentation](https://keras.io/#installation) for installation instructions.
* A backend for Keras. Here you can either choose [TensorFlow](https://www.tensorflow.org/) ([installation instructions](https://www.tensorflow.org/get_started/os_setup)) or [Theano](http://deeplearning.net/software/theano/) ([installation instructions](http://deeplearning.net/software/theano/install.html)). I have personally tested this specific project with Theano (8.2) only, but I frequently use TensorFlow as Keras backend in other projects and it works just as well (if not faster, after the last release).
* CUDA and cuDNN. Optional, but highly recommended, as training LSTMs is quite computationally intensive. See [this page](https://www.tensorflow.org/get_started/os_setup#optional_install_cuda_gpus_on_linux) for CUDA/cuDNN installation instructions if you are using TensorFlow, or [this page](http://deeplearning.net/software/theano/tutorial/using_gpu.html) if you are using Theano.


## Usage
The entire project takes up less than 250 lines of python code and consists of two simple scripts.

First, we'll need to mine some data. Let's say we want to download all titles of 2015 arXiv papers from the Machine Learning section, and save them for later use. We can simply run
```{r, engine='shell', count_lines}
python harvester.py --arxiv=stat --category=stat.ML --dateFrom=2015-01-01 --dateTo=2015-12-31 --dataDumpPath=./data/dump_2015.csv
```
This will download arXiv metadata using the [OAI protocol](https://arxiv.org/help/oa/index) and save it to file "./data/dump_2015.csv".

Feel free to run
```{r, engine='shell', count_lines}
python harvester.py -h
```
for help on how to use the data harvester script and which argument it accepts.

## License

MIT &copy; 2016 Jacopo Credi
