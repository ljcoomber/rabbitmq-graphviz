Script to display RabbitMQ topology using graphviz, heavily inspired by the [RabbitMQ Getting Started tutorial](http://www.rabbitmq.com/getstarted.html).

To generate the samples (currently only one):
```
$ make setup
$ make samples
```

To run (assuming you have run `make setup`):
```
$ . env/bin/activate
$ python rabbitmq_graphviz.py -d [DEFINITIONS_FILE] -o [DOT_FILE]
```

Limitations:
 - there is currently no distinction between vhosts
 - cannot show consumers and publishers as per the RabbitMQ tutorial (because they are not encoded anywhere in the bindings)

Sample output:

![Sample Output](https://raw.github.com/ljcoomber/rabbitmq-graphviz/master/samples/tutorial.png "Sample Output")
