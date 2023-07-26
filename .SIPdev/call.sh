#!/usr/bin/bash

echousage() {
    echo "Usage: ${0} \$1 \$2 \$3"
    echo '    $1 - SIP-server IP/FQDN'
    echo '    $1 - client login'
    echo '    $1 - client passwd'
    echo ''
    exit 1
}

if [ "${1}" ] ; then
    SERVER="${1}"
    if [ "${2}" ] ; then
        LOGIN="${2}"
        if [ "${3}" ] ; then
            PASSWORD="${3}"
        else
            echousage
        fi
    else
        echousage
    fi
else
    echousage
fi

PHONE='89021685218'
SOUND='/home/ubuntu/SIPdev/sirena.wav'
CONTROL='/usr/bin/linphonecsh'

${CONTROL} init
echo 'PHONE initialized'
sleep 1

${CONTROL} generic "soundcard use files"
echo 'PHONE use WAV'
sleep 1

${CONTROL} register --username ${LOGIN} --host ${SERVER} --password ${PASSWORD}
echo 'PHONE registered'
sleep 1

${CONTROL} dial sip:${PHONE}@${SERVER}
echo 'PHONE dialing'
sleep 15

${CONTROL} generic "play ${SOUND}"
echo 'PHONE playing'
sleep 10

${CONTROL} generic "terminate"
echo 'PHONE hang off'
sleep 1

${CONTROL} exit
echo 'PHONE exit'

###########################################################################