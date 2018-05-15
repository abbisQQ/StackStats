# StackStats# Stackstats #

### Python Software Developer Assignment ###

* Stackstats is a python application that uses the StackExchange API to retrieve data and accomplish the following *
* Retrieves the StackOverFlow answer data for a given date/time range.*
* Retrieves the comment data for a given set of answers.*
* Calculates the total number of accepted answers, the average score for all the accepter answers, the average count per question, 
	the comment count for each of the 10 answers with the highest score.
* Returns them in a JSON or tabular format.*


### Installation ###
* Open a Command Prompt *
* Navigate to encode-python-assignment folder location *
* Type the following command in your terminal python setup.py install*
	
	
### How to run the application ###
* Run it using " stats --since "YYYY-MM-DD HH-MM-SS" --until "YYYY-MM-DD HH-MM-SS --output-format json/tabular" *
* Example: stats --since "2016-06-02 10:00:00" --until "2016-06-07 11:00:00" --output-format json *
