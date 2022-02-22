This is the solution for the Gambit Challenge - TUF-2000M sensor
================================================================
Measurements are read from the URL provided and converted to 
a format humans can read. The converted data are displayed in 
two different ways. With the use of the terminal (command prompt) and
through a tkinter python interface.

The solution also creates an XML file (data.xml) that is then used by an
html file to dislplay the data in yet another way using an
internet browser.


Running the application
----------------------------------------------------------------
To run the solution: 
- Install: a python version (v.3.10)
- Install: python module "requests". Use the command " pip install requests "
	   in the terminal
- Copy the files from github in a folder
- Run the Gambit_challenge_Dimitrios_Gkizis.py file


Displaying data on the browser
----------------------------------------------------------------
To display the data in the browser, after executing 
Gambit_challenge_Dimitrios_Gkizis.py so that the XML file is 
created:
- Navigate in the terminal to the folder containing the files
- Run:	 " python -m http.server " in the terminal
  That way you run a local server in order to use the httpXMLHttpRequest()
javascript in the index.html. (Python module http.server)
- Find your IP address (e.g. " ipconfig " in the terminal)
- Type in the internet browser: " http://xxx.xxx.xxx.xxx:8000/ "