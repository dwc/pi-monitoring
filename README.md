pi-monitoring
=============

Push metrics to Xively.

Example
-------

    DEBUG=1 python bin/push_temperature.py --feed 123456789 --key $YOUR_XIVELY_KEY --file /sys/bus/w1/devices/28-000004a7a617/w1_slave
