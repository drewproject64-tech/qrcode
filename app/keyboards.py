from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📷 Scan QR Code", callback_data="qr:scan")],
            [InlineKeyboardButton(text="🔳 Create QR Code", callback_data="qr:create")],
            [InlineKeyboardButton(text="📋 QR History", callback_data="qr:history")],
        ]
    )

def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Back", callback_data="qr:home")]]
    )
