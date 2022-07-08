cp vars.py vars.bak
git fetch --all
git reset --hard origin/master
cp -f vars.bak vars.py