import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
# engine = create_engine("mysql+pymysql://root:riverplate10@localhost/stocks")

# query = "Select * From StockEvents"
# df = pd.read_sql(query, engine)

# Right now last 70 datapoints are predicted by previous 30 datapoints
class Regression:

    def __init__(self, data, lags=5):
        self.data = data
        self.lags = lags
        # re-add volume after normalizing this feature
        self.features = ["1. open", "2. high", "3. low", "4. close"]

        # define whether the input features should be converted to exponentially weighed moving average (EWMA).
        # source: https://ethz.ch/content/dam/ethz/special-interest/mtec/chair-of-entrepreneurial-risks-dam/documents/dissertation/master%20thesis/MAS_Johan_Boissard_Dec12.pdf
        self.moving_avg_input = False

        self.y_train = None
        self.X_train = None
        self.y_test = None
        self.X_test = None
        self.model = None

        self.y_pred_all = None
        self.y_all = None

    # avg_num: simple moving average is based on the last 'avg_num' number of datapoints.
    def simple_moving_average(self, data):

        import pdb; pdb.set_trace()

        df = data.copy()

        for feature in df.columns:
            sma_feature = f'{feature}_sma'
            df[sma_feature] = df[feature].rolling(window=10, min_periods=1).mean()

        return df


    def lag_features(self, data):
    
        df = data.copy()
        for feature in self.features:
            for i in range(1, self.lags + 1):
                df[f'{feature}_lag{i}'] = df[feature].shift(i)

        for feature in self.features:
            df.pop(feature) # now remove non-lagged features, to avoid data leakage.

        # remove nans due to lagged features
        df = df.dropna()
            
        return df


    def train(self, feature_transformation=None):

        # Define train/test split ratio
        train_size = int(len(self.data) * 0.3)

        # Split the data into training and test sets based on time
        train, test = self.data[:train_size], self.data[train_size:]
        test = self.data.reset_index(drop='True')

        import pdb; pdb.set_trace()
        # Use the closing price of each 5-min interval as the label
        self.y_train = train['4. close'][self.lags:]
        self.y_test = test['4. close'][self.lags:]
        
        self.X_train = self.lag_features(train)
        self.X_test = self.lag_features(test)
        # Simple moving average.
        if feature_transformation == 'SMA':
            self.X_train = self.simple_moving_average(self.X_train)
            self.X_test = self.simple_moving_average(self.X_test)

        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)


    def evaluate(self):
# # Predict next 70 datapoints, based on previous 30.
        import pdb; pdb.set_trace()

        y_pred = self.model.predict(self.X_test)

        self.y_train = self.y_train.to_numpy().astype(np.float64) # convert from pandas series to numpy array.
        self.y_test = self.y_test.to_numpy().astype(np.float64) # convert from pandas series to numpy array.

        # Prepend previous 30 datapoints to y_pred for visualization
        self.y_pred_all = np.concat([self.y_train, y_pred])

        # All datapoints
        self.y_all = np.concat([self.y_train, self.y_test])

        return self.y_pred_all

        # plt.plot(y_pred_all, label = 'predicted')
        # plt.plot(y_all, label = 'actual')
        # plt.title("Predicted vs Actual stock price over time")
        # plt.xlabel("Time step")
        # plt.ylabel("Closing stock price")
        # plt.legend()
        # plt.show()