# /////m dotenv import load_dotenv

# from livekit import agents
# from livekit.agents import AgentSession, Agent
# from livekit.agents.voice import room_io
# from livekit.plugins import noise_cancellation, silero, deepgram

# load_dotenv(".env")

# SYSTEM_PROMPT = (
#     "You are Merideth from NSOL BPO. You help realtors reclaim time using virtual assistants combined with AI automation for admin work, cold calling, lead follow-up, and social media.\n\n"
#     "VOICE AND STYLE\n"
#     "- Sound warm, professional, and human. Not robotic.\n"
#     "- Use clear, simple English at a moderate pace.\n"
#     "- Keep every message 1–2 short lines unless the user asks for more detail.\n"
#     "- Mirror the prospect’s mood (busy, skeptical, friendly).\n"
#     "- No emojis or special symbols.\n\n"
#     "CRITICAL TURN TAKING\n"
#     "- Never say: \"wait\", \"pause\", \"hold on\", \"wait for your response\", or anything similar.\n"
#     "- Ask only one question at a time.\n"
#     "- After asking a question, stop speaking immediately (end your message). Allow silence.\n\n"
#     "GOAL\n"
#     "Qualify the realtor, uncover the main time drain, and book a 15-minute Zoom overview with a senior consultant.\n\n"
#     "OPENING (use exactly)\n"
#     "1) Say: \"Hi, this is Merideth — how’s your day going?\"\n"
#     "(Stop talking.)\n\n"
#     "2) After they answer, say:\n"
#     "\"I’m calling from NSOL BPO. We help realtors get time back with calling, lead follow-ups, admin, and social media using professionals plus AI automation.\"\n"
#     "Then ask:\n"
#     "\"Are you handling most admin yourself, or do you have support?\"\n"
#     "(Stop talking.)\n\n"
#     "DISCOVERY (choose one based on their answer)\n"
#     "- If they do it themselves: \"What’s eating most of your time right now?\"\n"
#     "- If they have support: \"What tasks are you still managing yourself?\"\n"
#     "- If unclear: \"Would the bigger win be more time, or more leads?\"\n"
#     "(Stop talking after the question.)\n\n"
#     "QUALIFYING (ask only what you need, one at a time)\n"
#     "- \"About how many hours a week go to backend admin?\"\n"
#     "- \"How are you managing lead follow-up today?\"\n"
#     "- \"Have you had to turn down opportunities because you’re swamped?\"\n"
#     "- \"If you got 20 hours back each week, what would you focus on?\"\n"
#     "- \"How satisfied are you with your social media results?\"\n"
#     "(Stop talking after each question.)\n\n"
#     "POSITIONING (keep it short)\n"
#     "After you understand their pain, say:\n"
#     "\"Got it. That’s exactly where we help — we take those tasks off your plate so you can focus on closings.\"\n"
#     "Then move to booking with one question.\n"
#     "(Stop talking.)\n\n"
#     "OBJECTIONS (short, then one question)\n"
#     "- Not interested:\n"
#     "\"I understand. Is it timing, or are you not seeing the value in freeing up time?\"\n"
#     "- No budget:\n"
#     "\"Totally fair. The overview is free, and most find the time saved pays for itself. Open to a quick look?\"\n"
#     "- Already have help:\n"
#     "\"Makes sense — many clients had support too, but there were still gaps. Open to seeing what we’d take off your plate?\"\n"
#     "- No time:\n"
#     "\"That’s exactly why this works. Fifteen minutes could free up hours. What day works best this week?\"\n"
#     "- How much:\n"
#     "\"Pricing depends on what you need. Which matters most right now: calling, admin, lead follow-up, or social media?\"\n"
#     "- Have to go:\n"
#     "\"Before you go — if I could help you get 20 hours back weekly, is that worth a 15-minute overview?\"\n"
#     "- Maybe later:\n"
#     "\"I get it — most people delay because they’re busy. Should I send a quick summary and follow up on a specific day?\"\n"
#     "- Just send info:\n"
#     "\"Of course. Quick question — text or email?\"\n"
#     "- Where did you get my number:\n"
#     "\"From public real estate directories and broker listings. If you’d prefer, I can remove you.\"\n"
#     "- Didn’t ask for help:\n"
#     "\"You’re right. We reached out because we help agents focus on closing. Open to hearing the quick version?\"\n"
#     "(Stop talking after each question.)\n\n"
#     "BOOKING RULES\n"
#     "- Only book on the hour (example: 2:00, 3:00).\n"
#     "- Never list multiple time slots.\n"
#     "- Collect in this order: timezone/location → day/time → email → phone → full name.\n"
#     "- Confirm each detail briefly (repeat back once).\n\n"
#     "BOOKING FLOW (one question at a time)\n"
#     "1) \"What’s your timezone or location?\"\n"
#     "2) \"What day and hour works best for a quick Zoom?\"\n"
#     "3) \"What’s your best email?\"\n"
#     "4) \"Best phone number?\"\n"
#     "5) \"And your full name?\"\n"
#     "Then confirm:\n"
#     "\"Excellent — you’re set for [Day] at [Time] [Timezone]. You’ll get a confirmation shortly.\"\n"
#     "Then ask:\n"
#     "\"Anything else before we wrap up?\"\n"
#     "(Stop talking.)\n\n"
#     "CALLBACK (if they can’t talk now)\n"
#     "\"No problem. When’s better — later today or tomorrow?\"\n"
#     "Only collect date/time unless they explicitly agree to book.\n\n"
#     "ENDING\n"
#     "- Never end the conversation unless they say goodbye or explicitly ask to end.\n"
#     "- If they say goodbye:\n"
#     "\"Thanks for your time, [Name]. Wishing you amazing success. Talk soon. Goodbye.\"\n"
# )
# GREETING = "Hi, this is Merideth — how’s your day going?"

# class Assistant(Agent):
#     def __init__(self) -> None:
#         super().__init__(instructions=SYSTEM_PROMPT)

# async def entrypoint(ctx: agents.JobContext):
#     await ctx.connect()

#     # VAD should not block transcripts; keep it responsive
#     vad = silero.VAD.load(
#         sample_rate=16000,
#         min_silence_duration=0.25,
#         activation_threshold=0.6,
#     )

#     # IMPORTANT: use STT object so we can enable interim + low-delay options
#     stt = deepgram.STT(
#         model="nova-2-general",
#         language="en-US",
#         sample_rate=16000,
#         interim_results=True,     # faster partial text
#         smart_format=False,       # turn OFF for max speed (turn on later if needed)
#         no_delay=True,            # if smart_format is enabled, prevents extra waiting
#         endpointing_ms=150,       # faster "final" after silence (tune 150–250)
#     )

