if pidof $(basename $0) > /dev/null; then
  for p in $(pidof $(basename $0)); do
    if [ $p -ne $$ ]; then
      echo "Script $0 is already running: exiting"
      exit
    fi
  done
fi

./pinti.py -u <username> -p <password> -s <secret key> >> log/pinti.log
