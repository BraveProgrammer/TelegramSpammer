echo "\e[32m  ______     __                                         "
echo " /_  __/__  / /__  ____ __________ _____ ___            "
echo "  / / / _ \/ / _ \/ __ \`/ ___/ __ \`/ __ \`__ \           "
echo " / / /  __/ /  __/ /_/ / /  / /_/ / / / / / /           "
echo "/_/  \___/_/\___/\__, /_/   \__,_/_/ /_/ /_/            "
echo "        / ___/__/____/__ _____ ___  ____ ___  ___  _____"
echo "        \__ \/ __ \/ __ \`/ __ \`__ \/ __ \`__ \/ _ \/ ___/"
echo "       ___/ / /_/ / /_/ / / / / / / / / / / /  __/ /    "
echo "      /____/ .___/\__,_/_/ /_/ /_/_/ /_/ /_/\___/_/     "
echo "          /_/                                           \n"
echo "\e[46m\e[97m=========== Author: @BraveProgrammer ===========\e[49m"
echo "\e[41m\e[97m      I'm Not Responsible For your Actions      \e[49m\n"
echo "Do you want to update the \e[33mTelegram Spammer\e[39m? \e[32mYes\e[33m/\e[31mNo\e[39m\n"
echo -n "\e[1m\e[4mtlsp\e[0m > "
read yn;

update (){
	mkdir ~/.tlsp_update > /dev/null
	cp config.ini ~/.tlsp_update > /dev/null
	cp *.session ~/.tlsp_update > /dev/null
	cp msg ~/.tlsp_update > /dev/null
	cd ..
	DIR=$(pwd)
	cd ~/.tlsp_update
	git clone https://github.com/BraveProgrammer/TelegramSpammer
	rm -rf $DIR/TelegramSpammer
	mv TelegramSpammer $DIR
	mv config.ini $DIR/TelegramSpammer
	mv *.session $DIR/TelegramSpammer
	mv msg $DIR/TelegramSpammer
	rm -rf ~/.tlsp_update
	echo "\e[32mUpdated Successfully!\e[39m"
}

case $yn in
	[Yy]* ) update; break;;
	* ) exit;;
esac
