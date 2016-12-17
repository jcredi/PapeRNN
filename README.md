# Article titles generator

This is an overnight project where I had a lot of fun mining scientific article data from the [arXiv](https://arxiv.org/) and training an [Long Short Term Memory (LSTM)](https://www.google.it/url?sa=t&rct=j&q=&esrc=s&source=web&cd=4&cad=rja&uact=8&ved=0ahUKEwj1vtjD6vnQAhUGWxQKHQ42B48QFggzMAM&url=http%3A%2F%2Fdeeplearning.cs.cmu.edu%2Fpdfs%2FHochreiter97_lstm.pdf&usg=AFQjCNGoFvqrva4rDCNIcqNe_SiPL_VPxg) neural network for generating new article titles.

## Requirements

* [Python 2.7](https://www.python.org/downloads/) (tested on 2.7.12 on Ubuntu 16.04)
* [Keras](https://keras.io/), a high-level neural networks library. See the [documentation](https://keras.io/#installation) for installation instructions.
* A backend for Keras. You can either choose [TensorFlow](https://www.tensorflow.org/) ([installation](https://www.tensorflow.org/get_started/os_setup)) or [Theano](http://deeplearning.net/software/theano/) ([installation](http://deeplearning.net/software/theano/install.html)). I have personally tested this specific project with Theano (8.2) only, but I frequently use TensorFlow as Keras backend in other projects and it works just as well (if not faster, after the last release).
* CUDA and cuDNN. Optional, but highly recommended, as training LSTMs is quite computationally intensive. See [this page](https://www.tensorflow.org/get_started/os_setup#optional_install_cuda_gpus_on_linux) for CUDA/cuDNN installation instructions if you are using TensorFlow, or [this page](http://deeplearning.net/software/theano/tutorial/using_gpu.html) if you are using Theano.


## Usage (with examples)
The entire project takes up less than 250 lines of python code and consists of two simple scripts.

### Data harvesting

First, we'll need to mine some data. Let's say we want to download all titles of 2015 arXiv papers from the Machine Learning section, and save them for later use. We can simply run
```{r, engine='shell', count_lines}
python harvester.py --arxiv=stat --category=stat.ML --dateFrom=2015-01-01 --dateTo=2015-12-31 --dataDumpPath=./data/dump_2015.csv
```
This will download arXiv metadata using the [OAI protocol](https://arxiv.org/help/oa/index) and save it to file "./data/dump_2015.csv".
A note: arXiv uses 503 Retry-After replies to implement flow control, so it's totally OK if you get a lot of 503 errors. Just be patient until your precious metadata is downloaded :)

Feel free to run
```{r, engine='shell', count_lines}
python harvester.py -h
```
for help on how to use the data harvester script and which argument it accepts.

### LSTM training

Next, we are going to use this data to train our LSTM. We can simply run
```{r, engine='shell', count_lines}
python lstmtrainer.py --dataDumpPath=./data/dump_2015.csv
```
to start training an LSTM on the data we just downloaded, with default parameters. Again, if you wish to look under the hood, just run
```{r, engine='shell', count_lines}
python lstmtrainer.py -h
```
and play around with hyperparameters!

### Sample console output

```{r, engine='bash', count_lines}
Using Theano backend.
Using gpu device 0: GeForce GTX 850M (CNMeM is disabled, cuDNN 5105)
Corpus length: 128762
Total chars: 83
Number of sequences: 42908
One-hot vectorization...
Build model...

--------------------------------------------------
Epoch  1
Epoch 1/1
42908/42908 [==============================] - 20s - loss: 2.3533     
----- Generating with seed: "ing Pharmacotherapy Using Belgian Health"
ing Pharmacotherapy Using Belgian Health in Near and Malk Apporening Matrix Procenser Searne Learning with Spale Bayes Cols Ding Stochamal Mastor Learning and Malus. A Bayesian Spare Stor and Deng  alaning Maluly Coustem Bayesed Complimation and Proc A Bayesian Sparser Anger prorencal Sparsent Duta Men-in and Learning and Sparses Comparing Learning and Deng Learning and Sparsing an niar Regre Learning and Spal Maling Congering Gayes Ral
--------------------------------------------------
```
...5 epochs later...
```{r, engine='bash', count_lines}
--------------------------------------------------
Epoch  5
Epoch 1/1
42908/42908 [==============================] - 20s - loss: 1.2124     
----- Generating with seed: "stic Model to a Deterministic Algorithm."
stic Model to a Deterministic Algorithm. Process Convergence. Bayesian ivery A Gaussian process Factorization. Factorization for Deep Bayesian Processes. Active Models for Measures. Stochastic Training Time Matrix Models. Active Decomposition. Scalable latent Variational Sparse Factoring. A Process analysic Finter Factorized StochasticNent Grasianal Computational Structures. A Markov Strankngationing using Process Models. Processes. Pro
--------------------------------------------------
```
...and 5 more...
```{r, engine='bash', count_lines}
--------------------------------------------------
Epoch  10
Epoch 1/1
42908/42908 [==============================] - 20s - loss: 0.9872     
----- Generating with seed: "sitions via the Subspace Norm. Different"
sitions via the Subspace Norm. Differential Inference for Classification of the a distance Belabal Mantinal Modeling with Incomplete Detection and Markov Completion in Diracter Pricting. The data Application to networks. Estimation for Large Statistical Models for Convex algorithms. An Bayesian Functional Divilization and Matrix Factorization. A Sensing data monding Gaussian Markov and antion and Attions in a Generalized Baltming Networ
--------------------------------------------------
```
...and 5 more...
```{r, engine='bash', count_lines}
--------------------------------------------------
Epoch  15
Epoch 1/1
42908/42908 [==============================] - 20s - loss: 0.8873     
----- Generating with seed: "ce Functions for Machine Learning: Nonpa"
ce Functions for Machine Learning: Nonparametric Invent Sparse Learning with Application to lommetory for Markov Models for Deep Neural Networks. Parallel Series of the Options. A Columply Gaussian Process Point Algorithms for Distributed Randomization Markov Models. Policient Detection. Semi-supervised Sparse Selection of Distributed Distributed Stage Compressed for the reyp-Addisting deep Learning in Reweinical Comparisonal Sequential
--------------------------------------------------
```

## License

MIT &copy; 2016 Jacopo Credi
