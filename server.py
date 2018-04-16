#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from flask_table import Table, Col

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
print "Hello world!"
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.227.79.146/proj1part2
DATABASEURI = "postgresql://kdf2118:3632@35.227.79.146/proj1part2"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  cursor2 = g.conn.execute("SELECT * FROM piece")
  dates2 = []
  for result in cursor2:
    dates2.append(result['date'])
  cursor2.close()  

  cursor = g.conn.execute("SELECT DISTINCT school FROM studies")
  schools = []
  for result in cursor:
    schools.append(result['school'])
  cursor.close()

  cursor = g.conn.execute("SELECT row_name FROM rower_info")
  rowers = []
  for result in cursor:
    rowers.append(result['row_name'])
  cursor.close()

  cursor = g.conn.execute("SELECT piece_id FROM piece")
  pids2 = []
  for result in cursor:
    pids2.append(result['piece_id'])
  cursor.close()
 
  cursor = g.conn.execute("SELECT team_name FROM rower_info ORDER BY team_name")
  hsteams = []
  for result in cursor:
    hsteams.append(result['team_name'])
  cursor.close()
  
  cursor = g.conn.execute("SELECT DISTINCT concat FROM master_pieces") 
  piecenames = []
  for result in cursor:
    piecenames.append(result['concat'])
  cursor.close()

  return render_template("index.html", piecenames=piecenames, dates2=dates2, schools=schools, rowers=rowers, pids2=pids2, hsteams=hsteams)

@app.route('/another')
def another():
  return render_template("another.html")

@app.route('/piece', methods = ['POST'])
def piece():
  date = request.form['dates']
  if date == "all":
    cursor2 = g.conn.execute("SELECT * FROM all_pieces ORDER BY piece_id")
  else:
    cursor2 = g.conn.execute("SELECT * FROM all_pieces WHERE date = '{0}' ORDER BY piece_id".format(date))
  pids3 = []
  dates = []
  repnums = []
  rest = []
  lengths = []
  for result in cursor2:
    pids3.append(result['piece_id'])
    dates.append(result['date'])
    repnums.append(result['rep_num'])
    rest.append(result['rest'])
    lengths.append(result['length'])
  cursor2.close()
  context = dict(data = (pids3, dates, lengths, repnums, rest))
  return render_template("piece.html", **context)

@app.route('/piece_ids', methods = ['POST'])
def piece_ids():
  pid = request.form['pids']
  if date == "all":
    cursor2 = g.conn.execute("SELECT * FROM all_pieces ORDER BY piece_id")
  else:
    cursor2 = g.conn.execute("SELECT * FROM all_pieces WHERE piece_id = '{0}' ORDER BY piece_id".format(pid))
  pids3 = []
  dates = []
  repnums = []
  rest = []
  lengths = []
  for result in cursor2:
    pids3.append(result['piece_id'])
    dates.append(result['date'])
    repnums.append(result['rep_num'])
    rest.append(result['rest'])
    lengths.append(result['length'])
  cursor2.close()
  context = dict(data = (pids3, dates, lengths, repnums, rest))
  return render_template("piece_ids.html", **context)

@app.route('/teammembers', methods = ['POST'])
def teammembers():
  school = request.form['school']
  if school == "all":
    cursor= g.conn.execute("SELECT * FROM studies ORDER BY uni")
  else:
    cursor = g.conn.execute("SELECT * FROM studies WHERE school = '{0}' ORDER BY uni".format(school))
  unis = []
  gpas = []
  majors = []
  schools = []
  for result in cursor:
    unis.append(result['uni'])
    gpas.append(result['gpa'])
    majors.append(result['maj_name'])
    schools.append(result['school'])
  cursor.close()
  context = dict(data = (unis, schools, majors, gpas))
  return render_template("teammembers.html", **context)

@app.route('/winners', methods = ['POST'])
def winners():
  winners = request.form['winners']
  if winners == "allw":
    cursor= g.conn.execute("SELECT * FROM winners ORDER BY piece_id")
  else:
    cursor = g.conn.execute("SELECT * FROM winners WHERE date = '{0}' ORDER BY piece_id".format(winners))
  pids = []
  lengths = []
  reps = []
  rest = []
  splits = []
  dates = []
  rowers = []
  grads = []
  isrecruit = []
  for result in cursor:
    pids.append(result['piece_id'])
    lengths.append(result['length'])
    reps.append(result['rep_num'])
    rest.append(result['rest'])
    splits.append(result['split_speed'])
    dates.append(result['date'])
    rowers.append(result['row_name'])
    grads.append(result['year'])
    isrecruit.append(result['is_recruit'])
  cursor.close()
  context = dict(data = (pids, lengths, reps, rest, splits, dates, rowers, grads, isrecruit))
  return render_template("winners.html", **context)

