while true;
do
	cp codelighter/application ~/samba/router/www/codelighter/ -r -u
	inotifywait -e modify -r codelighter/application
done

