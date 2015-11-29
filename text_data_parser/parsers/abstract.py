##
#     Project: Text Data Parser
# Description: View text data files with definitions.
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2015 Fabio Castelli
#     License: GPL-2+
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 2 of the License, or (at your option)
#  any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#  You should have received a copy of the GNU General Public License along
#  with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA
##

import chardet

MAX_FILE_SIZE = 1 * 1024 * 1024


class DataParserAbstract(object):
    def __init__(self):
        self.data_file = None
        self.values = []

    def load_from_file(self, fields, file_source):
        """Clear the previous data and reload from the source file"""
        self.values = []
        self.data_file = file_source
        with open(self.data_file, 'rb') as text_file:
            buffer = text_file.read(MAX_FILE_SIZE)
            # Guess the file encoding
            try:
                self.encoding = chardet.detect(buffer)['encoding']
            except:
                self.encoding = None
            if not self.encoding:
                print 'warning: unknown encoding, will fallback to utf-8'
                self.encoding = 'utf-8'
            text_file.close()

    def __iter__(self):
        """Iterate over the values"""
        for value in self.values:
            yield value

    def __getitem__(self, index):
        return self.values[index]

    def __len__(self):
        return len(self.values)
