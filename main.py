# gascii.py
# A graphic and interactive table of printable ASCII characters.
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
from typing import NoReturn
import unicodedata


ConsoleEffect = NoReturn

ASCII_CHARS = [chr(char) for char in range(32, 127)]

TITLE = "ASCII character table"
DESCRIPTION = "The 95 ASCII printable characters."
EXIT_INDICATION = "Press q to quit."


def make_chunk(iterable: list,
               chunk_length: int) -> list:
    """Yield chunk of given iterator separated into chunk_length bundles."""
    for chunk in range(0, len(iterable), chunk_length):
        yield iterable[chunk:chunk + chunk_length]


def displays_table(stdscr,
                   pos_x: int,
                   pos_y: int,
                   chars_list: list) -> ConsoleEffect:
    """Displays each character in the list of given characters spaced from each
    other and separated by a blank line.
    """
    chars_list = make_chunk(ASCII_CHARS, 16)

    for y, chars in enumerate(chars_list):
        for x, char in enumerate(chars):
            stdscr.addstr(pos_y + y*2,
                          pos_x + x*2,
                          char + " ")


def cursor_position(stdscr,
                    pos_x: int,
                    pos_y: int,
                    x_max: int,
                    y_max: int) -> str:
    """Manages the movements of the cursor so that it can be overtaken in the
    zone (pos_x;pos_y);(pos_x + x_max;pos_y + y_max) and yields the identifier
    of the character below it.
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
        elif key == 339:  # Page ▲ key.
            cursor_y = pos_y
        elif key == 338:  # Page ▼ key.
            cursor_y = pos_y + y_max
        elif key == 262:  # Begin ◄ key.
            cursor_x = pos_x
        elif key == 360:  # End ► key.
            cursor_x = pos_x + x_max

        cursor_x = max(pos_x, cursor_x)
        cursor_x = min(pos_x + x_max, cursor_x)

        cursor_y = max(pos_y, cursor_y)
        cursor_y = min(pos_y + y_max, cursor_y)

        yield stdscr.inch(cursor_y, cursor_x)

        stdscr.move(cursor_y, cursor_x)

        key = stdscr.getch()
        stdscr.refresh()


def char_indications(stdscr,
                     pos_x: int,
                     pos_y: int,
                     char_code: int) -> ConsoleEffect:
    """Displays an information panel on the given character identifier.

    The information panel contains title, description, exit indications and
    character identifier given in binary, octal, decimal and hexadecimal
    format.
    """
    char = chr(char_code)

    char_line = "Char: " + char
    char_name = "Name: " + unicodedata.name(char)

    stdscr.addstr(pos_y + 1, pos_x, TITLE.center(pos_x - 7), curses.A_BOLD)
    stdscr.addstr(pos_y + 3, pos_x, DESCRIPTION)

    stdscr.addstr(pos_y + 5, pos_x, char_line)
    stdscr.addstr(pos_y + 6, pos_x, char_name)

    stdscr.addstr(pos_y + 8, pos_x, "Bin: {0:b}".format(char_code))
    stdscr.addstr(pos_y + 9, pos_x, "Oct: %o" % char_code)
    stdscr.addstr(pos_y + 10, pos_x, "Dec: %s" % char_code)
    stdscr.addstr(pos_y + 11, pos_x, "Hex: %x" % char_code)

    stdscr.addstr(pos_y + 13, pos_x, EXIT_INDICATION)


def mainloop(stdscr) -> ConsoleEffect:
    """curses rendering."""
    rows, cols = stdscr.getmaxyx()

    char_table_pos_x, char_table_pos_y = (4, 2)
    interface_pos = (cols//2, 0)

    cursor_positions = cursor_position(stdscr,
                                       char_table_pos_x,
                                       char_table_pos_y,
                                       30, 10)

    for char in cursor_positions:
        stdscr.clear()
        stdscr.box()

        curses.textpad.rectangle(stdscr,
                                 char_table_pos_y - 1,
                                 char_table_pos_x - 2,
                                 13, 36)

        displays_table(stdscr,
                       char_table_pos_x,
                       char_table_pos_y,
                       ASCII_CHARS)
        char_indications(stdscr,
                         *interface_pos,
                         char)

        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(mainloop)
