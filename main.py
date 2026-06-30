from telethon import TelegramClient, events
from env import *
import logging
from captcha_checking import Captcha

logging.basicConfig(level=logging.INFO)

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=TOKEN)

print('Bot start...')

wait_captcha = {}
@bot.on(events.ChatAction())
async def start_handler(event):
    if event.user_joined:
        user_entity = await event.get_user()
        chat_entity = await event.get_chat()

        if user_entity.username:
            greetings = "@" + user_entity.username
        else:
            greetings = user_entity.first_name

        captcha = Captcha()

        await bot.send_message(
            entity=chat_entity,
            message=f"Привет {greetings}! Пожалуйста, введи капчу, чтобы подтвердить, что ты не бот.",
            file=captcha.captcha_image
        )
        wait_captcha[(user_entity.id, chat_entity.id)] = captcha.captcha_text

@bot.on(events.NewMessage())
async def new_msg(event):
    peer_user = event.from_id
    peer_channel = event.peer_id

    user_entity = bot.get_entity(peer_user)

    captcha = wait_captcha.get((peer_user.user_id, peer_channel.user_id))

    if captcha is not None:
        if event.text != captcha:
            await event.respond("Капча введена неверно!")
            await bot.delete_messages(peer_channel, event.message)
            await bot.kick_participant(peer_channel, peer_user)
        else:
            await event.respond(f"Добро пожаловать! {user_entity}")
            await bot.delete_messages(peer_channel, [event.message.id, event.message.id - 1])
            del wait_captcha[(peer_user.user_id, peer_channel.user_id)]
            return


def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()