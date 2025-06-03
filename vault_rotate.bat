@echo off
cd /d "C:\Users\Administrator\Desktop\CALIUSODEBUG\caliuso-memory-core"

nssm start caliuso-memory-api
nssm start caliuso-autosync
nssm start caliuso-immortal-watchdog

echo IMMORTAL BOOTUP COMPLETE
pause