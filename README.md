# Predicting metlink bus route data from historical ping data
Using Keras and Tensorflow LSTM to use bus ping sequences from Wellington, New Zealand to predict bearing, location, and delays

##Dependencies

* keras
* tensorflow

Install Keras from [here](https://keras.io/) and Tensorflow from [here](https://www.tensorflow.org/versions/r0.12/get_started/os_setup). 

##Usage

![Alt text](/accuracy-graph.png?raw=true "Prediction Accuracy - One time step ahead")

Run this using [jupyter notebook](http://jupyter.readthedocs.io/en/latest/install.html). Just type `jupyter notebook` in the main directory and the code will pop up in a browser window. 

In order to generate data run the stopstat.py.  this pulls data every 30 seconds from metlink for the specified bus.  Default is set to bus #83.  If data hasn't updated, it doesnt store it.  Data is appended to the bus.csv file.

LSTM run from jupyter notebook pulls a single column (bearing by default) and predicts bearing changes (turns) one time step ahead of bus current position.  


##Credits

Credits go to [jaungiers](https://github.com/jaungiers/LSTM-Neural-Network-for-Time-Series-Prediction).

Wrapper credit goes to Siraj Raval https://www.youtube.com/watch?v=ftMq5ps503w&t=521s

Metlink api info credit to https://github.com/reedwade/metlink-api-maybe