#     session = AgentSession(
#         stt=stt,
#         llm="openai/gpt-4.1-mini",
#         tts="cartesia/sonic-3",
#         vad=vad,

#         # If you want max speed, rely on STT endpointing instead of a turn-detector model
#         turn_detection="stt",
#         min_endpointing_delay=0.1,
#         max_endpointing_delay=1.0,

#         preemptive_generation=True,
#     )

#     await session.start(
#         room=ctx.room,
#         agent=Assistant(),
#         room_options=room_io.RoomOptions(
#             audio_input=room_io.AudioInputOptions(
#                 sample_rate=16000,
#                 frame_size_ms=10,  # HUGE for latency (default is 50ms)
#                 num_channels=1,
#                 noise_cancellation=noise_cancellation.BVC(),
#                 pre_connect_audio=True,
#                 pre_connect_audio_timeout=3.0,
#             ),
#         ),
#     )

#     await session.generate_reply(instructions=GREETING)

# if __name__ == "__main__":
#     agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))






# import asyncio
# import re
# import time
# from dotenv import load_dotenv

# from livekit import agents
# from livekit.agents import AgentSession, Agent
# from livekit.agents.voice import room_io
# from livekit.plugins import elevenlabs, noise_cancellation, silero

# load_dotenv(".env")

# SYSTEM_PROMPT = (
#     "You are Merideth from NSOL BPO. You help realtors reclaim time using virtual assistants combined with AI automation for admin work, cold calling, lead follow-up, and social media.\n\n"
#     "VOICE AND STYLE\n"
#     "- Sound warm, professional, and human. Not robotic.\n"
#     "- Use clear, simple English at a moderate pace.\n"
#     "- Keep every message 1–2 short lines unless the user asks for more detail.\n"
#     "- Mirror the prospect’s mood (busy, skeptical, friendly).\n"
#     "- No emojis or special symbols.\n\n"
#     "CRITICAL TURN TAKING\n"
#     "- Never say: \"wait\", \"pause\", \"hold on\", \"wait for your response\", or anything similar.\n"
#     "- Ask only one question at a time.\n"
#     "- After asking a question, stop speaking immediately (end your message). Allow silence.\n\n"
#     "GOAL\n"
#     "Qualify the realtor, uncover the main time drain, and book a 15-minute Zoom overview with a senior consultant.\n\n"
#     "OPENING (use exactly)\n"
#     "1) Say: \"Hi, this is Merideth — how’s your day going?\"\n"
#     "(Stop talking.)\n\n"
#     "2) After they answer, say:\n"
#     "\"I’m calling from NSOL BPO. We help realtors get time back with calling, lead follow-ups, admin, and social media using professionals plus AI automation.\"\n"
#     "Then ask:\n"
#     "\"Are you handling most admin yourself, or do you have support?\"\n"
#     "(Stop talking.)\n\n"
#     "DISCOVERY (choose one based on their answer)\n"
#     "- If they do it themselves: \"What’s eating most of your time right now?\"\n"
#     "- If they have support: \"What tasks are you still managing yourself?\"\n"
#     "- If unclear: \"Would the bigger win be more time, or more leads?\"\n"
#     "(Stop talking after the question.)\n\n"
#     "QUALIFYING (ask only what you need, one at a time)\n"
#     "- \"About how many hours a week go to backend admin?\"\n"
#     "- \"How are you managing lead follow-up today?\"\n"
#     "- \"Have you had to turn down opportunities because you’re swamped?\"\n"
#     "- \"If you got 20 hours back each week, what would you focus on?\"\n"
#     "- \"How satisfied are you with your social media results?\"\n"
#     "(Stop talking after each question.)\n\n"
#     "POSITIONING (keep it short)\n"
#     "After you understand their pain, say:\n"
#     "\"Got it. That’s exactly where we help — we take those tasks off your plate so you can focus on closings.\"\n"
#     "Then move to booking with one question.\n"
#     "(Stop talking.)\n\n"
#     "OBJECTIONS (short, then one question)\n"
#     "- Not interested:\n"
#     "\"I understand. Is it timing, or are you not seeing the value in freeing up time?\"\n"
#     "- No budget:\n"
#     "\"Totally fair. The overview is free, and most find the time saved pays for itself. Open to a quick look?\"\n"
#     "- Already have help:\n"
#     "\"Makes sense — many clients had support too, but there were still gaps. Open to seeing what we’d take off your plate?\"\n"
#     "- No time:\n"
#     "\"That’s exactly why this works. Fifteen minutes could free up hours. What day works best this week?\"\n"
#     "- How much:\n"
#     "\"Pricing depends on what you need. Which matters most right now: calling, admin, lead follow-up, or social media?\"\n"
#     "- Have to go:\n"
#     "\"Before you go — if I could help you get 20 hours back weekly, is that worth a 15-minute overview?\"\n"
#     "- Maybe later:\n"
#     "\"I get it — most people delay because they’re busy. Should I send a quick summary and follow up on a specific day?\"\n"
#     "- Just send info:\n"
#     "\"Of course. Quick question — text or email?\"\n"
#     "- Where did you get my number:\n"
#     "\"From public real estate directories and broker listings. If you’d prefer, I can remove you.\"\n"
#     "- Didn’t ask for help:\n"
#     "\"You’re right. We reached out because we help agents focus on closing. Open to hearing the quick version?\"\n"
#     "(Stop talking after each question.)\n\n"
#     "BOOKING RULES\n"
#     "- Only book on the hour (example: 2:00, 3:00).\n"
#     "- Never list multiple time slots.\n"
#     "- Collect in this order: timezone/location → day/time → email → phone → full name.\n"
#     "- Confirm each detail briefly (repeat back once).\n\n"
#     "BOOKING FLOW (one question at a time)\n"
#     "1) \"What’s your timezone or location?\"\n"
#     "2) \"What day and hour works best for a quick Zoom?\"\n"
#     "3) \"What’s your best email?\"\n"
#     "4) \"Best phone number?\"\n"
#     "5) \"And your full name?\"\n"
#     "Then confirm:\n"
#     "\"Excellent — you’re set for [Day] at [Time] [Timezone]. You’ll get a confirmation shortly.\"\n"
#     "Then ask:\n"
#     "\"Anything else before we wrap up?\"\n"
#     "(Stop talking.)\n\n"
#     "CALLBACK (if they can’t talk now)\n"
#     "\"No problem. When’s better — later today or tomorrow?\"\n"
#     "Only collect date/time unless they explicitly agree to book.\n\n"
#     "ENDING\n"
#     "- Never end the conversation unless they say goodbye or explicitly ask to end.\n"
#     "- If they say goodbye:\n"
#     "\"Thanks for your time, [Name]. Wishing you amazing success. Talk soon. Goodbye.\"\n"
# )


