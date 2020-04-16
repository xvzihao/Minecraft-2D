from datetime import datetime


def info(msg: str):
    print(f"[{str(datetime.now())}/INFO] {msg}")


def warn(msg: str):
    print(f"[{str(datetime.now())}/WARN] {msg}")


def err(msg: str):
    print(f"[{str(datetime.now())}/ERR] {msg}")
