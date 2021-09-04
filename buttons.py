from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,ForceReply

CREATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('📝 Maqola yaratish', callback_data='create')
        ]]
    )
    
DEL_BUTTONS = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton('🗑', callback_data="del")
    
    
        ]])
        
markup = ForceReply(selective=False)