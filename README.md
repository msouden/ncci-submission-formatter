# ncci-submission-formatter

A script I made for a company I worked for over 2018-2019 in the work comp industry.

It took data from two sources, compared multiple datapoints to match values, and re-segment, add values, reformat date and timestamps, and generate a whitespace delimited machine readable file, as well as an error log for failures in matches or absent data.

Note: 

- This would not have been possible without a bunch of help from my friend Andrew. He introduced me to python dictionaries in this script.
- This was a quarterly task. While a considerable time-saver, I skipped the bells and whistles. Error log needs work, and adding request for file opening.
- All data in this repo is manufactured sample data- it contains no actual health or claims data.
- This was an internal tool used to process work comp claims data - which is not covered under HIPAA regulation nor does it transmit heath data.
