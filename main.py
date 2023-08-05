from pyrogram import Client, filters
import requests
import time

Token = "5803624137:AAGoGb8_P8QJIWFaDeoddb1c-hl0iPnbROs"

app = Client("Test-Bot",18660218, "bc9e7ab99ace90b7534d72203bea7fd6", bot_token=Token)

def get_result(url):
    try:
        response = requests.get(url)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def send_notification_to_channel(username, chat_id, post_url, result):
    message = f"المستخدم {username} طلب هذا المنشور:\n{post_url}\n\nالنتيجة:\n{result}"
    app.send_message(chat_id=chat_id, text=message)
@app.on_message(filters.private & filters.command("start"))
def start_command(client, message):
    client.send_message(
        message.chat.id,
        "- هلا حب.🖤\n- بوت رشق مشاهدات تلكرام\n- يمكنك رشق مشاهدات من خلال البوت مجانا 🔥.\n• كل ما عليك هو ارسال رابط المنشور 👤➕"
    )

@app.on_message(filters.private & filters.text)
def handle_message(client, message):
    base_url = "jpD70IVEDro0QsdsuDvfRC9ZRMqGtzqfUfAZ6kPtQLZ5ixYXmXh82l2KWJNO"
    post_url = message.text.strip()
    full_url = base_url + post_url

    while True:
        start_time = time.time()
        result = get_result(full_url)
        end_time = time.time()

        if result:
            client.send_message(
                message.chat.id,
                f"تم التشغيل: {result}"
            )
            if message.from_user:
                user_id = message.from_user.id
                user_name = message.from_user.first_name
                channel_id = -1001935538537  #ضع ايدي قناتك بدل من ايدي قناتي وسوف يرسل لك اشعار بكل من ارسل رابط لشرقه
                send_notification_to_channel(user_name, channel_id, post_url, result)

        elapsed_time = end_time - start_time
        if elapsed_time < 0.5:
            time.sleep(0.5 - elapsed_time)

if __name__ == "__main__":
    print("ITALY MUSIC IN TELEGRAM ♥")
    app.run()
