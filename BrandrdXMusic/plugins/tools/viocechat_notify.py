from pyrogram import Client

@Client.on_chat_event("video_chat_participants_invited")
async def voice_chat_join_notify(client, chat_event):
    chat_id = chat_event.chat.id
    invited_users = chat_event.new_participants
    for user in invited_users:
        name = (user.first_name or "") + (" " + user.last_name if user.last_name else "")
        username = f"@{user.username}" if user.username else "No username"
        user_id = user.id
        msg = (
            f"👤 User joined voice chat:\n"
            f"Name: {name}\n"
            f"Username: {username}\n"
            f"User ID: `{user_id}`"
        )
        await client.send_message(chat_id, msg)
