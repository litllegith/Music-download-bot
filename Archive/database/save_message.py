import aiosqlite

async def save_message(
    message_id: int,
    chat_id: int
):
    async with aiosqlite.connect("users.db") as db:
        await db.execute("DELETE FROM data WHERE chat_id = ?", (chat_id,))
    
        await db.execute("INSERT INTO data (message_id, chat_id) VALUES (?, ?)", (message_id, chat_id))
        await db.commit()
