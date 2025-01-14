import numpy as np
from math import pi
from random import random
from random import randint
from random import uniform
from numpy import array
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense

# generate damped sine wave in [0,1]
def generate_sequence(length, period, decay):
    return [0.5+0.5*np.sin(2*pi*i / period) * np.exp(-decay *i) for i in
            range(length)]

def generate_examples(length, n_patterns, output):
    X , y = list(), list()
    for _ in range(n_patterns):
        p = randint(10,20)
        d = uniform(0.01, 0.1)
        sequence = generate_sequence(length+output, p, d)
        X.append(sequence[:-output])
        y.append(sequence[-output:])
    X = array(X).reshape(n_patterns, length,1)
    y = array(y).reshape(n_patterns, output)
    return X, y
'''
X, y =generate_examples(20,5,5)
for i in range(len(X)):
    pyplot.plot([x for x in X[i,:,0]] + [x for x in y[i]], "-o")
pyplot.show()
'''
# configure problem
length = 50
output = 5
#define model
model = Sequential()
model.add(LSTM(20, return_sequences=True, input_shape=(length, 1)))
model.add(LSTM(20))
model.add(Dense(output))
model.compile(loss='mae', optimizer='adam')
print(model.summary)

# fit model
X, y = generate_examples(length, 10000, output)
history = model.fit(X, y, batch_size=10, epochs=1)

# evaluate model
X, y = generate_examples(length, 1000, output)
loss = model.evaluate(X,y, verbose=0)
print('MAE: %f'% loss)

# prediction on new data
X, y = generate_examples(length, 1, output)
yhat = model.predict(X, verbose=0)
pyplot.plot(y[0], label='y')
pyplot.plot(yhat[0], label='yhat')
pyplot.legend()
pyplot.show()
