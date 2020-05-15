import shutil
import signal
import pickle

from os import execl, path, remove
from sys import executable

from telegram.ext import CommandHandler, run_async
from bot import dispatcher, updater, botStartTime
from bot.helper.ext_utils import fs_utils
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.message_utils import *
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time
from .helper.telegram_helper.filters import CustomFilters
from .modules import authorize1, list1, cancel_mirror1, mirror_status1, mirror1, clone1, watch1


@run_async
def stats(update, context):
    currentTime = get_readable_time((time.time() - botStartTime))
    total, used, free = shutil.disk_usage('.')
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    stats = f'Bot Uptime: {currentTime}\n' \
            f'Total disk space: {total}\n' \
            f'Used: {used}\n' \
            f'Free: {free}'
    sendMessage(stats, context.bot, update)


@run_async
def start1(update, context):
    sendMessage("This is a bot which can mirror all your links to Google drive!\n"
                "Type /help1 to get a list of available commands", context.bot, update)


@run_async
def restart1(update, context):
    restart1_message = sendMessage("Restarting, Please wait!", context.bot, update)
    # Save restart message object in order to reply to it after restarting
    fs_utils.clean_all()
    with open('restart.pickle', 'wb') as status:
        pickle.dump(restart_message, status)
    execl(executable, executable, "-m", "bot")


@run_async
def ping1(update, context):
    start_time = int(round(time.time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update)
    end_time = int(round(time.time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)


@run_async
def log1(update, context):
    sendLogFile(context.bot, update)


@run_async
def bot_help1(update, context):
    help_string = f'''
/{BotCommands.Help1Command}: To get this message

/{BotCommands.Mirror1Command} [download_url][magnet_link]: Start mirroring the link to google drive

/{BotCommands.TarMirror1Command} [download_url][magnet_link]: start mirroring and upload the archived (.tar) version of the download

/{BotCommands.Watch1Command} [youtube-dl supported link]: Mirror through youtube-dl 

/{BotCommands.TarWatch1Command} [youtube-dl supported link]: Mirror through youtube-dl and tar before uploading

/{BotCommands.Cancel1Mirror} : Reply to the message by which the download was initiated and that download will be cancelled

/{BotCommands.Status1Command}: Shows a status of all the downloads

/{BotCommands.List1Command} [search term]: Searches the search term in the Google drive, if found replies with the link

/{BotCommands.Stats1Command}: Show Stats of the machine the bot is hosted on

/{BotCommands.Authorize1Command}: Authorize a chat or a user to use the bot (Can only be invoked by owner of the bot)

/{BotCommands.Log1Command}: Get a log file of the bot. Handy for getting crash reports

Watch video - https://youtu.be/07Pj9YLdpM4
'''
    sendMessage(help_string, context.bot, update)


def main():
    fs_utils.start_cleanup()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        restart_message.edit_text("Restarted Successfully!")
        remove('restart.pickle')

    start_handler = CommandHandler(BotCommands.Start1Command, start1,
                                   filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    ping_handler = CommandHandler(BotCommands.Ping1Command, ping1,
                                  filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    restart_handler = CommandHandler(BotCommands.Restart1Command, restart1,
                                     filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.Help1Command,
                                  bot_help1, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.Stats1Command,
                                   stats1, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.Log1Command, log1, filters=CustomFilters.owner_filter)
    dispatcher.add_handler(start1_handler)
    dispatcher.add_handler(ping1_handler)
    dispatcher.add_handler(restart1_handler)
    dispatcher.add_handler(help1_handler)
    dispatcher.add_handler(stats1_handler)
    dispatcher.add_handler(log1_handler)
    updater.start_polling()
    LOGGER.info("Bot Started!")
    signal.signal(signal.SIGINT, fs_utils.exit_clean_up)


main()
