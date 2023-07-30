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
CMD='/usr/bin/linphonecsh'

${CMD} init
##### echo 'PHONE initialized'
sleep 1

${CMD} generic "soundcard use files"
##### echo 'PHONE use WAV'
sleep 1

${CMD} register --username ${LOGIN} --host ${SERVER} --password ${PASSWORD}
##### echo 'PHONE registered'
sleep 1

${CMD} dial sip:${PHONE}@${SERVER}
##### echo 'PHONE dialing'
sleep 15

${CMD} generic "play ${SOUND}"
##### echo 'PHONE playing'
sleep 10

${CMD} generic "terminate"
##### echo 'PHONE hang off'
sleep 1

${CMD} exit
##### echo 'PHONE exit'

###########################################################################