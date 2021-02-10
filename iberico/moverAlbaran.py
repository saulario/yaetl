#!/usr/bin/python3

import argparse
import logging

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utilidad para mover albaranes entre rutas")
    parser.add_argument("-s", "--site", action="store", type=int, choices=(1,3), required=True, dest="site")


    args = parser.parse_args()
