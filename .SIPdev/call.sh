#!/usr/bin/bash

CONTROL='/usr/bin/linphonecsh'

${CONTROL} init
echo 'PHONE initialized'
sleep 1

${CONTROL} generic "soundcard use files"
echo 'PHONE use WAV'
sleep 1

${CONTROL} register --username 398736 --host sip.novofon.com --password mH9V7x8yfm
echo 'PHONE registered'
sleep 1

${CONTROL} dial sip:89021685218@sip.novofon.com
echo 'PHONE dialing'
sleep 15

${CONTROL} generic "play /home/stalk/DEVEL/sirena.wav"
echo 'PHONE playing'
sleep 10

${CONTROL} generic "terminate"
echo 'PHONE hang off'
sleep 1

${CONTROL} exit
echo 'PHONE exit'

###########################################################################