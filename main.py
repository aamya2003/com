import telebot
from telebot.types import *
from sqll import *

bot = telebot.TeleBot("6684343029:AAE_dD9Eo1wCEqV1ExeSNIyaWeIx2x_SIk0")
# bot.send_message(5832988930, "Ahmed")



my_id = int(5832988930)

mainCommandsText = "اهلا بك يا مطوري في لوحة الاوامر!"


def MangeBot():
    mrk = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text= "تفعيل التواصل", callback_data= "on communication"),
                InlineKeyboardButton(text= "تعطيل التواصل", callback_data= "off communication"),
            ],
            [
                InlineKeyboardButton(text= "تفعيل اشعار الدخول", callback_data= "on access"),
                InlineKeyboardButton(text= "نعطيل اشعار الدخول", callback_data= "off access"),
            ],
            [
                InlineKeyboardButton(text= "الاحصائيات", callback_data= "statistics"),
            ],
            [
                InlineKeyboardButton(text= "مسح المحظورين", callback_data= "del blcs"),
                InlineKeyboardButton(text= "مسح محظور", callback_data= "del blc"),
                InlineKeyboardButton(text= "حظر", callback_data= "blc"),
            ],
            [
                InlineKeyboardButton(text= "قناة الاشتراك الاجباري", callback_data= "sub chn"),
                InlineKeyboardButton(text= "اضف قناة", callback_data= "add chn"),
                InlineKeyboardButton(text= "مسح قناة", callback_data= "del chn"),
            ],
            [
                InlineKeyboardButton(text= "اذاعة بالتثبيت", callback_data= "brdcast pin"),
                InlineKeyboardButton(text= "اذاعة", callback_data= "brdcast"),
                InlineKeyboardButton(text= "اذاعة بالتحويل", callback_data= "brdcast fod"),
            ]
        ]
    )
    return mrk

def back():
    mrk = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text= '. رجوع .',callback_data= "back")]
        ]
    )
    return mrk

def cans():
    mrk = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text= '. الغاء .',callback_data= "cans")]
        ]
    )
    return mrk


@bot.message_handler(func= lambda message: message.from_user.id in [my_id], commands=['start'])
def MainMenuDev(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    bot.send_message(chat_id=chat_id, text= mainCommandsText, reply_markup= MangeBot())




@bot.callback_query_handler(func= lambda call:True)
def MAinQury(call: CallbackQuery):
    data = call.data
    message = call.message
    chat_id = message.chat.id
    user_id = call.from_user.id
    if user_id in [my_id]:
        if data == "on communication":
            txt = "تم تقغيل التواصل"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(login=1)

        elif data == "off communication":
            txt = "تم تعطيل التواصل"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(login=0)

        elif data == "on access":
            txt = "تم تفعيل اشعارات الدخول"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(notifications=0)

        elif data == "off access":
            txt = "تم تعطيل اشعارات الدخول"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(notifications=0)


        elif data == "statistics":
            num_us, num_blcs = (get_total_mms(), get_total_bans())
            txt = "عزيزي المطور, اليك القائمة الخاصة باحصائيات البوت" + f"\nعدد مستخدمين البوت = {num_us}" + f"\nعدد المحظورين = {num_blcs}"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())


        elif data == "del blcs":
            txt = "تم حذف جميع المستخدمين المحظورين"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            unban_uss()
            
        elif data == "del blc":
            txt = "ارسل ايدي المحظور"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, unban)

        elif data == "blc":
            txt = "ارسل ايدي المستخدم"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, ban)


        elif data == "sub chn":
            ch = get_compulsory_subscription()
            txt1 = "قناة الاشتراك الاجباري" + "\nاسم القناة: {name_ch}" + "\nمعرف القناة: {us_ch}" + "\nايدي القناة: {id_ch}"
            txt2 = "عذرا, ليس لديك قناة اشتارك اجباري!"
            if ch in [0, "0"]:
                txt = txt2
            else:
                all = bot.get_chat(ch)
                txt = txt1.format(name_ch = all.title, us_ch = all.username, id_ch = all.id)

            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())

        elif data == "add chn":
            txt = "لأضافه قناة اشتراك اجباري يجب اولا رفع البوت مشرفا في القناة" + "\nارسل ايدي او معرف القناة"
            bot.register_next_step_handler(message, addCh)
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())

        elif data == "del chn":
            txt = "تم حذف قناة الاشتراك الاجباري!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=back())
            update_user_settings(compulsory_subscription=0)


        elif data == "brdcast":
            txt = "ارسل محتوى الاذاعة, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast)

        elif data == "brdcast pin":
            txt = "ارسل محتوى الاذاعة للتثبيت, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast_pin)

        elif data == "brdcast fod":
            txt = "ارسل محتوى الاذاعة للتحويل, انتبة يجب ان تكون نصية!"
            bot.edit_message_text(text= txt, chat_id=chat_id, message_id=message.id, reply_markup=cans())
            bot.register_next_step_handler(message, broadcast_fod)


        elif data == "cans":
            bot.clear_step_handler(message)
            bot.edit_message_text(text= "تم الغاء المهمة بنجاح!", chat_id=chat_id, message_id=message.id, reply_markup=back())

        elif data == "back":
            bot.edit_message_text(text= mainCommandsText, chat_id=chat_id, message_id=message.id, reply_markup=MangeBot())