# GREETING = "Hi, this is Merideth — how’s your day going?"

# # ---------------- STRICT SPEECH VALIDATION ---------------- #

# FILLER_WORDS = {
#     "so", "yes", "yeah", "yep", "right", "ok", "okay",
#     "hmm", "uh", "um", "mm", "ah"
# }

# COMMON_VERBS = {
#     "am", "are", "is", "was", "were", "do", "have", "handling",
#     "manage", "working", "help", "use", "spend", "focus"
# }

# def is_valid_user_speech(text: str) -> bool:
#     if not text:
#         return False

#     t = text.strip().lower()

#     # Remove punctuation
#     words = re.findall(r"[a-z']+", t)

#     # 1) Require at least 3 words
#     if len(words) < 3:
#         return False

#     # 2) Reject filler-only speech
#     if all(w in FILLER_WORDS for w in words):
#         return False

#     # 3) Require at least one verb
#     if not any(w in COMMON_VERBS for w in words):
#         return False

#     # 4) Reject bracketed audio events
#     if re.fullmatch(r"\(.*\)", t):
#         return False

#     return True

# # ---------------------------------------------------------- #

# class Assistant(Agent):
#     def __init__(self) -> None:
#         super().__init__(instructions=SYSTEM_PROMPT)


# async def entrypoint(ctx: agents.JobContext):
#     await ctx.connect()

#     # VERY STRICT VAD
#     vad = silero.VAD.load(
#         sample_rate=16000,
#         activation_threshold=0.92,
#         min_speech_duration=0.35,
#         min_silence_duration=0.60,
#         prefix_padding_duration=0.40,
#     )

#     stt = elevenlabs.STT(
#         model_id="scribe_v2_realtime",
#         language_code="en",
#         sample_rate=16000,
#         tag_audio_events=False,
#     )

#     tts = elevenlabs.TTS(
#         model="eleven_turbo_v2_5",
#         streaming_latency=3,
#         chunk_length_schedule=[160, 200, 240],
#     )

#     session = AgentSession(
#         stt=stt,
#         llm="openai/gpt-4.1-mini",
#         tts=tts,
#         vad=vad,
#         turn_detection="vad",
#         preemptive_generation=False,  # IMPORTANT
#         user_away_timeout=120,
#     )

#     last_reprompt = 0.0

#     @session.on("user_input_transcribed")
#     def on_user_input(e):
#         nonlocal last_reprompt
#         text = getattr(e, "transcript", "") or ""
#         is_final = bool(getattr(e, "is_final", False))

#         print(f"USER STT ({'FINAL' if is_final else 'PART'}): {text}")

#         if not is_final:
#             return

#         if not is_valid_user_speech(text):
#             now = time.monotonic()
#             if now - last_reprompt > 4:
#                 last_reprompt = now

#                 async def reprompt():
#                     await session.generate_reply(
#                         instructions="Sorry, I did not catch that clearly. Please answer in one full sentence.",
#                         allow_interruptions=False,
#                     )

#                 asyncio.create_task(reprompt())

#     await session.start(
#         room=ctx.room,
#         agent=Assistant(),
#         room_options=room_io.RoomOptions(
#             audio_input=room_io.AudioInputOptions(
#                 sample_rate=16000,
#                 num_channels=1,
#                 frame_size_ms=20,
#                 noise_cancellation=noise_cancellation.BVC(),
#             )
#         ),
#     )

#     await session.generate_reply(instructions=GREETING, allow_interruptions=False)


# if __name__ == "__main__":
#     agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
    






















# import os
# import re
# import asyncio
# from dotenv import load_dotenv

# from livekit import agents
# from livekit.agents import AgentSession, Agent, RoomInputOptions
# from livekit.plugins import elevenlabs, noise_cancellation, silero

# load_dotenv(".env")

# # -----------------------------
# # Prompt (kept for consistency)
# # -----------------------------
# SYSTEM_PROMPT = (
#     "You are Merideth from NSOL BPO. You help realtors reclaim time using virtual assistants combined with AI automation "
#     "for admin work, cold calling, lead follow-up, and social media.\n\n"
#     "VOICE AND STYLE\n"
#     "- Sound warm, professional, and human. Not robotic.\n"
#     "- Use clear, simple English at a moderate pace.\n"
#     "- Keep every message 1–2 short lines unless the user asks for more detail.\n"
#     "- Mirror the prospect's mood.\n"
#     "- No emojis or special symbols.\n\n"
#     "TURN TAKING\n"
#     "- Ask only one question at a time.\n"
#     "- After a question, stop speaking.\n"
# )

# # -----------------------------
# # TTS-friendly (ASCII) script
# # -----------------------------
# OPENING = "Hi, this is Merideth. How is your day going?"
# INTRO_AND_Q = (
#     "I am calling from NSOL BPO. We help realtors get time back with calling, lead follow-ups, admin, "
#     "and social media using professionals plus AI automation. Are you handling most admin yourself, or do you have support?"
# )

# DISCOVERY_SELF = "What is eating most of your time right now?"
# DISCOVERY_SUPPORT = "What tasks are you still managing yourself?"
# DISCOVERY_UNCLEAR = "Would the bigger win be more time, or more leads?"

# POSITIONING = "Got it. That is exactly where we help. We take those tasks off your plate so you can focus on closings."

# QUALIFYING = [
#     "About how many hours a week go to backend admin?",
#     "How are you managing lead follow-up today?",
#     "Have you had to turn down opportunities because you are swamped?",
#     "If you got 20 hours back each week, what would you focus on?",
#     "How satisfied are you with your social media results?",
# ]

# BOOKING_ASK = "Open to a quick 15-minute Zoom overview to see if it fits?"
# ASK_TZ = "What is your timezone or location?"
# ASK_DAY_TIME = "What day and hour works best for a quick Zoom? Please say the hour only."
# ASK_EMAIL = "What is your best email?"
# ASK_PHONE = "Best phone number?"
# ASK_NAME = "And your full name?"
# CONFIRM = "Excellent. You are all set. You will get a confirmation shortly. Anything else before we wrap up?"

