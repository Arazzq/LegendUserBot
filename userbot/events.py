# Mia UserBot - Ч ⁪⁬⁮⁮

""" Olayları yönetmek için UserBot modülü.
 UserBot'un ana bileşenlerinden biri. """

import sys
from asyncio import create_subprocess_shell as asyncsubshell
from asyncio import subprocess as asyncsub
from os import remove
from time import gmtime, strftime
from traceback import format_exc
from telethon.events import NewMessage as NW, MessageEdited as ME, StopPropagation as SP
from telethon.errors.rpcerrorlist import MessageIdInvalidError
from userbot import bot, SUDO_ID, ASISTAN, SEVGILI, BOTLOG_CHATID, LOGSPAMMER, PATTERNS, LEGEND_VERSION, ForceVer


def register(**args):
    """ Yeni bir etkinlik kaydedin. """
    pattern = args.get('pattern', None)
    sudo = args.get('sudo', False)
    sevgili = args.get('sevgili', False)
    replyneeded = args.get('replyneeded',False)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)
    notifyoff = args.get('notifyoff', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']

    if 'replyneeded' in args:
        del args['replyneeded']

    if 'notifyoff' in args:
        del args['notifyoff']

    if "incoming" not in args:
        args['outgoing'] = True


    if 'sudo' in args:
        del args['sudo']
        if SUDO_ID:
            args['outgoing'] = False
            args['incoming'] = True
            args["from_users"] = SUDO_ID

    if 'sevgili' in args:
        del args['sevgili']
        if SEVGILI:
            args['outgoing'] = False
            args['incoming'] = True
            args["from_users"] = SEVGILI

    if 'asistan' in args:
        del args['asistan']
        args['outgoing'] = False
        args['incoming'] = True
        args["from_users"] = ASISTAN


    def decorator(func):
        async def wrapper(check):
            LegendVer = int(LEGEND_VERSION.split(".")[1])
            if ForceVer > LegendVer:
                await check.edit(f"`🌈 Botu təcili güncəlləmən lazımdır! Bu versiya artıq işlədilə bilmir..`\n\n__🥺 Xətanı həll etmək üçün__ `.update now` __yazmalısan!__")
                return

            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                if not notifyoff:
                    try:
                        await check.edit("`⛔ Bunun bir qrup olduğuna inanmıram. Bu plugini bir qrupta cəhd et! `")
                    except:
                        await check.respond("`⛔ Bunun bir qrup olduğuna inanmıram. Bu plugini bir qrupta cəhd et! `")
                return

            if replyneeded and not check.is_reply:
                if not notifyoff:
                    try:
                        await check.edit("`🤰🏻Plugini işlədə bilmək üçün bir mesajı yanıtlamalısan!`")
                    except:
                        await check.respond("`🤰🏻 Plugini işlədə bilmək üçün bir mesajı yanıtlamalısan!`")
                return

            try:
                await func(check)
                

            except SP:
                raise SP
            except KeyboardInterrupt:
                pass
            except MessageIdInvalidError:
                try: 
                    await check.respond('__🗒️ ( **Xəta** ) :: Pluginə aid mesaj silinmiş kimi görünür..__')
                except:
                    pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())

                    eventtext = str(check.text)
                    text = "**≛『 USERBOT XƏTA HESABATI 』≛**\n"
                    link = "[Legend Support Qrupuna](https://t.me/suplegend)"
                    if len(eventtext)<20:
                        text += f"\n**🗒️ Bunun üzündən:** {eventtext}\n"
                    text += "\n✆ İstəsəniz, bunu bildirə bilərsiniz."
                    text += f"- sadəcə bu mesajı {link} göndərin."
                    text += "**Xəta və tarix xaricində heçbir şey** yüklənə bilməz.\n"

                    ftext = ""
                    ftext += "========== XƏBƏRDARLIQ =========="
                    ftext += "\nBu Fayl sadəcə burada yükləndi,"
                    ftext += "\nSadəcə xəta və tarix qismini yüklədik,"
                    ftext += "\nGizliliyinizə hörmət edirik,"
                    ftext += "\nBurada hər hansı bir gizli data varsa"
                    ftext += "\nBu xəta hesabatı olmaya bilər, kimsə datalarınızə götürə bilməz.\n"
                    ftext += "--------USERBOT XƏTA GUNLUGU--------\n"
                    ftext += "\n➢ Tarix: " + date
                    ftext += "\n➢ Qrup ID: " + str(check.chat_id)
                    ftext += "\n➢ Göndərən kişinin ID: " + str(check.sender_id)
                    ftext += "\n\n➢ Olay Tetikləyici:\n"
                    ftext += str(check.text)
                    ftext += "\n\n➢ Xəta mətni:\n"
                    ftext += str(sys.exc_info()[1])
                    ftext += "\n\n➢ Bot versiyası:\n"
                    ftext += "{}".format(str(LEGEND_VERSION))
                    ftext += "\n\n\n➢ Geri izləmə məlumatı: \n"
                    ftext += str(format_exc())
                    ftext += "\n\n--------USERBOT XETA GUNLUGU BITIS--------"

                    command = "git log --pretty=format:\"%an: %s\" -7"

                    ftext += "\n\n\nSon 7 Güncəlləmə:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("error.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        try:
                            await check.edit("__🥺 Çox pisəm, UserBot bir xətayla qarşılaşdı.\n🐙 Xəta hesabatı Botlog qrupuna göndərildi.__")
                        except:
                            pass
                    await check.client.send_file(send_to,
                                                 "error.log",
                                                 caption=text)
                    try:
                        remove("error.log")
                    except:
                        pass
        if not disable_edited:
            bot.add_event_handler(wrapper, ME(**args))
        bot.add_event_handler(wrapper, NW(**args))

        return wrapper

    return decorator


