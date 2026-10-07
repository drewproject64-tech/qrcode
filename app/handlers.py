from pathlib import Path

import cv2
import numpy as np
import qrcode
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from .config import ADMIN_ID, BOT_NAME
from .keyboards import back_menu, main_menu
from .states import QRStates
from .storage import get_state, update_state

router = Router()

HELP_TEXT = (
    f"<b>{BOT_NAME}</b>\n\n"
    "Scan QR codes from images or create a new QR code from text or a URL.\n\n"
    "Choose a function below:"
)

async def send_home(message: Message) -> None:
    state = get_state()
    if state["redirect_enabled"]:
        image_path = Path(state["promo_image"])
        if image_path.exists():
            await message.answer_photo(FSInputFile(image_path), caption=state["promo_text"])
        else:
            await message.answer(state["promo_text"])
        return
    await message.answer(HELP_TEXT, reply_markup=main_menu())

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await send_home(message)

@router.message(Command("redirect"))
async def redirect_handler(message: Message) -> None:
    if not message.from_user or message.from_user.id != ADMIN_ID:
        return
    parts = (message.text or "").split(maxsplit=1)
    action = parts[1].strip().lower() if len(parts) > 1 else ""
    if action == "on":
        update_state(redirect_enabled=True)
        await message.answer("✅ Redirect mode enabled.")
    elif action == "off":
        update_state(redirect_enabled=False)
        await message.answer("✅ Redirect mode disabled. QR functions are active.")
    elif action == "status":
        enabled = get_state()["redirect_enabled"]
        await message.answer(f"Redirect mode: {'ON' if enabled else 'OFF'}")
    else:
        await message.answer("Usage: /redirect on | /redirect off | /redirect status")

@router.callback_query(F.data == "qr:home")
async def home_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(HELP_TEXT, reply_markup=main_menu())
    await callback.answer()

@router.callback_query(F.data == "qr:scan")
async def scan_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QRStates.waiting_scan)
    await callback.message.edit_text(
        "📷 <b>Scan QR Code</b>\n\nSend a photo containing a QR code.",
        reply_markup=back_menu(),
    )
    await callback.answer()

@router.message(QRStates.waiting_scan, F.photo)
async def scan_photo(message: Message, state: FSMContext) -> None:
    try:
        file = await message.bot.get_file(message.photo[-1].file_id)
        downloaded = await message.bot.download_file(file.file_path)
        image_bytes = np.frombuffer(downloaded.read(), dtype=np.uint8)
        image = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Unable to decode image")
        detector = cv2.QRCodeDetector()
        value, points, _ = detector.detectAndDecode(image)
        if value:
            await message.answer(
                f"✅ <b>QR Code detected</b>\n\n<code>{value}</code>",
                reply_markup=main_menu(),
            )
        else:
            await message.answer(
                "❌ No readable QR code was detected. Please send a clearer image.",
                reply_markup=main_menu(),
            )
    except Exception:
        await message.answer(
            "❌ I couldn't process that image. Please try again with a clear QR image.",
            reply_markup=main_menu(),
        )
    finally:
        await state.clear()

@router.message(QRStates.waiting_scan)
async def scan_non_photo(message: Message) -> None:
    await message.answer("Please send a photo containing a QR code.", reply_markup=back_menu())

@router.callback_query(F.data == "qr:create")
async def create_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(QRStates.waiting_create)
    await callback.message.edit_text(
        "<b>Create QR Code</b>\n\nSend the text or URL you want to encode.",
        reply_markup=back_menu(),
    )
    await callback.answer()

@router.message(QRStates.waiting_create, F.text)
async def create_qr(message: Message, state: FSMContext) -> None:
    content = message.text.strip()
    if not content:
        await message.answer("Please send text or a URL.")
        return
    output = Path("/tmp/qr_generated.png")
    qrcode.make(content).save(output)
    await message.answer_photo(FSInputFile(output), caption="✅ QR code created.", reply_markup=main_menu())
    await state.clear()

@router.message(QRStates.waiting_create)
async def create_non_text(message: Message) -> None:
    await message.answer("Please send text or a URL to create a QR code.", reply_markup=back_menu())

@router.callback_query(F.data == "qr:history")
async def history_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📋 <b>QR History</b>\n\n"
        "No QR content is stored by this version of the bot.",
        reply_markup=back_menu(),
    )
    await callback.answer()