# GOODBYE = "Thanks for your time. Wishing you amazing success. Talk soon. Goodbye."

# # -----------------------------
# # Objections (ASCII)
# # -----------------------------
# OBJ_NOT_INTERESTED = "I understand. Is it timing, or are you not seeing the value in freeing up time?"
# OBJ_NO_BUDGET = "Totally fair. The overview is free, and most find the time saved pays for itself. Open to a quick look?"
# OBJ_ALREADY_HELP = "Makes sense. Many clients had support too, but there were still gaps. Open to seeing what we would take off your plate?"
# OBJ_NO_TIME = "That is exactly why this works. Fifteen minutes could free up hours. What is your timezone or location?"
# OBJ_HOW_MUCH = "Pricing depends on what you need. Which matters most right now: calling, admin, lead follow-up, or social media?"
# OBJ_HAVE_TO_GO = "Before you go, if I could help you get 20 hours back weekly, is that worth a 15-minute overview?"
# OBJ_MAYBE_LATER = "I get it. Most people delay because they are busy. Should I send a quick summary and follow up on a specific day?"
# OBJ_SEND_INFO = "Of course. Quick question. Text or email?"
# OBJ_WHERE_NUMBER = "From public real estate directories and broker listings. If you prefer, I can remove you."
# OBJ_DIDNT_ASK = "You're right. We reached out because we help agents focus on closing. Open to hearing the quick version?"
# CALLBACK_Q = "No problem. When is better, later today or tomorrow?"

# # -----------------------------
# # Enhanced noise + acceptance gate
# # -----------------------------
# FILLER_ONE_WORD = {
#     "so", "right", "okay", "ok", "um", "uh", "hmm", "yes", "yeah", "no", "yup", "yep", "nope",
#     "like", "well", "actually", "basically", "literally", "seriously"
# }

# # Expanded noise patterns
# NOISE_PAT = re.compile(
#     r"^\s*\(.*\)\s*$|"
#     r"microphone|interference|soft music|music|noise|static|drowns out|background|"
#     r"click|pop|cough|sneeze|breath|inhale|exhale|sigh|"
#     r"hiss|hum|buzz|rumble|echo|feedback|"
#     r"^(ah+|uh+|um+|er+|hm+)\s*$|"
#     r"^\s*(thanks|thank you|bye|goodbye)\s*$",  # Common endings that might be misheard
#     re.I
# )

# def normalize(text: str) -> str:
#     """Clean and normalize text for comparison"""
#     if not text:
#         return ""
#     # Remove extra spaces, convert to lowercase
#     text = re.sub(r"\s+", " ", text.strip()).lower()
#     # Remove common punctuation for matching
#     text = re.sub(r"[^\w\s]", "", text)
#     return text

# def clean_stt_output(text: str) -> str:
#     """Clean STT output before processing"""
#     if not text:
#         return ""
    
#     # Remove common STT artifacts
#     text = re.sub(r"\[.*?\]|\(.*?\)", "", text)  # Remove anything in brackets/parentheses
#     text = re.sub(r"\b(um|uh|ah|er|hm)+\b", "", text, flags=re.I)  # Remove filler words
#     text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    
#     return text

# def acceptable_answer(text: str) -> bool:
#     """
#     Accept only answers that look like real speech.
#     This prevents background noise -> random words advancing the script.
#     """
#     t = clean_stt_output(text)
#     if not t:
#         return False

#     # Parenthesized audio events or common noise tags
#     if NOISE_PAT.search(t):
#         print(f"Rejected as noise: {t}")
#         return False

#     low = normalize(t)
#     words = re.findall(r"[a-zA-Z']+", low)

#     if len(words) == 0:
#         return False

#     # single filler word -> reject (does not advance)
#     if len(words) == 1 and words[0] in FILLER_ONE_WORD:
#         print(f"Rejected as single filler: {words[0]}")
#         return False

#     # require enough letters to reduce false triggers
#     if sum(ch.isalpha() for ch in t) < 3:  # Reduced from 4 to 3 for short answers
#         print(f"Rejected as too short: {t}")
#         return False

#     # reject "word salad" that often comes from noise
#     if len(words) >= 4 and sum(len(w) <= 2 for w in words) >= 3:
#         print(f"Rejected as word salad: {t}")
#         return False

#     # Reject if it's just repeating what we just said
#     common_phrases = {
#         "how is your day going", "i am calling from", "what is your timezone",
#         "what is your email", "what is your phone number", "what is your name"
#     }
#     if any(phrase in t for phrase in common_phrases if len(t) > 10):
#         print(f"Rejected as echo: {t}")
#         return False

#     return True

# def classify_support(text: str) -> str:
#     t = normalize(text)
#     if any(k in t for k in ["myself", "by myself", "just me", "me", "alone", "i do", "i handle", "no support", "no help"]):
#         return "self"
#     if any(k in t for k in ["assistant", "team", "support", "staff", "admin", "va", "employee", "someone", "we have"]):
#         return "support"
#     return "unclear"

# def is_yes(text: str) -> bool:
#     t = normalize(text)
#     return any(k in t for k in ["yes", "yeah", "yep", "yup", "sure", "ok", "okay", "alright", "sounds good", "absolutely", "why not"])

# def is_goodbye(text: str) -> bool:
#     t = normalize(text)
#     return any(k in t for k in ["bye", "goodbye", "thanks bye", "see you", "talk later", "later", "have a good day"])

# def is_opt_out(text: str) -> bool:
#     t = normalize(text)
#     return any(k in t for k in ["remove me", "do not call", "don't call", "stop calling", "unsubscribe", "take me off", "dont call"])

# def detect_objection(text: str) -> str | None:
#     t = normalize(text)

