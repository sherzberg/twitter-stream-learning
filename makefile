rebuild:
	fig kill
	fig rm --force
	fig up -d rabbit
	sleep 5
	fig up -d logstash
	sleep 5
	fig ps

test:
	fig run worker nosetests -v
