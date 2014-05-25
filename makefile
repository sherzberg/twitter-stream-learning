rebuild:
	fig kill
	fig rm --force
	fig up -d rabbit
	sleep 2
	fig up -d logstash
	sleep 2

test:
	fig run worker nosetests -v