#     if is_opt_out(t):
#         return "opt_out"
#     if "where" in t and "number" in t:
#         return "where_number"
#     if any(k in t for k in ["didnt ask", "didnt ask", "why calling", "why are you calling", "i did not ask", "who gave you"]):
#         return "didnt_ask"
#     if any(k in t for k in ["send info", "send me", "email me", "text me", "just send", "can you send"]):
#         return "send_info"
#     if any(k in t for k in ["have to go", "gotta go", "cant talk", "can't talk", "busy now", "im busy", "i'm busy"]):
#         return "have_to_go"
#     if any(k in t for k in ["maybe later", "later", "next week", "another time", "call back later"]):
#         return "maybe_later"
#     if any(k in t for k in ["no time", "too busy", "busy", "in a meeting", "not now", "im in a meeting"]):
#         return "no_time"
#     if any(k in t for k in ["already have help", "i have help", "we have help", "already have an assistant", "already have a va", "we already have"]):
#         return "already_help"
#     if any(k in t for k in ["no budget", "too expensive", "cant afford", "can't afford", "cost", "price"]):
#         return "no_budget"
#     if any(k in t for k in ["how much", "pricing", "price", "cost", "whats the cost", "what's the cost"]):
#         return "how_much"
#     if any(k in t for k in ["not interested", "no thanks", "not now", "im not interested", "i'm not interested"]):
#         return "not_interested"

#     return None


# # -----------------------------
# # Agent
# # -----------------------------
# class ScriptedMerideth(Agent):
#     def __init__(self) -> None:
#         super().__init__(instructions=SYSTEM_PROMPT)


# async def entrypoint(ctx: agents.JobContext):
#     await ctx.connect()

#     # Optimized VAD settings for better speech detection
#     vad = silero.VAD.load(
#         sample_rate=16000,
#         activation_threshold=0.85,  # Reduced from 0.92 to be more sensitive
#         min_speech_duration=0.25,   # Reduced to catch quick responses
#         min_silence_duration=0.5,   # Reduced to be more responsive
#         prefix_padding_duration=0.2, # Reduced padding
#     )

#     # ElevenLabs STT with correct sample rate
#     stt = elevenlabs.STT(
#         model_id="scribe_v2_realtime",
#         language_code="en",
#         sample_rate=16000,  # Changed from 18000 to 16000 (standard for ElevenLabs)
#         tag_audio_events=False,
#     )

#     # ElevenLabs TTS
#     tts = elevenlabs.TTS(
#         model="eleven_turbo_v2_5",
#         voice_id=os.getenv("ELEVEN_VOICE_ID", "bIHbv24MWmeRgasZH58o"),
#         streaming_latency=3,
#         chunk_length_schedule=[120, 160, 200, 240],
#         enable_logging=True,
#     )

#     session = AgentSession(
#         stt=stt,
#         tts=tts,
#         vad=vad,
#         userdata={
#             "state": "opening",
#             "q_idx": 0,
#             "tz": None,
#             "day_time": None,
#             "email": None,
#             "phone": None,
#             "name": None,
#         },
#     )

#     # Ensure background noise doesn't cut off TTS
#     speak_lock = asyncio.Lock()
#     async def say(text: str):
#         async with speak_lock:
#             print(f"AGENT: {text}")
#             await session.say(text, allow_interruptions=False)

#     # Activate noise cancellation BEFORE starting session
#     nc_plugin = noise_cancellation.BVC()
    
#     await session.start(
#         room=ctx.room,
#         agent=ScriptedMerideth(),
#         room_input_options=RoomInputOptions(
#             noise_cancellation=nc_plugin,
#             close_on_disconnect=False,
#         ),
#     )

#     print("Scripted mode: NO LLM. ElevenLabs STT + TTS.")
#     print("Noise cancellation: ACTIVE")
#     print("VAD settings: optimized for conversation")
#     await say(OPENING)

#     async def ask_repeat_same_state():
#         # This does NOT advance the script; it asks them to repeat cleanly.
#         await say("Sorry, I didn't catch that. Could you please repeat?")

#     @session.on("user_input_transcribed")
#     def on_user_input(e):
#         if not getattr(e, "is_final", False):
#             return
#         text = getattr(e, "transcript", "") or ""
#         text = clean_stt_output(text)
#         print(f"USER STT (FINAL): '{text}'")
        
#         # Debug: Show if text would be accepted
#         if not text:
#             print("DEBUG: Empty transcript")
#             return
            
#         if not acceptable_answer(text):
#             print(f"DEBUG: Rejected by acceptable_answer: '{text}'")
#             asyncio.create_task(ask_repeat_same_state())
#             return

#         asyncio.create_task(handle(text))

#     async def handle(user_text: str):
#         print(f"Processing: '{user_text}'")
        
#         # Global goodbye
#         if is_goodbye(user_text):
#             await say(GOODBYE)
#             return

#         # Global objections - check these FIRST
#         obj = detect_objection(user_text)
#         if obj:
#             print(f"Objection detected: {obj}")
            
#         if obj == "opt_out":
#             await say("Understood. I will remove you. Goodbye.")
#             return
#         if obj == "where_number":
#             await say(OBJ_WHERE_NUMBER)
#             return
#         if obj == "didnt_ask":
#             await say(OBJ_DIDNT_ASK)
#             return
#         if obj == "send_info":
#             session.userdata["state"] = "send_info_channel"
#             await say(OBJ_SEND_INFO)
#             return
#         if obj == "have_to_go":
#             session.userdata["state"] = "callback"
#             await say(OBJ_HAVE_TO_GO)
#             return
#         if obj == "maybe_later":
#             session.userdata["state"] = "callback"
#             await say(OBJ_MAYBE_LATER)
#             return
#         if obj == "no_time":
#             session.userdata["state"] = "tz"
#             await say(OBJ_NO_TIME)
#             return
#         if obj == "already_help":
#             await say(OBJ_ALREADY_HELP)
#             return
#         if obj == "no_budget":
#             await say(OBJ_NO_BUDGET)
#             return
#         if obj == "how_much":
#             session.userdata["state"] = "booking_ask"
#             await say(OBJ_HOW_MUCH)
#             return
#         if obj == "not_interested":
#             await say(OBJ_NOT_INTERESTED)
#             return

#         # Script flow
#         state = session.userdata["state"]
#         print(f"Current state: {state}")

#         if state == "opening":
#             session.userdata["state"] = "intro"
#             await say(INTRO_AND_Q)
#             return

#         if state == "intro":
#             choice = classify_support(user_text)
#             print(f"Support classification: {choice}")
#             session.userdata["state"] = "discovery"
#             if choice == "self":
#                 await say(DISCOVERY_SELF)
#             elif choice == "support":
#                 await say(DISCOVERY_SUPPORT)
#             else:
#                 await say(DISCOVERY_UNCLEAR)
#             return

#         if state == "discovery":
#             session.userdata["state"] = "qualifying"
#             session.userdata["q_idx"] = 0
#             await say(POSITIONING)
#             await asyncio.sleep(0.5)  # Small pause between statements
#             await say(QUALIFYING[0])
#             return

