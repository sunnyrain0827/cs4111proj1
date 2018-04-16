kdf2118- Kyle Framm
tio2001- Tristan Orlofski


postgreSQL account: same as part 2, under kdf2118


Web app location: http://35.196.194.87:8111/


Implemented parts:
Stores data on rowers, pieces, and teams


Team focus on how to organize by high school for recruiting purposes


Allows to search database by rower, piece, or date to show split progression over time for teams or individuals


Allowed to see the calculated rank of each rower for each piece to see standing relative to teammates


Allows easy access to information on each rower such as major, high school team, whether they were recruited or not, and whether their junior team was a club or a high school


Allowed to search rower by high school team rowed for


Used historical data and allowed access to it to analyze data


Allowed adding pieces to database from full set of standardized Erg pieces among Columbia Rowing


Allowed adding times for any of the rowers in the database, corresponding to any piece- note that adding rowers is not allowed as this was not a proposed feature. 


Allowed finding academic data on rowers, in addition to sorting the data by school


Not implemented parts, in accordance with feedback:
Excel sheet importation of data (see above for individual addition replacement option of pieces)


Making a “practice schedule” was deemed impractical because major selection does not imply class schedule, so we simply made it easy to access majors of rowers 


We did not need to use world record data because it did not fit into our data presentation or analysis, it is an irrelevant benchmark and there was more than enough data to populate our presentation. 


Most interesting pages:
The ability to see each piece winner, as well as the ability to see each piece for a specific rower involves complex database queries. It joins our timed and distance pieces onto the generalized piece set, and then links each piece with a rower to see the speed. Because the time and distance pieces are not union compatible, we created a descriptive varchar to replace the interval or integer value, allowing for the pieces to be union compatible. 
We then calculated the total time from the distance and average split for distance pieces, and the total distance from the time and average split for the timed pieces to add them to the database as to not lose data on presentation. 
We can then select the data from a simple select query and present it in a table view on our website. 


The ability to add pieces to the database is also interesting, as we had to construct the piece_id key ourselves. Because some pieces were missing from the historical database, we had to use generated piece_ids, so when adding a new piece from the database, we query the database to find the highest piece_id, and then insert the new tuple with an incremented piece_id. Then, our error handling method selected 


As a stylistic touch, we decided to keep the Another file, as well creating 90’s-esque web design.# cs4111proj1
Project 1 Web Front End Option

Note- the website is sometimes slow in screen mode, when multiple people are accessing it. This is not due to our code running slowly

Some inspiration from internet tutorials and help from Jerome Kafrouni
