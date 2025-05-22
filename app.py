
## Local Prototype version of Flask web app with linear regression ##

from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
from db import Database
from fetch import Fetch
from regression import Regression
import pickle
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

app = Flask(__name__)

fetch = Fetch()
# today = datetime.today()
# dates = [(today - timedelta(days=i)) for i in range(31)]

# data = []
# for date in dates:

# train linear regression model before loading the main page

global rg

# with open('model.pkl', 'wb') as f:
#     pickle.dump(model, f)

@app.route('/')
def home():
    return render_template('index.html', plot_div=None, symbol=None)

@app.route('/predict', methods=['POST'])
def predict(): 

    symbol = request.form['Symbol']
    import pdb; pdb.set_trace()
    data = fetch.fetch_stocks(request.form['Symbol'], True) # set store (in postgres container) to True.
    rg = Regression(data)

    feature_transformation = None

    if 'sma_checkbox' in request.form:
        feature_transformation = 'SMA'

    rg.train(feature_transformation)

    predicted_time_series = rg.evaluate()
    # make sure the predicted values can't delve below 0.
    predicted_time_series = np.clip(predicted_time_series, a_min=0, a_max=None)
    # Now, plot using plotly below:
    print("predicted")
    print(predicted_time_series)
    print("actual")
    print(rg.y_all)
    import pdb; pdb.set_trace()
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=predicted_time_series[-1000:], mode='lines', name='predicted'))
    fig.add_trace(go.Scatter(y=rg.y_all[-1000:], mode='lines', name='actual'))
    plot_html = pio.to_html(fig, full_html=False)

    return render_template('index.html', plot_div=plot_html, symbol=symbol)

    # fig.show()


if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0')