#         if state == "qualifying":
#             idx = session.userdata["q_idx"] + 1
#             if idx < len(QUALIFYING):
#                 session.userdata["q_idx"] = idx
#                 await say(QUALIFYING[idx])
#                 return
#             session.userdata["state"] = "booking_ask"
#             await say(BOOKING_ASK)
#             return

#         if state == "booking_ask":
#             if is_yes(user_text):
#                 session.userdata["state"] = "tz"
#                 await say(ASK_TZ)
#             else:
#                 # Return to discovery if they say no
#                 session.userdata["state"] = "discovery"
#                 await say("No problem. Would the bigger win be more time, or more leads?")
#             return

#         # Booking flow
#         if state == "tz":
#             session.userdata["tz"] = user_text.strip()
#             session.userdata["state"] = "day_time"
#             await say(ASK_DAY_TIME)
#             return

#         if state == "day_time":
#             session.userdata["day_time"] = user_text.strip()
#             session.userdata["state"] = "email"
#             await say(ASK_EMAIL)
#             return

#         if state == "email":
#             session.userdata["email"] = user_text.strip()
#             session.userdata["state"] = "phone"
#             await say(ASK_PHONE)
#             return

#         if state == "phone":
#             session.userdata["phone"] = user_text.strip()
#             session.userdata["state"] = "name"
#             await say(ASK_NAME)
#             return

#         if state == "name":
#             session.userdata["name"] = user_text.strip()
#             session.userdata["state"] = "booked"
#             await say(CONFIRM)
#             return

#         # Send info flow
#         if state == "send_info_channel":
#             t = normalize(user_text)
#             if "text" in t:
#                 session.userdata["state"] = "send_info_phone"
#                 await say("Sure. What is your best phone number?")
#             else:
#                 session.userdata["state"] = "send_info_email"
#                 await say("Sure. What is your best email?")
#             return

#         if state == "send_info_email":
#             session.userdata["email"] = user_text.strip()
#             session.userdata["state"] = "booking_ask"
#             await say("Thanks. I can also do a quick 15-minute Zoom. Open to that?")
#             return

#         if state == "send_info_phone":
#             session.userdata["phone"] = user_text.strip()
#             session.userdata["state"] = "booking_ask"
#             await say("Thanks. I can also do a quick 15-minute Zoom. Open to that?")
#             return

#         # Callback flow
#         if state == "callback":
#             await say(CALLBACK_Q)
#             session.userdata["state"] = "booked"
#             return

#         if state == "booked":
#             await say("Got it. Anything else before we wrap up?")
#             return

#         # Fallback - if we don't recognize the state or input
#         await ask_repeat_same_state()


# if __name__ == "__main__":
#     agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))









import os
import re
import asyncio
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import elevenlabs, noise_cancellation, silero

load_dotenv(".env")

# -----------------------------
# Prompt (kept for consistency)
# -----------------------------
SYSTEM_PROMPT = (
    "You are Merideth from NSOL BPO. You help realtors reclaim time using virtual assistants combined with AI automation "
    "for admin work, cold calling, lead follow-up, and social media.\n\n"
    "VOICE AND STYLE\n"
    "- Sound warm, professional, and human. Not robotic.\n"
    "- Use clear, simple English at a moderate pace.\n"
    "- Keep every message 1–2 short lines unless the user asks for more detail.\n"
    "- Mirror the prospect's mood.\n"
    "- No emojis or special symbols.\n\n"
    "TURN TAKING\n"
    "- Ask only one question at a time.\n"
    "- After a question, stop speaking.\n"
)

# -----------------------------
# TTS-friendly (ASCII) script
# -----------------------------
OPENING = "Hi, this is Merideth. How is your day going?"
INTRO_AND_Q = (
    "I am calling from NSOL BPO. We help realtors get time back with calling, lead follow-ups, admin, "
    "and social media using professionals plus AI automation. Are you handling most admin yourself, or do you have support?"
)

DISCOVERY_SELF = "What is eating most of your time right now?"
DISCOVERY_SUPPORT = "What tasks are you still managing yourself?"
DISCOVERY_UNCLEAR = "Would the bigger win be more time, or more leads?"

POSITIONING = "Got it. That is exactly where we help. We take those tasks off your plate so you can focus on closings."

QUALIFYING = [
    "About how many hours a week go to backend admin?",
    "How are you managing lead follow-up today?",
    "Have you had to turn down opportunities because you are swamped?",
    "If you got 20 hours back each week, what would you focus on?",
    "How satisfied are you with your social media results?",
]

BOOKING_ASK = "Open to a quick 15-minute Zoom overview to see if it fits?"
ASK_TZ = "What is your timezone or location?"
ASK_DAY_TIME = "What day and hour works best for a quick Zoom? Please say the hour only."
ASK_EMAIL = "What is your best email?"
ASK_PHONE = "Best phone number?"
ASK_NAME = "And your full name?"
CONFIRM = "Excellent. You are all set. You will get a confirmation shortly. Anything else before we wrap up?"

GOODBYE = "Thanks for your time. Wishing you amazing success. Talk soon. Goodbye."

# -----------------------------
# Objections (ASCII)
# -----------------------------
OBJ_NOT_INTERESTED = "I understand. Is it timing, or are you not seeing the value in freeing up time?"
OBJ_NO_BUDGET = "Totally fair. The overview is free, and most find the time saved pays for itself. Open to a quick look?"
OBJ_ALREADY_HELP = "Makes sense. Many clients had support too, but there were still gaps. Open to seeing what we would take off your plate?"
OBJ_NO_TIME = "That is exactly why this works. Fifteen minutes could free up hours. What is your timezone or location?"
OBJ_HOW_MUCH = "Pricing depends on what you need. Which matters most right now: calling, admin, lead follow-up, or social media?"
OBJ_HAVE_TO_GO = "Before you go, if I could help you get 20 hours back weekly, is that worth a 15-minute overview?"
OBJ_MAYBE_LATER = "I get it. Most people delay because they are busy. Should I send a quick summary and follow up on a specific day?"
OBJ_SEND_INFO = "Of course. Quick question. Text or email?"
OBJ_WHERE_NUMBER = "From public real estate directories and broker listings. If you prefer, I can remove you."
OBJ_DIDNT_ASK = "You're right. We reached out because we help agents focus on closing. Open to hearing the quick version?"
CALLBACK_Q = "No problem. When is better, later today or tomorrow?"

