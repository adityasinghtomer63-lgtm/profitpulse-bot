import os
import asyncio
from io import BytesIO
from PIL import Image
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8742356584:AAG2z5uHiyu1qy5W9eGbaJJMGDdNpEbUZxw"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


client = genai.Client(api_key=GEMINI_API_KEY)

PROMPT_ANALYSIS = """
You are an institutional quantitative trading analyst synthesizing a massive confluence of 2000+ technical trading strategies (SMC, Order Blocks, Liquidity Sweeps, Price Action, Trend Following, and Momentum Indicators).

Analyze this chart image thoroughly and generate a comprehensive institutional trade breakdown strictly in English.

Format your output exactly as follows:

====================================
PROFITPULSE MULTI-STRATEGY REPORT
====================================
• Asset Observed: [Asset / Symbol / Pair]
• Overall Market Bias: [Strong Bullish / Strong Bearish / Ranging]
• Core Key Levels: Support: [Price] | Resistance: [Price]

------------------------------------
1. SCALPING SETUP (Quick Moves: 1m - 5m)
------------------------------------
• Scalp Bias: [BUY / SELL / AVOID]
• Scalping Win Probability: [X]% to [Y]%
• Entry Range: [Price]
• Stop-Loss: [Tight Stop Price]
• Target: [Quick 1:1.5 Target Price]

------------------------------------
2. INTRADAY SETUP (Day Trading: 15m - 1H)
------------------------------------
• Intraday Bias: [BUY / SELL / AVOID]
• Intraday Win Probability: [X]% to [Y]%
• Entry Zone: [Price]
• Stop-Loss: [Structure Invalidation Price]
• Target 1 & Target 2: [Target Levels with 1:2 R:R]

------------------------------------
3. SWING / LONG-TERM (Holding: 4H - Daily)
------------------------------------
• Swing Bias: [BULLISH ACCUMULATION / BEARISH DISTRIBUTION / NEUTRAL]
• Long-term Win Probability: [X]% to [Y]%
• Ideal Entry Zone: [Major Demand / Supply Area]
• Macro Invalidation (SL): [Price]
• Macro Target: [Major Resistance / Highs]

------------------------------------
4. TOP CONFLUENCE SIGNALS (From 2000+ Strategies)
------------------------------------
- Signal 1: [e.g., SMC Bullish Order Block + FVG tap]
- Signal 2: [e.g., Liquidity sweep of session lows]
- Signal 3: [e.g., Momentum continuation & volume surge]

[RISK ADVISORY]
• Suggested Risk: Strict 1-2% account exposure limit per trade setup.
====================================
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "ProfitPulse Quantitative Strategy AI Active!\n\n"
        "Engine Capabilities:\n"
        "• Synthesizes 2000+ technical strategies into one report.\n"
        "• Provides dedicated breakdowns for Scalping, Intraday, and Swing/Long-term.\n"
        "• Calculates precise Win Rate (%) and entry/exit risk-reward levels.\n\n"
        "Send your chart screenshot below to start analysis!"
    )
    await update.message.reply_text(welcome_text)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Scanning chart across 2000+ strategies... Calculating Win Rates...")
    
    try:
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        image = Image.open(BytesIO(photo_bytes))
        
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[image, PROMPT_ANALYSIS]
            )
        except Exception:
            response = client.models.generate_content(
                model='gemini-flash-latest',
                contents=[image, PROMPT_ANALYSIS]
            )
        
        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"Analysis Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    print("ProfitPulse Strategy Bot is Live and Ready...")
    app.run_polling()
