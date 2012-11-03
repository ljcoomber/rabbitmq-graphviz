.PHONY: samples 

samples:
	python rabbitmq_graphviz.py -d samples/tutorial.json -o samples/tutorial.dot -p
	dot -Tpng samples/tutorial.dot > samples/tutorial.png
