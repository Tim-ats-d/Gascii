#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  gascii.py
#  A graphic and interactive table of printable ASCII characters.
#
#  Copyright 2020 Timéo Arnouts <tim.arnouts@protonmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import curses
import curses.textpad
import os
import unicodedata


COLS, ROWS = os.get_terminal_size()
ASCII_CHARS = [chr(char) for char in range(32, 127)]


def cutting_list(list_: list, part_size: int):
    """Yield a sub-list of size part_size of the given list."""
    for part in range(0, len(list_), part_size):
        yield list_[part:part + part_size]


def displays_table(stdscr, pos_x: int, pos_y: int, chars_list: list):
    """Displays each character in the list of given characters spaced from each other and separated
    by a blank line.
    """
    chars_list = cutting_list(ASCII_CHARS, 16)

    for y, chars in enumerate(chars_list):
        for x, char in enumerate(chars):
            stdscr.addstr(pos_y + y*2, pos_x + x*2, "%s " % char)


def cursor_position(stdscr, pos_x: int, pos_y: int, x_max: int, y_max: int):
    """Manages the movements of the cursor so that it can be overtaken in the zone
    (pos_x;pos_y);(pos_x + x_max;pos_y + y_max) and yields the identifier of the character below it.
    """
    key = 0
    cursor_x, cursor_y = pos_x, pos_y

    while key != ord("q"):
        if key == curses.KEY_UP:
            cursor_y -= 2
        elif key == curses.KEY_DOWN:
            cursor_y += 2
        elif key == curses.KEY_LEFT:
            cursor_x -= 2
        elif key == curses.KEY_RIGHT:
            cursor_x += 2
        elif key == 339:  # page ▲ key.
            cursor_y = pos_y
        elif key == 338:  # page ▼ key.
            cursor_y = pos_y + y_max
        elif key == 262:  # begin ◄ key.
            cursor_x = pos_x
        elif key == 360:  # end ► key.
            cursor_x = pos_x + x_max

        cursor_x = max(pos_x, cursor_x)
        cursor_x = min(pos_x + 30, cursor_x)

        cursor_y = max(pos_y, cursor_y)
        cursor_y = min(pos_y + 10, cursor_y)

        yield stdscr.inch(cursor_y, cursor_x)

        stdscr.move(cursor_y, cursor_x)

        key = stdscr.getch()
        stdscr.refresh()


def character_indications(stdscr, pos_x: int, pos_y: int, char: int):
    """Displays an information panel on the given character identifier. The information panel
    contains title, description, exit indications and character identifier given in binary, octal,
    decimal and hexadecimal format.
    """
    title = "ASCII character table"
    description = "This table contains the 95 ASCII printable character."
    character_line = "Char   Character name"
    conversion_line = "Bin       Oct   Dec   Hex"
    exit_indication = "Press q to quit."

    stdscr.addstr(pos_y + 1, pos_x, title.center(pos_x - 7), curses.A_BOLD)
    stdscr.addstr(pos_y + 4, pos_x, description)

    stdscr.addstr(pos_y + 6, pos_x, character_line)
    stdscr.addstr(pos_y + 8, pos_x, chr(char))
    stdscr.addstr(pos_y + 8, pos_x + 7, "%s" % unicodedata.name(chr(char)))

    stdscr.addstr(pos_y + 10, pos_x, conversion_line)
    stdscr.addstr(pos_y + 12, pos_x, str(bin(char)[2:]))
    stdscr.addstr(pos_y + 12, pos_x + 10, str(oct(char)[2:]))
    stdscr.addstr(pos_y + 12, pos_x + 16, str(char))
    stdscr.addstr(pos_y + 12, pos_x + 22, str(hex(char)[2:]))

    stdscr.addstr(pos_y + 15, pos_x, exit_indication)


def embed_window(stdscr):
    """Displays borders on the terminal and a rectangle that frames the character table."""
    stdscr.box()
    curses.textpad.rectangle(stdscr, 2, 13, 16, 50)


def main(stdscr):
    """curses rendering."""
    char_table_pos_x, char_table_pos_y = COLS//2//3 - 6, 4
    interface_pos_x, interface_pos_y = COLS//2, 0

    for char in cursor_position(stdscr, char_table_pos_x, char_table_pos_y, 30, 10):
        stdscr.clear()
        displays_table(stdscr, char_table_pos_x, char_table_pos_y, ASCII_CHARS)
        embed_window(stdscr)
        character_indications(stdscr, interface_pos_x, interface_pos_y, char)
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
