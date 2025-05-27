#/bin/bash



ip=$1
user=$2
pass=$3
port=$4
fpga=$5
dir=/media/disk/ci

pushd tests
old="$(./power-port.sh $ip $user $pass $port 1)"
./power-port.sh $ip $user $pass $port 0
sleep 2
./power-port.sh $ip $user $pass $port 1
./wait-for-it.sh $fpga:22 -t 60
if [ $? -ne 0 ]
then
   exit 5
fi
sleep 5
pushd 
./deploy.sh $fpga $dir
pushd tests
if [ $? -ne 0 ]
then
   exit 5
fi

pytest  --fpga=$fpga --dir=$dir --timeout=1500 -v 
err=$?
./power-port.sh $ip $user $pass $port $old
popd
exit $err
