#  Final Project - Stats Web App

### Team:
##### Douglas Rizio 

##### Michael Rock

### Installation
The app can be cloned from the git repository and started with a simple docker-compose up command.

### Description
The app will utilize sgin-in/ sign-up functions as well as perform some arithmetic and stats functions while charting the output
using the Chartist.js, and Flask libraries. Our app also utilizes Docker, Python, and a database. 

### Usage 

#### Log-in
Upon first loading our app, the user is greeted with the log-in/registration screen. 
![login](screenshots/login.PNG) 

If this is the first time using our app the user will need to follow the prompts to register. 

#### Calculation Screen
After signing up or signing in the user is greeted by the calculation screen:  

![calc_screen](screenshots/calc_screen.PNG) 

The left column displays the number entry and database table of all entries. The calculations can be performed on any two numbers.
For operations that require only one number (square, square root) please enter a zero in the second box. 

The right column displays the totals along with a trend line of all entries. Clicking on the id number of an equation will bring the user to the individual calculation scrren. The user then has an option to delete equation from the database. 
![view_delete](screenshots/view_delete.PNG) 

#### Stats Page
At the top of the page you will find a link to the stats page. 
![stats page](screenshots/stats_page.PNG)

The stats page follows the same layout ast the calculation screen. Including viewing individual calculations and deletion procedures. However, more data is required for the functions to run. In order to use the stats functions six numbers **MUST** be entered. The stats screen tracks the individual totals of each function. 

 
#### Postman
Data can actually be read and written to our app using API's and json. To use post man only the numbers and operation for the calculations or statistics need to entered. 
![postman_calc](screenshots/postman_calc.PNG)

![postman_stats](screenshots/postman_stats.PNG)   

Deletions can also be completed by supplying the id number as part of the request. 

![postman_delete](screenshots/postman_delete.PNG)


 
 


