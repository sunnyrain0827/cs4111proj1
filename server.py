#!/usr/bin/env python2.7

#Tristan Orlofski, Kyle Fram
#tio2001, kdf2118
#COMS 4111 Database Project 1 Part 3 

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
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

  #index.html has a lot of drop-down menus that require data from the database
  #to be displayed, so these select queries allow us to show that information
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

#page for error handling on incorrect input for the INSERT queries
@app.route('/error', methods = ['GET'])
def error():
  return render_template("error.html")

#we liked this one, so he stayed :)
@app.route('/another')
def another():
  return render_template("another.html")

#function to display pieces by date
@app.route('/piece', methods = ['POST'])
def piece():
  
  #grab the date from the form in index.html
  date = request.form['dates']

  #need to check if user selected all dates option
  if date == "all":
    cursor2 = g.conn.execute("SELECT * FROM all_pieces ORDER BY piece_id")
  else:
    #we bounced around between using the .format and the %s option for
    #inserting the information from the form into the queries, but decided
    #on .format because we were having trouble with data types other than 
    #strings. This stays true throughout the entire file
    cursor2 = g.conn.execute("SELECT * FROM all_pieces WHERE date = '{0}' ORDER BY piece_id".format(date))
  
  #easiet way to grab the information is to encode each attribute
  #in its own array
  pids3 = []
  dates = []
  repnums = []
  rest = []
  lengths = []
  
  #populate arrays based on string matching with the cursor
  for result in cursor2:
    pids3.append(result['piece_id'])
    dates.append(result['date'])
    repnums.append(result['rep_num'])
    rest.append(result['rest'])
    lengths.append(result['length'])
  cursor2.close()
  #create dict to send to the HTML template, modeled after the example provided
  context = dict(data = (pids3, dates, lengths, repnums, rest))
  return render_template("piece.html", **context)

#function for pieces by piece ID. All of the select functions follow a similar
#pattern, and thus we will not be commenting each individually
@app.route('/piece_ids', methods = ['POST'])
def piece_ids():
  pid = request.form['pids']
  if pid == "all":
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

#function for team academic info by school
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

#function for piece winners by piece date
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

#function for piece and other information by rower, using a custom view
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


#function for general academic rower info
@app.route('/rowerinfo', methods = ['POST'])
def rowerinfo():
  rowers = request.form['rowers']
  if rowers == "all":
    cursor= g.conn.execute("SELECT * FROM rower_info ORDER BY row_name")
  else:
    cursor = g.conn.execute("SELECT * FROM rower_info WHERE row_name = '{0}'".format(rowers))
 
  #this is where the array system got cumbersome, but we could not 
  #implement a better, more reliable way, given that both of our
  #knowledge of python data structures was limited (we both come from a 
  #mainly java or C background). However, we know arrays well
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

#function for selecting rower info by high school team
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

#function for adding a piece to the piece entity of the database
@app.route('/addpiece', methods = ['POST'])
def addpiece():
  
  #get date info from 3 tickers, put together into our chosen format
  datedays = request.form['datedays']
  datemonths = request.form['datemonths']
  dateyears = request.form['dateyears']     
  date = datedays + "\\" + datemonths + "\\" + dateyears

  #minimum number of characters our date format can be is 8, so if
  #our date is fewer characters than that, we need to reject input
  if len(date) < 8:
    return render_template("error.html")

  #we need piece_id to add to pieces, we need a piece ID which is unique
  #in order to generate this, we get the maximum current piece ID and iterate
  piece = request.form['pieces']
  cursor = g.conn.execute("SELECT max(p.piece_id) FROM piece p")
  id_to_insert = ((cursor.fetchone()[0]) + 1)
  cursor.close()  

  #this query allows us to get the piece_ID associated with the piece name
  #picked by the user, so that we can piece type 
  cursor = g.conn.execute("SELECT DISTINCT piece_id FROM master_pieces WHERE concat = '{0}'".format(piece))
  pieceid = cursor.fetchone()[0]
  cursor.close()
  
  #getting piece_type then allows us to know which of the ISA piece types to
  #insert into
  piecetype = ""
  cursor = g.conn.execute("SELECT cat FROM master_pieces WHERE piece_id = '{0}'".format(pieceid))
  piecetype = cursor.fetchone()[0]
  cursor.close()
 
  #filling out the information to insert, in much the same way our select
  #functions worked
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
  
  #we had trouble inputing rest in pieces where there was no rest, and thus
  #this if statement and variable allows us to set rest to 0 rather than 
  #encounter the error
  resty = rest[0]
  if repnums[0] == 1:
    resty = 0 

  #need to insert into the correct piece type, and this if statement gives us
  #the information we need
  if piecetype == "time":
    #insert into piece first, then the ISA type, so we do not violate 
    #any of our constraints
    g.conn.execute("INSERT INTO piece(piece_id, rest, rep_num, date) VALUES('{0}', '{1}', '{2}', to_date('{3}', 'dd/mm/yyyy'))".format(id_to_insert, resty, repnums[0], date))
    g.conn.execute("INSERT INTO time_piece(duration, piece_id) VALUES('{0}', '{1}')".format(duration[0],
 id_to_insert))
  else:
     g.conn.execute("INSERT INTO piece(piece_id, rest, rep_num, date) VALUES('{0}', '{1}', '{2}', to_date('{3}', 'dd/mm/yyyy'))".format(id_to_insert, resty, repnums[0], date))
     g.conn.execute("INSERT INTO dist_piece(distance, piece_id) VALUES('{0}', '{1}')".format(distance[0], id_to_insert))
  #on success, returns user to index.html
  return redirect('/')

#function for adding a workout
@app.route("/addworkout", methods=['POST'])
def addworkout():
  #get split data in the same way we got date data in the previous function
  #we assume in our database that split won't be above 3:59, as this
  #is a completely unrealistic and ridiculous score for a collegiate rower
  splitmins = request.form['splitmins']
  splitsecs = request.form['splitsecs']
  pid = request.form['pid']
  rower = request.form['rowers']
  split = ""  
  uni = ""  

  #making sure our splits were entered correctly
  if (len(splitmins) < 1) or (len(splitsecs) < 1):
    return render_template("error.html")

  #need to format split in the proper way, as an interval
  if splitsecs < 10:
     split = "00:0" + splitmins + ":" + "0" + splitsecs
  else:
    split = "00:0" + splitmins + ":" + splitsecs

  #need to get uni, as it is the key. We did not have users select by it as 
  #it is much easier to select by name
  cursor = g.conn.execute("SELECT uni FROM rower WHERE row_name = '{0}'".format(rower))
  uni = cursor.fetchone()[0]
  cursor.close()
  
  #the if statement here allows us to both reject a completely unfilled input
  #and reject inputs that would violate the uniqueness of our keys  
  cursor = g.conn.execute("SELECT * FROM rowed WHERE piece_id = '{0}' AND uni = '{1}'".format(pid, uni))
  if cursor.rowcount != 0:
    return render_template("error.html")
  else:
    g.conn.execute("INSERT INTO rowed(split_speed, piece_id, uni) VALUES('{0}', '{1}', '{2}')".format(split, pid, uni))
  cursor.close()
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