@app.route('/pieces_by_rower', methods = ['POST'])
def pieces_by_rower():
  rowers = request.form['pcsbyrower']
  if rowers == "all":
    cursor= g.conn.execute("SELECT * FROM pcs_by_rowers ORDER BY row_name")
  else:
    cursor = g.conn.execute("SELECT * FROM pcs_by_rowers WHERE row_name = '{0}' ORDER BY row_name".format(rowers))
  row_names = []
  unis = []
  grads = []
  pids = []
  lengths = []
  reps = []
  rests = []
  splits = []
  dates = []
  for result in cursor:
    pids.append(result['piece_id'])
    lengths.append(result['length'])
    reps.append(result['rep_num'])
    rests.append(result['rest'])
    splits.append(result['split_speed'])
    dates.append(result['date'])
    row_names.append(result['row_name'])
    grads.append(result['year'])
    unis.append(result['uni'])
  cursor.close()
  context = dict(data = (row_names, unis, grads, pids, lengths, reps, rests, splits, dates))
  return render_template("pieces_by_rower.html", **context)

@app.route('/rowerinfo', methods = ['POST'])
def rowerinfo():
  rowers = request.form['rowers']
  if rowers == "all":
    cursor= g.conn.execute("SELECT * FROM rower_info ORDER BY row_name")
  else:
    cursor = g.conn.execute("SELECT * FROM rower_info WHERE row_name = '{0}'".format(rowers))
  names = []
  grads = []
  zips = []
  unis = []
  hsteams = []
  isclub = []
  isrecruit = []
  collegeteams = []
  gpas = []
  majors = []
  schools = []
  ranks = []
  for result in cursor:
    names.append(result['row_name'])
    grads.append(result['year'])
    zips.append(result['zip_code'])
    unis.append(result['uni'])
    hsteams.append(result['team_name'])
    isclub.append(result['is_club'])
    isrecruit.append(result['is_recruit'])
    collegeteams.append(result['class'])
    gpas.append(result['gpa'])
    majors.append(result['maj_name'])
    schools.append(result['school'])
    ranks.append(result['rank'])
  cursor.close()
  context = dict(data = (names, grads, unis, zips, hsteams, isclub, isrecruit, collegeteams, gpas, majors, schools, ranks))
  return render_template("rowerinfo.html", **context)

@app.route('/rower_by_hsteam', methods = ['POST'])
def rower_by_hsteam():
  hsteam2 = request.form['hsteams']
  if hsteam2 == "all":
    cursor= g.conn.execute("SELECT * FROM rower_info ORDER BY row_name")
  else:
    cursor = g.conn.execute("SELECT * FROM rower_info WHERE team_name = '{0}'".format(hsteam2))
  names = []
  grads = []
  zips = []
  unis = []
  hsteams = []
  isclub = []
  isrecruit = []
  collegeteams = []
  gpas = []
  majors = []
  schools = []
  ranks = []
  for result in cursor:
    names.append(result['row_name'])
    grads.append(result['year'])
    zips.append(result['zip_code'])
    unis.append(result['uni'])
    hsteams.append(result['team_name'])
    isclub.append(result['is_club'])
    isrecruit.append(result['is_recruit'])
    collegeteams.append(result['class'])
    gpas.append(result['gpa'])
    majors.append(result['maj_name'])
    schools.append(result['school'])
    ranks.append(result['rank'])
  cursor.close()
  context = dict(data = (names, grads, unis, zips, hsteams, isclub, isrecruit, collegeteams, gpas, majors, schools, ranks))
  return render_template("rower_by_hsteam.html", **context)

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO major(school, maj_name) VALUES (\'CC\', %s)', name)
  return redirect('/')

@app.route('/addpiece', methods = ['POST'])
def addpiece():
  print "working at first..."
  date = "15/04/2018"
  piece = request.form['pieces']
  print "form requests working..."
  cursor = g.conn.execute("SELECT max(p.piece_id) FROM piece p")
  print "first select working..."
  id_to_insert = ((cursor.fetchone()[0]) + 1)
  print "fetchone bullshit working..."
  cursor.close()  

  cursor = g.conn.execute("SELECT DISTINCT piece_id FROM master_pieces WHERE concat = '{0}'".format(piece))
  pieceid = cursor.fetchone()[0]
  cursor.close()
  
  piecetype = ""
  cursor = g.conn.execute("SELECT cat FROM master_pieces WHERE piece_id = '{0}'".format(pieceid))
  piecetype = cursor.fetchone()[0]
  cursor.close()
 
  duration = []
  repnums = []
  rest = []
  distance = []
  cursor = g.conn.execute("SELECT * FROM master_pieces WHERE piece_id = '{0}'".format(pieceid))
  for result in cursor:
    duration.append(result['duration'])
    repnums.append(result['rep_num'])
    rest.append(result['rest'])
    distance.append(result['distance'])
  if piecetype == "time":
    g.conn.execute("INSERT INTO time_piece(duration, piece_id) VALUES('{0}', '{1}')".format(duration[0], id_to_insert))
    g.conn.execute("INSERT INTO piece(piece_id, rest, rep_num, date) VALUES('{0}', '{1}', '{2}', to_date('{3}', 'dd/mm/yyyy'))".format(id_to_insert, rest[0], repnums[0], date))
  else:
     g.conn.execute("INSERT INTO dist_piece(distance, piece_id) VALUES('{0}', '{1}')".format(distance[0], id_to_insert))
     g.conn.execute("INSERT INTO piece(piece_id, rest, rep_num, date) VALUES('{0}', '{1}', '{2}', to_date('{3}', 'dd/mm/yyyy'))".format(id_to_insert, rest[0], repnums[0], date))
  return redirect('/')

@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
