#!/bin/bash
set -e

iris session IRIS <<'EOF'

Write "STARTING IRIS CONFIGURATION...",!

Write "Changing to SYS namespace for additional system permission...",!
Set $namespace="%SYS"

Write "Disabling password expiration...",!
Do ##class(Security.Users).UnExpireUserPasswords("*")

Write "Enabling analytics...",!
do EnableDeepSee^%SYS.cspServer("/csp/user/")

Write "Enabling structured logging...",!
do ^LOGDMN
4
INFO
irislogd -f /dur/log/MLpipelineLogs.log
JSON
1
-Audit.*,-Utility.*,-Log.*,-Generic.*,-System.*,+Utility.*
SYS.LogDmm:Enable
1
7
q

Write "Installing IPM...",!
s version="latest" s r=##class(%Net.HttpRequest).%New(),r.Server="pm.community.intersystems.com",r.SSLConfiguration="ISC.FeatureTracker.SSL.Config" d r.Get("/packages/zpm/"_version_"/installer"),$system.OBJ.LoadStream(r.HttpResponse.Data,"c")

Write "Installing IPM packages...",!
zpm
repo -r -n registry -url https://pm.community.intersystems.com/ -user "" -pass ""
# install csvgenpy 1.2.5 # This is an example to show how to install additional packages if needed, currently not used in the pipeline. WARNING: Be aware thet packages installed via IPM might overwrite existing python dependencies in IRIS
quit

Write "Changing to USER namespace for project configuration...",!
Set $namespace="USER"

Write "Importing ObjectScript packages...",!
Do $system.OBJ.Import("/usr/irissys/mgr/MLpipeline", "ck")


Write "IRIS CONFIGURATION COMPLETED.",!
halt
EOF
