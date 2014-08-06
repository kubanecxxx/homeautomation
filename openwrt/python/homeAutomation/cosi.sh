while true;
do
	cp aplications ~/samba/router/homeAutomation/ -r -u
	cp aplications ~/samba/router/homeAutomation/ -r -u
	inotifywait -e modify -r aplications
done