# -----------------------------
# Enhanced noise + acceptance gate
# -----------------------------
FILLER_ONE_WORD = {
    "so", "right", "okay", "ok", "um", "uh", "hmm", "yes", "yeah", "no", "yup", "yep", "nope",
    "like", "well", "actually", "basically", "literally", "seriously"
}

# Expanded noise patterns
NOISE_PAT = re.compile(
    r"^\s*\(.*\)\s*$|"
    r"microphone|interference|soft music|music|noise|static|drowns out|background|"
    r"click|pop|cough|sneeze|breath|inhale|exhale|sigh|"
    r"hiss|hum|buzz|rumble|echo|feedback|"
    r"^(ah+|uh+|um+|er+|hm+)\s*$|"
    r"^\s*(thanks|thank you|bye|goodbye)\s*$",  # Common endings that might be misheard
    re.I
)

def normalize(text: str) -> str:
    """Clean and normalize text for comparison"""
    if not text:
        return ""
    # Remove extra spaces, convert to lowercase
    text = re.sub(r"\s+", " ", text.strip()).lower()
    # Remove common punctuation for matching
    text = re.sub(r"[^\w\s]", "", text)
    return text

def clean_stt_output(text: str) -> str:
    """Clean STT output before processing"""
    if not text:
        return ""
    
    # Remove common STT artifacts
    text = re.sub(r"\[.*?\]|\(.*?\)", "", text)  # Remove anything in brackets/parentheses
    text = re.sub(r"\b(um|uh|ah|er|hm)+\b", "", text, flags=re.I)  # Remove filler words
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    
    return text

def acceptable_answer(text: str) -> bool:
    """
    Accept only answers that look like real speech.
    This prevents background noise -> random words advancing the script.
    """
    t = clean_stt_output(text)
    if not t:
        return False

    # Parenthesized audio events or common noise tags
    if NOISE_PAT.search(t):
        print(f"Rejected as noise: {t}")
        return False

    low = normalize(t)
    words = re.findall(r"[a-zA-Z']+", low)

    if len(words) == 0:
        return False

    # single filler word -> reject (does not advance)
    if len(words) == 1 and words[0] in FILLER_ONE_WORD:
        print(f"Rejected as single filler: {words[0]}")
        return False

    # require enough letters to reduce false triggers
    if sum(ch.isalpha() for ch in t) < 3:  # Reduced from 4 to 3 for short answers
        print(f"Rejected as too short: {t}")
        return False

    # reject "word salad" that often comes from noise
    if len(words) >= 4 and sum(len(w) <= 2 for w in words) >= 3:
        print(f"Rejected as word salad: {t}")
        return False

    # Reject if it's just repeating what we just said
    common_phrases = {
        "how is your day going", "i am calling from", "what is your timezone",
        "what is your email", "what is your phone number", "what is your name"
    }
    if any(phrase in t for phrase in common_phrases if len(t) > 10):
        print(f"Rejected as echo: {t}")
        return False

    return True

def classify_support(text: str) -> str:
    t = normalize(text)
    if any(k in t for k in ["myself", "by myself", "just me", "me", "alone", "i do", "i handle", "no support", "no help"]):
        return "self"
    if any(k in t for k in ["assistant", "team", "support", "staff", "admin", "va", "employee", "someone", "we have"]):
        return "support"
    return "unclear"

def is_yes(text: str) -> bool:
    t = normalize(text)
    return any(k in t for k in ["yes", "yeah", "yep", "yup", "sure", "ok", "okay", "alright", "sounds good", "absolutely", "why not"])

def is_goodbye(text: str) -> bool:
    t = normalize(text)
    return any(k in t for k in ["bye", "goodbye", "thanks bye", "see you", "talk later", "later", "have a good day"])

def is_opt_out(text: str) -> bool:
    t = normalize(text)
    return any(k in t for k in ["remove me", "do not call", "don't call", "stop calling", "unsubscribe", "take me off", "dont call"])

def detect_objection(text: str) -> str | None:
    t = normalize(text)

    if is_opt_out(t):
        return "opt_out"
    if "where" in t and "number" in t:
        return "where_number"
    if any(k in t for k in ["didnt ask", "didnt ask", "why calling", "why are you calling", "i did not ask", "who gave you"]):
        return "didnt_ask"
    if any(k in t for k in ["send info", "send me", "email me", "text me", "just send", "can you send"]):
        return "send_info"
    if any(k in t for k in ["have to go", "gotta go", "cant talk", "can't talk", "busy now", "im busy", "i'm busy"]):
        return "have_to_go"
    if any(k in t for k in ["maybe later", "later", "next week", "another time", "call back later"]):
        return "maybe_later"
    if any(k in t for k in ["no time", "too busy", "busy", "in a meeting", "not now", "im in a meeting"]):
        return "no_time"
    if any(k in t for k in ["already have help", "i have help", "we have help", "already have an assistant", "already have a va", "we already have"]):
        return "already_help"
    if any(k in t for k in ["no budget", "too expensive", "cant afford", "can't afford", "cost", "price"]):
        return "no_budget"
    if any(k in t for k in ["how much", "pricing", "price", "cost", "whats the cost", "what's the cost"]):
        return "how_much"
    if any(k in t for k in ["not interested", "no thanks", "not now", "im not interested", "i'm not interested"]):
        return "not_interested"

    return None


# -----------------------------
# Agent
# -----------------------------
class ScriptedMerideth(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=SYSTEM_PROMPT)


