import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] %(pathname)s:%(funcName)s:%(lineno)d - %(message)s",
    datefmt="%m-%d %H:%M",
    filename="spam.log",
    filemode="a",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)


grey = "\x1b[38;20m"
yellow = "\x1b[33;20m"
red = "\x1b[31;20m"
bold_red = "\x1b[31;1m"
reset = "\x1b[0m"


formatter = logging.Formatter(
    f"[%(asctime)s] {yellow}[%(levelname)s]{reset} %(pathname)s:%(funcName)s:%(lineno)d - {yellow}%(message)s{reset}"
)


console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

logger = logging.getLogger("app")
