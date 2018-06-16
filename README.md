# randomstuff
just some random stuff

# Maxinet

## settings

- I created a user to execute Maxinet related commands: SOMEUSER
- pox controller => 172.17.20.11:6633
- server => 172.17.20.11
- worker1 => 172.17.20.11
- worker2 => 172.17.20.11
- config file => ~/.MaxiNet.cfg

## startup
- run controller, server, worker1
```
ssh SOMEUSER@172.17.20.11
SOMEUSER@kumo-nuc01:~$ screen -d -m -S PoxScr python /opt/pox/pox.py forwarding.l2_learning
SOMEUSER@kumo-nuc01:~$ screen -d -m -S MaxiNetFrontend MaxiNetFrontendServer
SOMEUSER@kumo-nuc01:~$ screen -d -m -S MaxiNetWorker sudo MaxiNetWorker
SOMEUSER@kumo-nuc01:~$ screen -ls
There are screens on:
        23707.MaxiNetWorker     (06/16/2018 03:43:10 PM)        (Detached)
        23678.MaxiNetFrontend   (06/16/2018 03:42:55 PM)        (Detached)
        23617.PoxScr    (06/16/2018 03:37:32 PM)        (Detached)
```        
- run worker2
```
SOMEUSER@kumo-nuc03:~$ screen -d -m -S MaxiNetWorker sudo MaxiNetWorker
```

## check if everything is okay
- status
```
SOMEUSER@kumo-nuc01:~$ MaxiNetStatus
MaxiNet Frontend server running at 172.17.20.11
Number of connected workers: 2
--------------------------------
kumo-nuc03              free
kumo-nuc01              free
```

- controller screen
```
SOMEUSER@kumo-nuc01:~$ screen -r PoxScr
POX 0.5.0 (eel) / Copyright 2011-2014 James McCauley, et al.
INFO:core:POX 0.5.0 (eel) is up.
```
- server screen
```
SOMEUSER@kumo-nuc01:~$ screen -r MaxiNetFrontend
Broadcast server running on 0.0.0.0:9091
NS running on 172.17.20.11:9090 (172.17.20.11)
URI = PYRO:Pyro.NameServer@172.17.20.11:9090
Monitoring clusters...
DEBUG:MaxiNet.FrontendServer.server:starting up and connecting to  172.17.20.11:9090
INFO:MaxiNet.FrontendServer.server:startup successful. Waiting for workers to register...
INFO:MaxiNet.FrontendServer.server:new worker signed in: kumo-nuc01 (pyro: MaxiNetWorker_kumo-nuc01)
INFO:MaxiNet.FrontendServer.server:new worker signed in: kumo-nuc03 (pyro: MaxiNetWorker_kumo-nuc03)
```
- worker1 screen
```
SOMEUSER@kumo-nuc01:~$ screen -r MaxiNetWorker
INFO:MaxiNet.WorkerServer.server:starting up and connecting to  172.17.20.11:9090
INFO:MaxiNet.WorkerServer.server:configuring and starting ssh daemon...
INFO:MaxiNet.WorkerServer.server:looking for manager application...
INFO:MaxiNet.WorkerServer.server:signing in...
INFO:MaxiNet.WorkerServer.server:done. Entering requestloop.
```
- worker2 screen
```
SOMEUSER@kumo-nuc03:~$ screen -r MaxiNetWorker
INFO:MaxiNet.WorkerServer.server:starting up and connecting to  172.17.20.11:9090
INFO:MaxiNet.WorkerServer.server:configuring and starting ssh daemon...
INFO:MaxiNet.WorkerServer.server:looking for manager application...
INFO:MaxiNet.WorkerServer.server:signing in...
INFO:MaxiNet.WorkerServer.server:done. Entering requestloop.

```

## run script
- use SOMEUSER to run scripts
```
SOMEUSER@kumo-nuc01:~$ python simplePing.py
```