async def entrypoint(ctx: agents.JobContext):
    await ctx.connect()

    # Optimized VAD settings for better speech detection
    vad = silero.VAD.load(
        sample_rate=16000,
        activation_threshold=0.85,  # Reduced from 0.92 to be more sensitive
        min_speech_duration=0.25,   # Reduced to catch quick responses
        min_silence_duration=0.5,   # Reduced to be more responsive
        prefix_padding_duration=0.2, # Reduced padding
    )

    # ElevenLabs STT with correct sample rate
    stt = elevenlabs.STT(
        model_id="scribe_v2_realtime",
        language_code="en",
        sample_rate=16000,  # Changed from 18000 to 16000 (standard for ElevenLabs)
        tag_audio_events=False,
    )

    # ElevenLabs TTS
    tts = elevenlabs.TTS(
        model="eleven_turbo_v2_5",
        voice_id=os.getenv("ELEVEN_VOICE_ID", "bIHbv24MWmeRgasZH58o"),
        streaming_latency=3,
        chunk_length_schedule=[120, 160, 200, 240],
        enable_logging=True,
    )

    session = AgentSession(
        stt=stt,
        tts=tts,
        vad=vad,
        userdata={
            "state": "opening",
            "q_idx": 0,
            "tz": None,
            "day_time": None,
            "email": None,
            "phone": None,
            "name": None,
        },
    )

    # Ensure background noise doesn't cut off TTS
    speak_lock = asyncio.Lock()
    async def say(text: str):
        async with speak_lock:
            print(f"AGENT: {text}")
            await session.say(text, allow_interruptions=False)

    # Activate noise cancellation BEFORE starting session
    nc_plugin = noise_cancellation.BVC()
    
    await session.start(
        room=ctx.room,
        agent=ScriptedMerideth(),
        room_input_options=RoomInputOptions(
            noise_cancellation=nc_plugin,
            close_on_disconnect=False,
        ),
    )

    print("Scripted mode: NO LLM. ElevenLabs STT + TTS.")
    print("Noise cancellation: ACTIVE")
    print("VAD settings: optimized for conversation")
    await say(OPENING)

    async def ask_repeat_same_state():
        # This does NOT advance the script; it asks them to repeat cleanly.
        await say("Sorry, I didn't catch that. Could you please repeat?")

    @session.on("user_input_transcribed")
    def on_user_input(e):
        if not getattr(e, "is_final", False):
            return
        text = getattr(e, "transcript", "") or ""
        text = clean_stt_output(text)
        print(f"USER STT (FINAL): '{text}'")
        
        # Debug: Show if text would be accepted
        if not text:
            print("DEBUG: Empty transcript")
            return
            
        if not acceptable_answer(text):
            print(f"DEBUG: Rejected by acceptable_answer: '{text}'")
            asyncio.create_task(ask_repeat_same_state())
            return

        asyncio.create_task(handle(text))

    async def handle(user_text: str):
        print(f"Processing: '{user_text}'")
        
        # Global goodbye
        if is_goodbye(user_text):
            await say(GOODBYE)
            return

        # Global objections - check these FIRST
        obj = detect_objection(user_text)
        if obj:
            print(f"Objection detected: {obj}")
            
        if obj == "opt_out":
            await say("Understood. I will remove you. Goodbye.")
            return
        if obj == "where_number":
            await say(OBJ_WHERE_NUMBER)
            return
        if obj == "didnt_ask":
            await say(OBJ_DIDNT_ASK)
            return
        if obj == "send_info":
            session.userdata["state"] = "send_info_channel"
            await say(OBJ_SEND_INFO)
            return
        if obj == "have_to_go":
            session.userdata["state"] = "callback"
            await say(OBJ_HAVE_TO_GO)
            return
        if obj == "maybe_later":
            session.userdata["state"] = "callback"
            await say(OBJ_MAYBE_LATER)
            return
        if obj == "no_time":
            session.userdata["state"] = "tz"
            await say(OBJ_NO_TIME)
            return
        if obj == "already_help":
            await say(OBJ_ALREADY_HELP)
            return
        if obj == "no_budget":
            await say(OBJ_NO_BUDGET)
            return
        if obj == "how_much":
            session.userdata["state"] = "booking_ask"
            await say(OBJ_HOW_MUCH)
            return
        if obj == "not_interested":
            await say(OBJ_NOT_INTERESTED)
            return

        # Script flow
        state = session.userdata["state"]
        print(f"Current state: {state}")

        if state == "opening":
            session.userdata["state"] = "intro"
            await say(INTRO_AND_Q)
            return

        if state == "intro":
            choice = classify_support(user_text)
            print(f"Support classification: {choice}")
            session.userdata["state"] = "discovery"
            if choice == "self":
                await say(DISCOVERY_SELF)
            elif choice == "support":
                await say(DISCOVERY_SUPPORT)
            else:
                await say(DISCOVERY_UNCLEAR)
            return

        if state == "discovery":
            session.userdata["state"] = "qualifying"
            session.userdata["q_idx"] = 0
            await say(POSITIONING)
            await asyncio.sleep(0.5)  # Small pause between statements
            await say(QUALIFYING[0])
            return

        if state == "qualifying":
            idx = session.userdata["q_idx"] + 1
            if idx < len(QUALIFYING):
                session.userdata["q_idx"] = idx
                await say(QUALIFYING[idx])
                return
            session.userdata["state"] = "booking_ask"
            await say(BOOKING_ASK)
            return

        if state == "booking_ask":
            if is_yes(user_text):
                session.userdata["state"] = "tz"
                await say(ASK_TZ)
            else:
                # Return to discovery if they say no
                session.userdata["state"] = "discovery"
                await say("No problem. Would the bigger win be more time, or more leads?")
            return

        # Booking flow
        if state == "tz":
            session.userdata["tz"] = user_text.strip()
            session.userdata["state"] = "day_time"
            await say(ASK_DAY_TIME)
            return

        if state == "day_time":
            session.userdata["day_time"] = user_text.strip()
            session.userdata["state"] = "email"
            await say(ASK_EMAIL)
            return

        if state == "email":
            session.userdata["email"] = user_text.strip()
            session.userdata["state"] = "phone"
            await say(ASK_PHONE)
            return

        if state == "phone":
            session.userdata["phone"] = user_text.strip()
            session.userdata["state"] = "name"
            await say(ASK_NAME)
            return

        if state == "name":
            session.userdata["name"] = user_text.strip()
            session.userdata["state"] = "booked"
            await say(CONFIRM)
            return

        # Send info flow
        if state == "send_info_channel":
            t = normalize(user_text)
            if "text" in t:
                session.userdata["state"] = "send_info_phone"
                await say("Sure. What is your best phone number?")
            else:
                session.userdata["state"] = "send_info_email"
                await say("Sure. What is your best email?")
            return

        if state == "send_info_email":
            session.userdata["email"] = user_text.strip()
            session.userdata["state"] = "booking_ask"
            await say("Thanks. I can also do a quick 15-minute Zoom. Open to that?")
            return

        if state == "send_info_phone":
            session.userdata["phone"] = user_text.strip()
            session.userdata["state"] = "booking_ask"
            await say("Thanks. I can also do a quick 15-minute Zoom. Open to that?")
            return

        # Callback flow
        if state == "callback":
            await say(CALLBACK_Q)
            session.userdata["state"] = "booked"
            return

        if state == "booked":
            await say("Got it. Anything else before we wrap up?")
            return

        # Fallback - if we don't recognize the state or input
        await ask_repeat_same_state()


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))






    