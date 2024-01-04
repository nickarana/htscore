
       <form action="{{ url_for('extreme_ca_teamid_')}}" method="GET">
           <div>
            <label for='teamid' display='inline-block',width='110px'>TeamID</label>
            <input type='text' name='teamid' placeholder='145644' padding='5px 10px' style="width:50%;" autofocus required/>
            <button type="submit" class="btn btn-primary">Calculate</button>
           </div>
       </form>
       <form action="{{ url_for('extreme_ca_teamname_')}}" method="GET">
            TeamName : <input type='text' name='teamname' placeholder='FC de Oosterballers' required/><br>
            <button type="submit" class="btn btn-primary">Calculate</button>
       </form>
       <form action="{{ url_for('extreme_ca_country_')}}" method="GET">
            Country : <input type='text' name='country' placeholder='Netherlands' required/><br>
            <button type="submit" class="btn btn-primary">Calculate</button>
       </form>
       <form action="{{ url_for('extreme_ca_competition_')}}" method="GET">
            Competition (L = League, C = Cup, P = Promotion, H = Hattrick Masters, I = International) : <input type='text' name='competition' placeholder='I' required/><br>
            <button type="submit" class="btn btn-primary">Calculate</button>
       </form>


      <form method="GET">
           <label for="xca_filter">Choose a field on which to filter, or scroll down to see the top 100 ratings since S69:</label>
           <select name="xca_filter" class="Input" id="xca_filter">
             <option value="TeamID">TeamId</option>
             <option value="TeamName">TeamName</option>
             <option value="Country">Country</option>
             <option value="Season">Season (International; current season = 85)</option>
             <option value="Comp">Competition (L=League, C=Cup, P=Promotion, H=HT Masters,I=International) </option>
           </select>
       </form>


       
@app.route('/extreme_ca/teamid/', methods =("GET","POST"))
def extreme_ca_teamid_():
    XCA_=XCA_teamid(XCA(),int(request.args.get("teamid")))
    XCA_
    return render_template('template_xca_form.html',tables=[XCA_],titles=[''])

@app.route('/extreme_ca/teamname/', methods =("GET","POST"))
def extreme_ca_teamname_():
    XCA_=XCA_teamname(XCA(),request.args.get("teamname"))
    XCA_
    return render_template('template_xca_form.html',tables=[XCA_],titles=[''])

@app.route('/extreme_ca/country/', methods =("GET","POST"))
def extreme_ca_country_():
    XCA_=XCA_country(XCA(),request.args.get("country"))
    XCA_
    return render_template('template_xca_form.html',tables=[XCA_],titles=[''])

@app.route('/extreme_ca/competition/', methods =("GET","POST"))
def extreme_ca_competition_():
    XCA_=XCA_competition(XCA(),request.args.get("competition"))
    XCA_
    return render_template('template_xca_form.html',tables=[XCA_],titles=[''])

##def match_predict_():
##    XCA
##    return render_template('heroku_match_predict.html',tables=[mp2,mp0,mp1],titles=['Match Overview','Chance Breakdown','Special Events Breakdown'])



from flask import Flask, request,render_template
from pychpp import CHPP  
import pandas as pd
import numpy as np
from pa_match_predict import match_predict

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

if __name__ == '__main__':
    app.debug=True
    app.run(debug=True,use_reloader=False)




    <style>
      div {
        margin-bottom: 10px;
      }
      label {
        display: inline-block;
        width: 110px;
        color: #777777;
      }
      input {
        padding: 5px 10px;
      }
    </style>
    style="display:grid; grid-template-columns: max-content max-content; grid-gap:5px; width:50%; label: "
    <!DOCTYPE html>
<html>
  <head>
    <title>HT Score</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.css" />
    <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.js"></script>
  </head>
  <header>
      <div class="container">
        <h1 class="logo">Nickarana's Hattrick Stats</h1>
        <strong><nav>
          <ul class="menu">
            <li><a href="{{ url_for('home') }}">Home</a></li>
          </ul>
        </nav></strong>
      </div>
    </header>
    <div class="extreme_ca">
       <h1>Extreme CA Top Ratings</h1>
    </div>
    {% for table in tables %}
          <br>
          <br>
          <b>{{ titles[loop.index-1]|safe }}</b>
          <br>
          {{ table|safe }}
    {% endfor %}
</html>
