from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS  
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Load CSV
        df = pd.read_csv('WDAP\\seattle-weather.csv')

        # Validate columns
        required_columns = {'date', 'temp_max', 'temp_min'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': f'CSV must contain columns: {required_columns}'}), 400

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df['temp'] = (df['temp_max'] + df['temp_min']) / 2

        # Prepare data for regression
        X = df['date'].map(datetime.toordinal).values.reshape(-1, 1)
        y = df['temp'].values
        model = LinearRegression()
        model.fit(X, y)

        # Get selected start date from user
        req_data = request.get_json()
        start_date_str = req_data.get('start_date')
        if not start_date_str:
            return jsonify({'error': 'Start date not provided'}), 400

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        except:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        # Predict for next 7 days from selected date
        predictions = []
        for i in range(7):
            date_pred = start_date + timedelta(days=i)
            x_pred = np.array([[date_pred.toordinal()]])
            y_pred = model.predict(x_pred)[0]
            predictions.append({
                'date': date_pred.strftime('%Y-%m-%d'),
                'temp': round(float(y_pred), 2)
            })

        # Prepare historical data to plot as well
        history = df[['date', 'temp']].copy()
        history['date'] = history['date'].dt.strftime('%Y-%m-%d')
        history_list = history.to_dict(orient='records')

        return jsonify({
            'history': history_list,
            'predictions': predictions
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)





# python WDAP\System.py