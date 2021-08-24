
THIS_DIR=`dirname $0`


ls -1F $1 | grep "/$" | bash $THIS_DIR/listmenu.sh "Application" 20 60 13

