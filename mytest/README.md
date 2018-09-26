screen -d -m -S drone_data_forwarder main.py data_forwarder 192.168.56.102:18800
screen -d -m -S phone_data_display main.py display_server 192.168.56.102:18900
screen -d -m -S mininet_server main.py mininet_server 192.168.56.102:19000
