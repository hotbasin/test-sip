#!/usr/bin/bash

echousage() {
    echo "Usage: ${0} \$1 \$2 \$3 \$4"
    echo '    $1 - SIP-server IP/FQDN'
    echo '    $2 - SIP-client login'
    echo '    $3 - SIP-client password'
    echo '    $4 - Telephone number'
    echo ''
    exit 1
}

if [ "${1}" ] ; then
    SERVER="${1}"
    if [ "${2}" ] ; then
        LOGIN="${2}"
        if [ "${3}" ] ; then
            PASSWORD="${3}"
            if [ "${4}" ] ; then
                PHONE="${4}"
            else
                echousage
            fi
        else
            echousage
        fi
    else
        echousage
    fi
else
    echousage
fi

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