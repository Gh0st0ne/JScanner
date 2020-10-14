# Version 3.1
* Picture added and other binary changes

# Version 3.0
* Type hinted some functions
* Repetition of same function decreased
* Output format is changed and now sorted along with horizontal lines
* Hidden input parameters discovery support ( You can argue using burp displays it, but it doesnt highlight it, displays same as normal)
* Binary file is regenerated after many versions
* Other minor changes, improvement in speed & efficieny

# Version 2.9
* Custom regex implemented in function!
* Regex for s3 amazon was improved [a-zA-Z] -> [a-zA-Z0-9]

# Version 2.8
* Web services and endpoints differentiated
* Compiled dynamically linked binary now available! 
* Better parsing of inline tags
* Other small variables changes

# Version 2.7
* Exline scripts parsing and printing

# Version 2.6
* Shannon entropy rebalanced
* New functions in JSExtract with extracting as much as necessary data. eg "endpoint" or 'endpoint' will be shown as endpoint.
* Also, single_path_regex is added

# Version 2.5
* Path regex improved and new test case
* Test case detection further improved

# Version 2.4
* Traceback added for error debuggging
* Path regex added and to be implemented
* New argument --enable-entropy

# Version 2.3
* New class and file. Improved code structure.
* Data repetition is reduced more
* Other fixes and improvements

# Version 2.2
* Improved look and UI
* returncomment_fromhtml now return set instead of list reducing repetition of data!
* Shannon entropy value raised to 3.6

# Version 2.1
* Comments parsing added from html

# Version 2.0
* Reverted back to original requests due to [Faster_than_requests error](https://github.com/juancarlospaco/faster-than-requests/issues/93) but again changed to faster_than_requests
* Entirely changed JScanner.py with new class called Engine
* Fixed bugs and stability and LOC is severely reduced. Processing speed increased!
* More regexes are in process so more detection. Also regexes are case insensitive now!
* Code is more cleaner and several variables renaming
* Colorful output avialable now
* Also, duplicate issue is now fixed!

