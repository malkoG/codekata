#!/bin/sh

FILEPATH=`realpath $0`
DIRECTORY=$(echo `dirname $FILEPATH`)
INCLDUE_PATH="$DIRECTORY/$1.sh"

case $1 in
	tmux|zsh|fish)
		source $INCLUDE_PATH # ` 쓰지 말 것
		;;
	*)
		echo ">> Import Error"
		echo ""
		echo "You should use commands as follows : "
		echo " * ./init.sh <package> ... "
		echo ""
		echo "And, possible packages are : "
		echo " * zsh "
		echo " * fish "
		echo " * tmux "
		exit
		;;
esac

