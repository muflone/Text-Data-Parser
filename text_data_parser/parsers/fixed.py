##
#     Project: Text Data Parser
# Description: View text data files with definitions.
#      Author: Fabio Castelli (Muflone) <muflone@vbsimple.net>
#   Copyright: 2016 Fabio Castelli
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

from .abstract import DataParserAbstract

class DataParserFixed(DataParserAbstract):
  def __init__(self):
    super(self.__class__, self).__init__()

  def load_from_file(self, fields, file_data):
    super(self.__class__, self).load_from_file(fields, file_data)
    with open(file_data, 'r') as f:
      for s_line in f:
        # Strip invalid characters
        s_line = s_line.replace('\r', '')
        s_line = s_line.replace('\n', '')
        values = {}
        for field in fields:
          values[field.name] = s_line[field.start - 1:field.end]
        self.values.append(values)
      f.close()
