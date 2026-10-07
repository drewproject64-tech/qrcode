# QR Code Scan

Telegram QR utility bot using Python 3.12 and aiogram 3.x.

## Main functions

1. Scan QR Code
2. Create QR Code
3. QR History

## Admin redirect

Only ADMIN_ID can change the global mode.

- /redirect on
- /redirect off
- /redirect status

When redirect mode is ON, /start sends the promotional image and the configured promotional text instead of the QR menu.

Put the promotional image at `assets/promo.jpg`.

## Environment

Set BOT_TOKEN and ADMIN_ID in your environment.

## Render

The repository contains a Dockerfile and render.yaml for deployment.
