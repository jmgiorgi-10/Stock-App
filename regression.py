import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

engine = create_engine("mysql+pymysql://root:riverplate10@localhost/stocks")

query = "Select * From StockEvents"
df = pd.read_sql(query, engine)

# Right now last 70 datapoints are predicted by previous 30 datapoints
df = df[:100]

print(df.columns)

# Set the amount of lags we wish to use for each feature
LAG = 5
features = ["open", "high", "low", "close", "volume"]

# Start with linear regression --> need to introduce lag to adapt regression to time-series data.
def lag_features(data, lag=10):
    
    df = data.copy()
    for feature in features:
        for i in range(1, lag + 1):
            df[f'{feature}_lag{i}'] = df[feature].shift(i)

    for feature in features:
        df.pop(feature) # now remove non-lagged features, to avoid data leakage.

    # remove nans due to lagged features
    df = df.dropna()
        
    return df
    # print("Lagged dataframe: ", df)

# Define train/test split ratio
train_size = int(len(df) * 0.3)

# Split the data into training and test sets based on time
train, test = df[:train_size], df[train_size:]
test = df.reset_index(drop='True')

y_train = train['close'][LAG:]
X_train = lag_features(train, LAG)

y_test = test['close'][LAG:]
X_test = lag_features(test, LAG)

model = LinearRegression()
model.fit(X_train, y_train)

# Predict next 70 datapoints, based on previous 30.
y_pred = model.predict(X_test)

# Prepend previous 30 datapoints to y_pred for visualization
y_pred_all = np.concat([y_train, y_pred])

# All datapoints
y_all = np.concat([y_train, y_test])

plt.plot(y_pred_all, label = 'predicted')
plt.plot(y_all, label = 'actual')
plt.title("Predicted vs Actual stock price over time")
plt.xlabel("Time step")
plt.ylabel("Closing stock price")
plt.legend()
plt.show()