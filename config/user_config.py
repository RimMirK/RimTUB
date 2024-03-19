f"""\__| Основные настройки |__/"""

PHONES = [] # Номера телефонов в международном формате ["+380..", "+1234"]

PREFIX = '.' # префикс перед командой.
# если "." то команда выглядит как ".command"
# если "!" то команда выглядит как "!command"

PLAY_SOUND = True # воспроизводить ли звук при запуске True | False

SHOW_HEADER_IN_HELP = False

f""" Настройки Встроенных модулей """ 

from pyrogram import filters

f""" ChatTools - настройка сохранения удаленных сообщений """

DELETED_MESSAGES_CHAT_ID = 0 # Идентификатор чата куда сохранять сообщения.
# В Чате в который хотите сохранять пропишите команду `cid`
# Полученное число вставьте выше

DELETED_MESSAGES_FILTERS = filters.all 
# Фильтры сообщений которые будут сохранены при удалени.

# & - и
# ~ - не
# | - или

# filters.all - все сообщения
# filters.all & ~filters.me - все сообщения кроме своих
# filters.chat([123456, 654321]) - Только из определенных чатов
# ~filters.chat([-1029384756]) - все кроме определенных
#

f""" Funni plugin """

TYPING_SYMBOL = "█" # символ, который эмитирует курсор при команде type



f""" code_photo plugin """

PHOTO_PARAMS = dict(
    background_color = (255, 255, 255, 1),
    drop_shadow = True,
    shadow_blur_radius_px = 68,
    shadow_offset_y_px = 20,
    export_size = 2,
    font_size_px = 14,
    font_family = 'hack',
    first_line_number = 1,
    line_height_percent = 1.33,
    show_line_numbers = True,
    show_window_controls = True,
    show_watermark = False,
    horizontal_padding_px = 56,
    vertical_padding_px = 56,
    adjust_width = True,
    theme = 'vscode',
    window_theme = 'none'
)