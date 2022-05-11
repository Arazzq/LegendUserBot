# Mia UserBot - Ч ⁪⁬⁮⁮

""" UserBot başlangıç noktası """
import importlib
from importlib import import_module
from sqlite3 import connect
import os
import requests
import sys
from telethon.tl.types import InputMessagesFilterDocument
from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from telethon.tl.functions.channels import GetMessagesRequest
from . import BRAIN_CHECKER, LOGS, bot, PLUGIN_CHANNEL_ID, CMD_HELP, LANGUAGE, LEGEND_VERSION, PATTERNS, ForceVer
from .modules import ALL_MODULES
import userbot.modules.sql_helper.mesaj_sql as MSJ_SQL
import userbot.modules.sql_helper.galeri_sql as GALERI_SQL
from pySmartDL import SmartDL
from telethon.tl import functions

from random import choice
import chromedriver_autoinstaller
from json import loads, JSONDecodeError
import re
import userbot.cmdhelp

ALIVE_MSG = [
    "`Userbotunuz işləyir. Sənə birşey demək istiyirəm.. Səni sevirəç` **{legendsahip}** ❤️",
    "🎆 `Narahat olma! Səni yalnız buraxmaram.` **{legendsahip}**, `LegendUserbot işləyir.`",
    "`⛈️ Əlimdən gələnin ən yaxşısını etməyə hazıram`, **{legendsahip}**",
    "✨ `LegendUserBot sahibinin əmirlərinə hazır...`",
    "`İndi ən müasir userbotun editlədiyi mesajı oxumalısan` **{legendsahip}**.",
    "`Mənə zəng eləmişdin❓ Mən Buradayam Maraqlanma`"
    "`Userbotunuz işləyəli bu qədər olur:` **{worktime}** ❤️",
    "🎆 `Narahat olma! Səninləyəm.` **{legendsahip}**, `userbot işləyir.`",
    "`⛈️ Yeni kimi görünür!`, **{legendsahip}:3**",
    "✨ `Userbot sahibinin əmirlərinə hazır...`",
    "`Huh!` **{legendsahip}** `məni çağırır 🍰 < bu sənin üçündür 🥺..`",
    "{mention} **Legend Sənin Üçün İşləyir✨**",
    "{username}, `LegendUserBot {worktime} zamandır işləyir...`\n——————————————\n**Telethon versiyası :** `{telethon}`\n**Userbot versiyası  :** `{legend}`\n**Python versiyası    :** `{python}`\n**Plugin sayısı :** `{plugin}`\n——————————————\n**Əmrindəyəm dostum... 😇*
DIZCILIK_STR = [
    "Stikeri dızlıyıram...",
    "Oğurladım Getdi Keçmiş Olsun 🤭",
    "Yaşasın dızcılıq...",
    "Bu stikeri öz paketimə dəvət edirəm...",
    "Bunu dızlamam lazımdıda ...",
    "Hooy bu gözəl bir stiker!\nHəmən dızlıyıram..",
    "Stikeri dızlıyıram\nhahaha.",
    "Hooy bura bax. (☉｡☉)!→\nMən bunu dızlayanda...",
    "Güllər qırmızı bənövşələr mavi, bu stiker paketime dızlayaraq havalı olacam...",
    "Stiker həbs edilir...",
    "Canım, dızcı bu stikeri dızlıyır... ",
    "Bu gözəl stiker niyə mənim paketimde də olmasın🤭",
]

AFKSTR = [
    "İndi tələsirəm, daha sonra mesaj atsan olmaz dı? Onsuz yenə gələcəmdə.",
    "Çağırdığınız kişi İndi telefona cavab verə bilmir. Siqnal səsindən sonra öz tərifiniz üzərindən mesajınızı buraxa bilərsiniz. Mesaj haqqı 49 qəpiydir. \n`biiiiiiiiiiiiiiiiiiiiiiiiiiiiib`!",
    "Bir neçə dəqiqəyə gələcəm. Amma, gəlməzsəm...\ndaha çox gözlə.",
    "İndi burada deyiləm, amma ehtimal edirəmki başqa bir yerdəyəm.",
    "Güllər qırmızı\nBənövşələr mavi\nMənə bir mesaj burax\nVə sənə gələcəm.",
    "Bəzən həyatdakı ən yaxşı şeyləri gözləməyə dəyər…\nİndi gələrəm.",
    "İndi gələrəm,\namma geri gəlməzsəm,\ndaha sonra gələrəm.",
    "Hələdə anlamamısan?,\nburada deyiləm.",
    "Salam, uzaq mesajıma xoş gəldiniz, bugün sizi necə görməzdən gələ bilərəm?",
    "7 dəniz və 7 ölkədən uzaqdayam,\n7 su ve 7 qitə,\n7 dağ və 7 təpə,\n7 ovala və 7 kurqan,\n7 hovuz və 7 göl,\n7 bahar və 7 çəmən,\n7 şəhər və 7 məhəllə,\n7 blok və 7 ev...\n\nMesajların belə mənə çata bilməyəcəyi bir yer!",
    "İndi klaviyaturadan uzaqdayam, amma ekranınızda yetərincə yüksək səslə qışqırsanız, sizi eşidə bilərəm.",
    "Bu yöndə gedirəm\n---->",
    "Bu yöndə gedirəm\n<----",
    "Xahiş mesaj buraxın və məni olduğumdan daha özəl hiss etdirin.",
    "Sahibim burada değil, bu yüzden bana yazmayı bırak.",
    "Burada olsaydım,\nSənə harada olduğumu deyərdim.\n\nAmma mən deyiləm,\ngeri gəldiyimdə mənə de...",
    "Uzaqlardayam!\nNə vaxt gələrəm bilmirəm !\nÜmid edirəmki bir neçə dəqiqə sonra!",
    "Sahibim indidə məşğuldur. Adınızı, nömrənizi və adresinizi versəniz ona göndərə bilərəm və beləliklə geri döndüyü zaman.",
    "Çox pisəm, sahibim burada deyil.\nO gələnə qədər mənimlə danışa bilərsiniz.\nSahibim sizə sonra gələr.",
    "Bəhsə girərəm bir mesaj gözləyirdin!",
    "Həyat çok qısa, edəcək çox şey var...\nOnlardan birini edirəm...",
    "İndi burada deyiləm....\nama eləsəm ...\n\nbu babat olmazdı?",
    "Məni xatırladığına sevindim amma indi klaviyatura mənə çox uzaqdır",
    "Bəlkə Yaxşıyam, Bəlkə pisəm, Bilmirsən Amma AFK Olduğumu Görə bilirsən"
]

KICKME_MSG = [
    "Sağol da mən gedirəm👋🏻",
    "Səssizcə tullanıram 🥴",
    "Xəbərin olmadan çıxarsam bir gün mənim qrupta olmadığını biləcəksən.. Onun üçün bu mesajı buraxıram🚪",
    "Mən buranı tərk etməliyəm🤭"
    "7 dəniz və 7 ölkə,\n7 su və 7 qitə,\n7 dağ və 7 təpə,\n7 ovala və 7 kurqan,\n7 hovuz və 7 göl,\n7 bahar və 7 çəmən,\n7 şəhər ve 7 məhəllə,\n7 blok və 7 ev...\n\nQısaca bu qruptan uzaq bir yerə..!",
    "Sağolun mən qaçdım!"
]


UNAPPROVED_MSG = ("`{mention} Sahibim təsdiq edənə qədər bu mesajı alacaqsın👩🏻‍💻!\n\n`"
                  "`✔️ Təsdiqli olmadığın vaxtda hər yazdığın mesaja yanıt olaraq sahibimin yerinə mən mesaj  `"
                  "`atacağam.....\n\n`")

DB = connect("learning-data-root.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM BRAIN1""")
ALL_ROWS = CURSOR.fetchall()


INVALID_PH = '\nHATA: Girilen telefon nömrəsi keçərsiz' \
             '\n  Ipucu: Ölkə kodunu işlədərək nömrəni gir' \
             '\n   Telefon nömrənizi təkrar yoxlayın'

for i in ALL_ROWS:
    BRAIN_CHECKER.append(i[0])
connect("learning-data-root.check").close()
BRAIN_CHECKER = BRAIN_CHECKER[0]

def extractCommands(file):
    FileRead = open(file, 'r').read()
    
    if '/' in file:
        file = file.split('/')[-1]

    Pattern = re.findall(r"@register\(.*pattern=(r|)\"(.*)\".*\)", FileRead)
    Komutlar = []

    if re.search(r'CmdHelp\(.*\)', FileRead):
        pass
    else:
        dosyaAdi = file.replace('.py', '')
        CmdHelp = userbot.cmdhelp.CmdHelp(dosyaAdi, False)

        # Komutları Alıyoruz #
        for Command in Pattern:
            Command = Command[1]
            if Command == '' or len(Command) <= 1:
                continue
            Komut = re.findall("(^.*[a-zA-Z0-9şğüöçı]\w)", Command)
            if (len(Komut) >= 1) and (not Komut[0] == ''):
                Komut = Komut[0]
                if Komut[0] == '^':
                    KomutStr = Komut[1:]
                    if KomutStr[0] == '.':
                        KomutStr = KomutStr[1:]
                    Komutlar.append(KomutStr)
                else:
                    if Command[0] == '^':
                        KomutStr = Command[1:]
                        if KomutStr[0] == '.':
                            KomutStr = KomutStr[1:]
                        else:
                            KomutStr = Command
                        Komutlar.append(KomutStr)

            # MIAPY
            Legendpy = re.search('\"\"\"LEGENDPY(.*)\"\"\"', FileRead, re.DOTALL)
            if not Legendpy == None:
                Legendpy = Legendpy.group(0)
                for Satir in Legendpy.splitlines():
                    if (not '"""' in Satir) and (':' in Satir):
                        Satir = Satir.split(':')
                        Isim = Satir[0]
                        Deger = Satir[1][1:]
                                
                        if Isim == 'INFO':
                            CmdHelp.add_info(Deger)
                        elif Isim == 'WARN':
                            CmdHelp.add_warning(Deger)
                        else:
                            CmdHelp.set_file_info(Isim, Deger)
            for Komut in Komutlar:
                # if re.search('\[(\w*)\]', Komut):
                    # Komut = re.sub('(?<=\[.)[A-Za-z0-9_]*\]', '', Komut).replace('[', '')
                CmdHelp.add_command(Komut, None, 'Bu plugin xaricdən yüklənmişdir. Hər hansı bir açıqlama tanımlanmamışdır.')
            CmdHelp.add()

forceVer = []
DB = connect("force-surum.check")
CURSOR = DB.cursor()
CURSOR.execute("""SELECT * FROM SURUM1""")
ALL_ROWS = CURSOR.fetchall()

for i in ALL_ROWS:
    forceVer = i
connect("force-surum.check").close()
try:
    ForceVer = int(forceVer)
except:
    ForceVer = -1


try:
    bot.start()
    idim = bot.get_me().id
    miabl = requests.get('https://raw.githubusercontent.com/Miauserbot/datas/master/blacklist.json').json()
    if idim in miabl:
        bot.send_message("me", f"`❌ Legend adminləri sizi botdan qadağa etdi! Bot bağlanır...`")
        LOGS.error("Legend qurucuları sizi botdan qadağan etdi! Bot bağlanır...")
        bot.disconnect()
        sys.exit(1)
    # ChromeDriver'ı Ayarlayalım #
    try:
        chromedriver_autoinstaller.install()
    except:
        pass
    
    # Galeri için değerler
    GALERI = {}

    # PLUGIN MESAJLARI AYARLIYORUZ
    PLUGIN_MESAJLAR = {}
    ORJ_PLUGIN_MESAJLAR = {"alive": f"{str(choice(ALIVE_MSG))}", "afk": f"`{str(choice(AFKSTR))}`", "kickme": f"`{str(choice(KICKME_MSG))}`", "pm": str(UNAPPROVED_MSG), "dızcı": str(choice(DIZCILIK_STR)), "ban": "🌀 {mention}`, Banlandı!!`", "mute": "🌀 {mention}`, sessize alındı!`", "approve": "`Merhaba` {mention}`, artık bana mesaj gönderebilirsin!`", "disapprove": "{mention}`, artık bana mesaj gönderemezsin!`", "block": "{mention}`, bunu bana mecbur bıraktın! Seni engelledim!`"}


    PLUGIN_MESAJLAR_TURLER = ["alive", "afk", "kickme", "pm", "dızcı", "ban", "mute", "approve", "disapprove", "block"]
    for mesaj in PLUGIN_MESAJLAR_TURLER:
        dmsj = MSJ_SQL.getir_mesaj(mesaj)
        if dmsj == False:
            PLUGIN_MESAJLAR[mesaj] = ORJ_PLUGIN_MESAJLAR[mesaj]
        else:
            if dmsj.startswith("MEDYA_"):
                medya = int(dmsj.split("MEDYA_")[1])
                medya = bot.get_messages(PLUGIN_CHANNEL_ID, ids=medya)

                PLUGIN_MESAJLAR[mesaj] = medya
            else:
                PLUGIN_MESAJLAR[mesaj] = dmsj
    if not PLUGIN_CHANNEL_ID == None:
        LOGS.info("🔄 Pluginlər Yüklənir..")
        try:
            KanalId = bot.get_entity(PLUGIN_CHANNEL_ID)
        except:
            KanalId = "me"

        for plugin in bot.iter_messages(KanalId, filter=InputMessagesFilterDocument):
            if plugin.file.name and (len(plugin.file.name.split('.')) > 1) \
                and plugin.file.name.split('.')[-1] == 'py':
                Split = plugin.file.name.split('.')

                if not os.path.exists("./userbot/modules/" + plugin.file.name):
                    dosya = bot.download_media(plugin, "./userbot/modules/")
                else:
                    LOGS.info("Bu Plugin Onsuzda Yüklüdür " + plugin.file.name)
                    extractCommands('./userbot/modules/' + plugin.file.name)
                    dosya = plugin.file.name
                    continue 
                
                try:
                    spec = importlib.util.spec_from_file_location("userbot.modules." + Split[0], dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)
                except Exception as e:
                    LOGS.info(f"`[×] Yükləmə Uğursuz! Plugin xətalı!!\n\nHata: {e}`")

                    try:
                        plugin.delete()
                    except:
                        pass

                    if os.path.exists("./userbot/modules/" + plugin.file.name):
                        os.remove("./userbot/modules/" + plugin.file.name)
                    continue
                extractCommands('./userbot/modules/' + plugin.file.name)
    else:
        bot.send_message("me", f"`Xahiş pluginlərin qalıcı olması üçün PLUGIN_CHANNEL_ID'i ayarlayın.`")
except PhoneNumberInvalidError:
    print(INVALID_PH)
    sys.exit(1)

async def FotoDegistir (foto):
    FOTOURL = GALERI_SQL.TUM_GALERI[foto].foto
    r = requests.get(FOTOURL)

    with open(str(foto) + ".jpg", 'wb') as f:
        f.write(r.content)    
    file = await bot.upload_file(str(foto) + ".jpg")
    try:
        await bot(functions.photos.UploadProfilePhotoRequest(
            file
        ))
        return True
    except:
        return False

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

os.system("clear")

LOGS.info("+===========================================================+")
LOGS.info("|                     ✨Legend Userbot✨                       |")
LOGS.info("+==============+==============+==============+==============+")
LOGS.info("|                                                            |")
LOGS.info("Botunuz işləyir! Hər hansı bir söhbətə .alive yazaraq Test edin."
          " Yardıma Ehtiyacınız varsa, Kömək qrupumuza gəlin t.me/suplegend")
LOGS.info(f"Bot versiyanız: Legend {LEGEND_VERSION}")

"""
if len(argv) not in (1, 3, 4):
    bot.disconnect()
else:
"""
bot.run_until_disconnected()
