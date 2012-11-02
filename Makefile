.PHONY: clean setup samples 

samples: env
	. env/bin/activate && python rabbitmq_graphviz.py -d samples/tutorial.json -o samples/tutorial.dot
	dot -Tpng samples/tutorial.dot > samples/tutorial.png


setup : env/bin/pystache

env/bin/pystache : env
	. env/bin/activate && pip install pystache
	touch env/bin/pystache

virtualenv.py:
	curl https://raw.github.com/pypa/virtualenv/master/virtualenv.py --output virtualenv.py

env: virtualenv.py
	python virtualenv.py env

clean:
	rm -rf env
