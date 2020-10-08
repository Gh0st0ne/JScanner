(fuser -k 80/tcp 1>/dev/null 2>/dev/null; php -S 0.0.0.0:80 1>/dev/null 2>/dev/null &)
JScanner -u http://localhost/example.js -o output/done1.txt
JScanner -u http://localhost/example.html -o output/done2.txt
