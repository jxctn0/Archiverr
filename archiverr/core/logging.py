import logging


FORMATTING = {
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
    "END": "\033[0m",
}
COLORS = {
    "LIGHT":{
        "BLACK": "\033[90m",
        "RED": "\033[91m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "BLUE": "\033[94m",
        "MAGENTA": "\033[95m",
        "CYAN": "\033[96m",
        "WHITE": "\033[97m",
    },
    "DARK":{
        "BLACK": "\033[30m",
        "RED": "\033[31m",
        "GREEN": "\033[32m",
        "YELLOW": "\033[33m",
        "BLUE": "\033[34m",
        "MAGENTA": "\033[35m",
        "CYAN": "\033[36m",
        "WHITE": "\033[37m",
    },
    "BACKGROUND":{
        "BLACK": "\033[40m",
        "RED": "\033[41m",
        "GREEN": "\033[42m",
        "YELLOW": "\033[43m",
        "BLUE": "\033[44m",
        "MAGENTA": "\033[45m",
        "CYAN": "\033[46m",
        "WHITE": "\033[47m"
    }
}

def color_text(text, color):
    if color is None:
        return text
    elif color.upper() in COLORS["LIGHT"]:
        return f"{COLORS['LIGHT'].get(color.upper(), '')}{text}{FORMATTING['END']}"
    elif int(color) in range(256):
        return f"\033[38;5;{color}m{text}{FORMATTING['END']}"
    else:
        return text

    # Support for ansi codes directly passed as color: color_text(text, int(color))
    # Based on: for code in {0..255}; do echo -e "\e[38;5;${code}m"'\\e[38;5;'"$code"m"\e[0m"; done
    
def format_text(text, *formats):
    format_sequence = "".join([FORMATTING.get(fmt.upper(), "") for fmt in formats])
    return f"{format_sequence}{text}{FORMATTING['END']}"



C = {
    "D": COLORS["LIGHT"]["CYAN"],
    "I": COLORS["LIGHT"]["GREEN"],
    "W": COLORS["LIGHT"]["YELLOW"],
    "E": COLORS["LIGHT"]["RED"],
    "C": COLORS["LIGHT"]["MAGENTA"],
    "R": FORMATTING["END"]
}




def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

def log_debug(message):
    formatted = f"{C['D']}[DEBUG] {message}{C['R']}"
    logging.debug(formatted)
    return formatted

def log_info(message):
    formatted = f"{C['I']}[INFO] {message}{C['R']}"
    logging.info(formatted)
    return formatted

def log_warning(message):
    formatted = f"{C['W']}[WARNING] {message}{C['R']}"
    logging.warning(formatted)
    return formatted

def log_error(message):
    formatted = f"{C['E']}[ERROR] {message}{C['R']}"
    logging.error(formatted)
    return formatted

def log_critical(message):
    formatted = f"{C['C']}[CRITICAL] {message}{C['R']}"
    logging.critical(formatted)
    return formatted

def log_data(data, level="info"):
    # Log structured data (like dictionaries or lists) in a pretty-printed format with color-coding based on the log level
    import json
    message = json.dumps(data, indent=4, default=str)
    return log(message, level)

def log(message, level="info", noprint=False): 
    # General log function that takes a message and a level and logs it using the appropriate log function based on the level - this is a convenience function to allow logging with color-coded output without having to call the specific log functions directly
    level = level.lower()[0] # Get the first letter of the level to determine which log function to call
    if level == "d":
        if noprint:
            return log_debug(message)
        else:
            print(log_debug(message))
    elif level == "i":
        if noprint:
            return log_info(message)
        else:
            print(log_info(message))
    elif level == "w":
        if noprint:
            return log_warning(message)
        else:
            print(log_warning(message))
    elif level == "e":
        if noprint:
            return log_error(message)
        else:
            print(log_error(message))
    elif level == "c":
        if noprint:
            return log_critical(message)
        else:
            print(log_critical(message))
    else:
        formatted = f"{C['I']}[INFO] {message}{C['R']}"
        logging.info(formatted)
        return formatted

