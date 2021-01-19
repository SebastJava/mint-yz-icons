#!/usr/bin/python3
import os
import subprocess
import sys

colors = ["Aqua", "Blue", "BlueDeep", "green", "Grey", "MintSoda", "MintSoft", "Orange", "Pink", "Purple", "PurpleDeep", "Red", "Yellow"]
sizes = ["16", "22", "24", "32", "48", "64", "96", "128"]


def generate_color(color):
    source = "places/" + color + ".svg"
    if color == "green":
        theme_dir = "../usr/share/icons/Mint-Yz-Old"
    else:
        theme_dir = "../usr/share/icons/Mint-Yz-%s" % color
    os.system("mkdir -p %s" % theme_dir)

    for size in sizes:
        icon_dir = os.path.join(theme_dir, "places", size)
        icon_dir_2x = os.path.join(theme_dir, "places", size + "@2x")
        os.system("mkdir -p %s" % icon_dir)
        os.system("mkdir -p %s" % icon_dir_2x)
        names = subprocess.check_output("inkscape -S %s | grep -E \"_%s\" | sed 's/\,.*$//'" % (source, size), shell=True).decode("UTF-8")
        for name in names.split("\n"):
            if "_" in name:
                icon_name = name.replace("_%s" % size, "")
                icon_path = os.path.join(icon_dir, icon_name + ".png")
                print("Rendering %s" % icon_path)
                os.system("inkscape --export-id=%s \
                               --export-id-only \
                               --export-filename=%s %s >/dev/null \
                     && optipng -o7 --quiet %s" % (name, icon_path, source, icon_path))

                icon_path = os.path.join(icon_dir_2x, icon_name + ".png")
                print("Rendering %s" % icon_path)
                os.system("inkscape --export-id=%s \
                               --export-id-only \
                               --export-dpi=192 \
                               --export-filename=%s %s >/dev/null \
                     && optipng -o7 --quiet %s" % (name, icon_path, source, icon_path))

def parse_arg(arg):
    if arg == "All":
        for color in colors:
            generate_color(color)
    else:
        generate_color(arg)

def usage():
    print ("Usage: render_places.py COLOR")
    print ("COLOR can be 'All' or one of these:")
    for color in colors:
        print ("    %s" % color)
    sys.exit(1)

if len(sys.argv) != 2:
    usage()
else:
    parse_arg(sys.argv[1])