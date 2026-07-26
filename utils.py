import datetime


def get_timestamp():
    return datetime.datetime.now().strftime("%I:%M %p")


def export_chat(messages):
    conversation = ""

    for msg in messages:
        conversation += f"{msg['role'].upper()}:\n"
        conversation += msg["content"]
        conversation += "\n\n"

    return conversation