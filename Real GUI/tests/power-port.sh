ip=$1
user=$2
pass=$3
port=$4
state=$5
python3 -c "import ip9258;print(ip9258.Ip9258(\"$ip\", \"$user\", \"$pass\").set($port,$state))"
