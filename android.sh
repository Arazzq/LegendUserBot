MESAJ="LegendUserBot Otomatik Deploy Kuruluma Hoş Geldiniz"
MESAJ+="\nTelegram: @legendot"
pkg update -y
clear
echo -e $MESAJ
echo "Python Yüklənir"
pkg install python -y
clear
echo -e $MESAJ
echo "Git Yüklənir"
pkg install git -y
clear
echo -e $MESAJ
echo "TeleThon Yüklənir"
pip install telethon
echo "Repo klonlanır..."
git clone https://github.com/Arazzq/installler
clear
echo -e $MESAJ
cd Installer
clear
echo "Bəzi alt yapi dosyaları Yüklənir"
echo -e $MESAJ
pip install wheel
pip install -r requirements.txt
python -m legend_installer
