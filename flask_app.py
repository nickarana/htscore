from flask import Flask, request,render_template
from pychpp import CHPP
import pandas as pd
import numpy as np
from pa_match_predict import match_predict
from pa_xca import XCA,XCA_100,XCA_filter,XCAT
import pa_hts_mappings as htsm

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('heroku_test_home.html')

@app.route('/matchpredict/', methods =("GET","POST"))
def match_predict_():
    if request.method =='POST':
        mp0,mp1,mp2,mp3 = match_predict(int(request.form.get("matchid")))
    else:
        mp0,mp1,mp2,mp3 = match_predict(int(request.args.get("matchid")))
    return render_template('heroku_match_predict.html',tables=[mp2,mp0,mp1],titles=['Match Overview','Chance Breakdown','Special Events Breakdown'])


@app.route('/extreme_ca/', methods =("GET","POST"))
def extreme_ca_():
    XCA_= XCA_100(XCA(htsm.csvXCA,htsm.cols_XCA,htsm.cols_XCA_out,'HatXmid'))
    XCA_
    return render_template('template_xca_v3.html',tables=[XCA_],titles=[''])

@app.route('/extreme_ca/filter/', methods =("GET","POST"))
def extreme_ca_filter_():
    XCA_= XCA_filter(XCA(htsm.csvXCA,htsm.cols_XCA,htsm.cols_XCA_out,'HatXmid'),request.args.get("filter"),1)
    XCA_
    return render_template('template_xca_filter.html',tables=[XCA_],titles=[''])

@app.route('/extreme_ca/team/', methods =("GET","POST"))
def extreme_ca_team_():
    XCA_= XCAT(XCA_filter(XCA(htsm.csvXCA,htsm.cols_XCA,htsm.cols_XCA_out,'HatXmid'),request.args.get("filter_team"),0),'HatXmid')
    XCA_
    return render_template('template_xca_filter.html',tables=[XCA_],titles=[''])

@app.route('/high_hat/', methods =("GET","POST"))
def high_hat_():
    XCA_= XCA_100(XCA(htsm.csvXHH,htsm.cols_XHH,htsm.cols_XHH_out,'HatStats'))
    XCA_
    return render_template('template_xhh_v3.html',tables=[XCA_],titles=[''])

@app.route('/high_hat/filter/', methods =("GET","POST"))
def high_hat_filter_():
    XCA_= XCA_filter(XCA(htsm.csvXHH,htsm.cols_XHH,htsm.cols_XHH_out,'HatStats'),request.args.get("filter"),1)
    XCA_
    return render_template('template_xhh_filter.html',tables=[XCA_],titles=[''])

@app.route('/high_hat/team/', methods =("GET","POST"))
def high_hat_team_():
    XCA_ = XCAT(XCA_filter(XCA(htsm.csvXHH,htsm.cols_XHH,htsm.cols_XHH_out,'HatStats'),request.args.get("filter_team"),0),'HatStats')
    XCA_
    return render_template('template_xhh_filter.html',tables=[XCA_],titles=[''])

@app.route('/masters/', methods =("GET","POST"))
def masters_():
    XCA_= XCA_100(XCA(htsm.csvHTM,htsm.cols_HTM,htsm.cols_HTM_out,'HTSN'))
    XCA_
    return render_template('template_htm_v3.html',tables=[XCA_],titles=[''])

@app.route('/masters/filter/', methods =("GET","POST"))
def masters_filter_():
    XCA_= XCA_filter(XCA(htsm.csvHTM,htsm.cols_HTM,htsm.cols_HTM_out,'HTSN'),request.args.get("filter"),1)
    XCA_
    return render_template('template_htm_filter.html',tables=[XCA_],titles=[''])

@app.route('/masters/team/', methods =("GET","POST"))
def masters_team_():
    XCA_ = XCAT(XCA_filter(XCA(htsm.csvHTM,htsm.cols_HTM,htsm.cols_HTM_out,'HTSN'),request.args.get("filter_team"),0),'HTSN')
    XCA_
    return render_template('template_htm_filter.html',tables=[XCA_],titles=[''])


if __name__ == '__main__':
    app.debug=True
    app.run(debug=True,use_reloader=False)
