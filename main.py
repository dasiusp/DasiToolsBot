import os
import database

from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from datetime import date

allowed = False

group_id_name = {
    "-1001375094289": "Diretoria",
    "-1001288984466": "Administrativo",
    "-1001479427906": "Financeiro",
    "-1001360969735": "Acadêmico",
    "-1001417414524": "Comercial",
    "-1001142338317": "Esportivo",
    "-1001323151506": "TI",
    "-1001193181957": "Eventos",
    "-1001159037615": "Criação"
}


def check_group(bot, update):
    global allowed
    chat_id = str(update.message.chat.id)

    allowed_groups_ref = database.get_allowed_groups()
    allowed_groups = (allowed_groups_ref.to_dict()).values()

    if chat_id in allowed_groups:
        allowed = True
    else:
        allowed = False


def start(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    update.message.reply_text("Olá, eu fui criado pelo Vino para facilitar a marcação de " +
                              "todos os membros de um setor ou de todos os membros do DASI!\n\n" +
                              "Digite /ajuda para ver os comandos disponiveis.", quote=False)


def help(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    update.message.reply_text("Lista de comandos \n\n"+
                              "/join - Entrar na lista do seu setor e do geral\n" +
                              "/diretoria - Todos os membros da diretoria\n" +
                              "/administrativo - Todos os membros do setor Administrativo\n" +
                              "/financeiro - Todos os membros do setor Financeiro\n" +
                              "/academico - Todos os membros do setor Acadêmico\n" +
                              "/comercial - Todos os membros do setor Comercial\n" +
                              "/esportivo - Todos os membros do setor Esportivo\n" +
                              "/ti - Todos os membros do setor de TI\n" +
                              "/eventos - Todos os membros do setor de Eventos\n" +
                              "/criacao - Todos os membros do setor de Criação\n" +
                              "/todos - Todos os membros do DASI", quote=False)


def join(bot, update):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    user = update.message.from_user

    chat_id = str(update.message.chat.id)
    group_name = str(group_id_name.get(str(chat_id)))
    username = "@" + str(user.username)

    group_list_ref = database.get_group_list(group_name)
    group_list = group_list_ref.to_dict()

    if group_id_name.get(str(chat_id)) is None:
        update.message.reply_text("Função indisponível para esse chat!", quote=False)
        return

    if str(user.id) in group_list.keys():
        update.message.reply_text("Você já está na lista do seu setor!", quote=False)
    else:
        database.join_group_list(group_name, user.id, username)
        update.message.reply_text("Você entrou na lista do seu setor!", quote=False)


def show_group_members(bot, update, group_name):
    check_group(bot, update)
    if allowed is False:
        update.message.reply_text("Este grupo não tem permissão para utilizar o bot!", quote=False)
        return

    group_ref = database.get_group_list(str(group_name))
    group = (group_ref.to_dict()).values()

    if bool(group) is False:
        update.message.reply_text("Essa lista está vazia!", quote=False)
        return

    for i in range(len(group)):
        lista = " ".join(group)

    update.message.reply_text(str(group_name) + ": \n\n" + str(lista), quote=False)


def diretoria(bot, update):
    show_group_members(bot, update, "Diretoria")


def adm(bot, update):
    show_group_members(bot, update, "Administrativo")


def financeiro(bot, update):
    show_group_members(bot, update, "Financeiro")


def acad(bot, update):
    show_group_members(bot, update, "Acadêmico")


def comercial(bot, update):
    show_group_members(bot, update, "Comercial")


def esportivo(bot, update):
    show_group_members(bot, update, "Esportivo")


def ti(bot, update):
    show_group_members(bot, update, "TI")


def eventos(bot, update):
    show_group_members(bot, update, "Eventos")


def criacao(bot, update):
    show_group_members(bot, update, "Criação")


def todos(bot, update):
    show_group_members(bot, update, "Todos")


def reminder(bot, update):
    data_ref = database.get_reminder_date()
    data = data_ref.to_dict()

    year = int(data.get('year'))
    month = int(data.get('month'))
    day = int(data.get('day'))

    current_reminder = date(year, month, day)
    today = date.today()

    day_diff = (today - current_reminder)

    if (day_diff.days) >= 45:
        database.update_reminder_date(today)
        update.message.reply_text("[LEMBRETE]\n\nRealizar transação nas maquininhas de cartão para que elas não sejam desativadas", quote=False)


def invalid_message(bot, update):
    chat_type = update.message.chat.type
    chat_id = str(update.message.chat.id)

    if chat_id == "-1001375094289":
        reminder(bot, update)

    if chat_type == "private":
        check_group(bot, update)
        if allowed is False:
            update.message.reply_text("Você não tem permissão para utilizar o bot!", quote=False)
            return
        update.message.reply_text("Comando inválido! Digite /ajuda para visualizar a lista de comandos.", quote=False)


def webhook(request):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    dispatcher = Dispatcher(bot, None, 0)
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("ajuda", help))
    dispatcher.add_handler(CommandHandler("join", join))
    dispatcher.add_handler(CommandHandler("diretoria", diretoria))
    dispatcher.add_handler(CommandHandler("administrativo", adm))
    dispatcher.add_handler(CommandHandler("financeiro", financeiro))
    dispatcher.add_handler(CommandHandler("academico", acad))
    dispatcher.add_handler(CommandHandler("comercial", comercial))
    dispatcher.add_handler(CommandHandler("esportivo", esportivo))
    dispatcher.add_handler(CommandHandler("ti", ti))
    dispatcher.add_handler(CommandHandler("eventos", eventos))
    dispatcher.add_handler(CommandHandler("criacao", criacao))
    dispatcher.add_handler(CommandHandler("todos", todos))
    dispatcher.add_handler(MessageHandler(Filters.text, invalid_message))
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return "ok"