def ban(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم حظر المستخدم بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        update_user(user_id= message.text, type= "blc")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def unban(message:Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    txt = "تم الغاء حظر المستخدم بنجاح!"
    if message.text:
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
        update_user(user_id= message.text, type= "mms")
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def addCh(message:Message):
    chat_id = message.chat.id
    if message.text:
        try:
            id = bot.get_chat(message.text).id
            txt = "تم اضافه قناة الاشتراك الاجباري بنجاح!"
            bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
            update_user_settings(compulsory_subscription=id)
        except:
            txt = "تحقق من وجود البوت في القناة"
            bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())

def broadcast(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                bot.send_message(user_id, message.text, disable_web_page_preview=True)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def broadcast_pin(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                m = bot.send_message(user_id, message.text, disable_web_page_preview=True)
                bot.pin_chat_message(m.chat.id, m.id)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())


def broadcast_fod(message:Message):
    chat_id = message.chat.id
    if message.text:
        for user_id in get_total_users():
            try:
                bot.forward_message(user_id, chat_id, message.id)
            except:
                pass
        txt = "تم ارسال الاذاعة الى جميع المستخدمين!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())
    else:
        txt = "يجب ان تكون الرسالة نصية!"
        bot.send_message(text= txt, chat_id=chat_id, reply_markup=back())



def EditPost(message: Message):
    title = message.chat.title
    link = bot.create_chat_invite_link(message.chat.id, name=title).invite_link
    text = (
        str(message.text) if message.text else ""
        + "\n"
        + f' Made With 💙 By  ( <a href="{link}">{title}</a> ) © 2023.' + "\n" + "."
    )
    if not message.text:
        print(True)
        bot.edit_message_caption(caption=text, chat_id=message.chat.id, message_id=message.id, reply_markup=AddMrkup(link=link, title=title), parse_mode="HTML")
    elif message.text:
        bot.edit_message_text(
            text=text,
            message_id=message.id,
            chat_id=message.chat.id,
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=AddMrkup(link=link, title=title),
        )

def AddMrkup(link, title):
    mrkup = InlineKeyboardMarkup()
    mrkup.add(InlineKeyboardButton(text="𝒩𝒶𝓂𝑒 𝒸𝒽:  " + title, url=link))
    return mrkup


@bot.channel_post_handler(content_types=telebot.util.content_type_media.remove("sticker"))
def main(message: Message):
    EditPost(message)


bot.infinity_polling(skip_pending=True)
