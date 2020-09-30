(php -S 0.0.0.0:80 1>/dev/null 2>/dev/null &)
JScanner -u http://localhost/example.js  -d yahoo.com -o done1.txt
echo "http://localhost/example.js" | JScanner --- -d yahoo.com -o done2.txt
if [[ "`wc -l done1.txt`" == "`wc -l done2.txt`" ]]; then
	echo "Successful test";
fi
