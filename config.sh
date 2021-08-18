#!/usr/bin/env bash

CONFIG_PATH=./tmp

menuconfig() {
	if [ -f ./build/global_config.config ]; then cp -f ./build/global_config.config ./.config; fi
	python3 -u ./scripts/kconfiglib/menuconfig.py ./build/configList
	if [ -f ./.config ]; then cp -f ./.config ./build/global_config.config; fi
}

choice() {
	mkdir -p $CONFIG_PATH
	INPUT_CONFIG=`bash ./scripts/get_config.sh`
    echo INPUT_CONFIG=$INPUT_CONFIG
	echo CONFIG_PATH=$CONFIG_PATH
	python3 -u ./scripts/kconfiglib/conf2h.py ./build/config/$INPUT_CONFIG $CONFIG_PATH/global_config.h
	echo "global_config.h is generated !!"
}

config() {
	if [ ! -f ./build/global_config.config ]; then
		CONFIG=`bash ./scripts/get_config.sh`
		cp ./build/config/$CONFIG ./build/global_config.config
		fi
	mkdir -p $CONFIG_PATH
	echo INPUT_CONFIG=../global_config.config
	echo CONFIG_PATH=$CONFIG_PATH
	python3 -u ./scripts/kconfiglib/conf2h.py ./build/global_config.config $CONFIG_PATH/global_config.h
	echo "global_config.h is generated !!"
}

if [ "$1" = "menuconfig" ]; then
    menuconfig
elif [ "$1" = "choice" ]; then
    choice
else
    config
fi


