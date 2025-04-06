import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
import streamlit as st

start = '2010-01-01'
end = '2023-12-31'
st.title('Stock Trend Prediction')
user_input = st.text_input('Enter Stock Ticker', 'AAPL')
df = yf.download(user_input, start=start, end=end)
#Describing Data
st.subheader('Data from 2010 - 2023')
st.write(df.describe())
#Visualizations
st. subheader('Closing Price vs Time chart')
fig = plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

# Splitting data into train and test
data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
data_training_array= scaler.fit_transform(data_training)
data_training_array

model= load_model('keras_model.h5')

past_100_days= data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)

input_data= scaler.fit_transform(final_df)

x_test=[]
y_test=[]

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test, y_test= np.array(x_test), np.array(y_test)

#making predicts
y_predicted= model.predict(x_test)

scale_factor=scaler.scale_

scale_factor= 1/scale_factor
y_predicted= y_predicted*scale_factor
y_test= y_test*scale_factor

fig = plt.figure(figsize = (12,6))
plt.plot(y_test, 'b', label= 'Original Price')
plt.plot(y_predicted, 'r', label= 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
st.pyplot(fig)