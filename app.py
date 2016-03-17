import pandas as pd
from flask import Flask, render_template, request, redirect
import requests
from bokeh.plotting import figure, output_file, show, save

app = Flask(__name__)

app.vars = {}

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
#request was a POST
        app.vars['abbrev'] = request.form['abbrev']

        abbrev = app.vars['abbrev']

        f = open('%s.txt'%(app.vars['abbrev']),'w')
        f.write('Stock abbreviation: %s'%(app.vars['abbrev']))
        f.close()

        #Get the closing value of the stock over the last month into a pandas Series:
        StockURL = 'https://www.quandl.com/api/v3/datasets/WIKI/' + abbrev + '.csv'
        dataSet = pd.read_csv(StockURL, parse_dates=['Date'])

        output_file('templates/datetime_'+abbrev+'.html')

        p = figure(width=800, height=250, x_axis_type="datetime", title=abbrev, y_axis_label='Price (in dollars)')

        #p.grid.bounds(dataSet['Date'][0], dataSet['Date'][29])
        #print dataSet['Date'][0], dataSet['Date'][29]
        p.line(dataSet[0:30]['Date'], dataSet[0:30]['Close'], color='navy', alpha=0.5, legend = 'Closing price')
        if 'adjustedClose' in request.form:
            p.line(dataSet[0:30]['Date'], dataSet[0:30]['Adj. Close'], color='purple', alpha=0.5, legend = 'Adjusted Closing price')
        if 'openValue' in request.form:
            p.line(dataSet[0:30]['Date'], dataSet[0:30]['Open'], color='red', alpha=0.5, legend = 'Opening price')
        if 'adjustedOpen' in request.form:
            p.line(dataSet[0:30]['Date'], dataSet[0:30]['Adj. Open'], color='black', alpha=0.5, legend = 'Adjusted opening price')
            
        p.legend.orientation = "top_left"

        save(p)
        return render_template('datetime_'+abbrev+'.html')

@app.route('/',methods=['GET','POST'])
def next():
    return redirect('/index')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

#  app.run(port=33507)
