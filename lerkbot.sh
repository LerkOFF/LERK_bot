#!/usr/bin/bash

cd /opt/LERK_bot
service lerkbot stop
git pull
service lerkbot start
