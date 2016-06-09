# BeePy

## Install

```
python setup.py install
```

## Tools

Dump all status values from SensorBee server:

```
bin/sensorbee_status
```

```js
{
    "topologies": {
        "jubatus_iris": {
            "streams": {
                "labeled_iris": {
                    "node_type": "box",
                    "status": {
                        "input_stats": {
                            "num_errors": 0,
                            "inputs": {},
                            "num_received_total": 150
                        },
                        "state": "stopped",
                        "output_stats": {
                            "num_dropped": 0,
                            "num_sent_total": 150,
                            "outputs": {}
                        },
                        "behaviors": {
                            "stop_on_outbound_disconnect": false,
                            "graceful_stop": false,
                            "remove_on_stop": false,
                            "stop_on_inbound_disconnect": true
                        }
                    },
                    "state": "stopped",
                    "meta": {},
                    "name": "labeled_iris"
                }
            },
            "sinks": {
                "iris_classifier_sink": {
                    "node_type": "sink",
                    "status": {
                        "input_stats": {
                            "num_errors": 0,
                            "inputs": {},
                            "num_received_total": 150
                        },
                        "state": "running",
                        "behaviors": {
                            "graceful_stop": false,
                            "stop_on_disconnect": false,
                            "remove_on_stop": false
                        }
                    },
                    "state": "running",
                    "meta": {},
                    "name": "iris_classifier_sink"
                },
                "classification_result": {
                    "node_type": "sink",
                    "status": {
                        "input_stats": {
                            "num_errors": 0,
                            "inputs": {},
                            "num_received_total": 150
                        },
                        "state": "running",
                        "behaviors": {
                            "graceful_stop": false,
                            "stop_on_disconnect": false,
                            "remove_on_stop": false
                        }
                    },
                    "state": "running",
                    "meta": {},
                    "name": "classification_result"
                }
            },
            "sources": {
                "iris": {
                    "node_type": "source",
                    "status": {
                        "source": {
                            "waiting_for_rewind": false,
                            "rewindable": false
                        },
                        "output_stats": {
                            "num_dropped": 0,
                            "num_sent_total": 150,
                            "outputs": {}
                        },
                        "state": "stopped",
                        "behaviors": {
                            "remove_on_stop": false,
                            "stop_on_disconnect": false
                        }
                    },
                    "state": "stopped",
                    "meta": {},
                    "name": "iris"
                },
                "iris_analysis": {
                    "node_type": "source",
                    "status": {
                        "source": {
                            "waiting_for_rewind": false,
                            "rewindable": false
                        },
                        "output_stats": {
                            "num_dropped": 0,
                            "num_sent_total": 150,
                            "outputs": {}
                        },
                        "state": "stopped",
                        "behaviors": {
                            "remove_on_stop": false,
                            "stop_on_disconnect": false
                        }
                    },
                    "state": "stopped",
                    "meta": {},
                    "name": "iris_analysis"
                }
            }
        }
    },
    "runtime_status": {
        "user": "kenichi",
        "num_cgo_call": 101,
        "pid": 19789,
        "num_goroutine": 8,
        "hostname": "localhost",
        "gomaxprocs": 4,
        "goversion": "go1.6.2",
        "working_directory": "/home/kenichi/Development/sensorbee-iris-jubatus",
        "goroot": "/home/kenichi/local/go",
        "num_cpu": 4
    }
}
```
