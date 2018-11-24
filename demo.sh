if [[ ! -d "demo/data/" ]]; then
	mkdir demo/data;
fi

if [[ "$1" == "clean" ]]; then
	csv_num=$(ls -l demo/data/*.csv 2>/dev/null | wc -l);
	if [[ $csv_num -gt 0 ]]; then
		rm demo/data/*.csv;
	fi
fi

if [[ "$1" == "generate" ]]; then
	cd demo;
	python3 prepare_data.py;
fi

if [[ "$1" == "server" ]]; then
	cd demo;
	python3 server.py;
fi

if [[ "$1" == "start" ]]; then
	csv_num=$(ls -l demo/data/*.csv 2>/dev/null | wc -l);
	if [[ $csv_num -gt 0 ]]; then
		rm demo/data/*.csv;
	fi
	cd demo;
	python3 prepare_data.py;
	python3 server.py;
fi
