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

import os.path
from xdg import BaseDirectory

# Application constants
APP_NAME = 'Text Data Parser'
APP_VERSION = '0.1.0'
APP_DESCRIPTION = 'View text data files with definitions'
APP_ID = 'textdataparser.muflone.com'
APP_URL = 'http://www.muflone.com/textdataparser/'
APP_AUTHOR = 'Fabio Castelli'
APP_AUTHOR_EMAIL = 'muflone@vbsimple.net'
APP_COPYRIGHT = 'Copyright 2015 %s' % APP_AUTHOR
# Other constants
DOMAIN_NAME = 'textdataparser'

# Paths constants
DIR_PREFIX = '.'
DIR_LOCALE = os.path.join(DIR_PREFIX, 'locale')
# Set the paths for the folders
DIR_DATA = os.path.join(DIR_PREFIX, 'data')
DIR_UI = os.path.join(DIR_PREFIX, 'ui')
DIR_SETTINGS = BaseDirectory.save_config_path(DOMAIN_NAME)
# Set the paths for the UI files
FILE_UI_MAIN = os.path.join(DIR_UI, 'main.glade')
FILE_UI_APPMENU = os.path.join(DIR_UI, 'appmenu.ui')
# Set the paths for the data files
FILE_ICON = os.path.join(DIR_DATA, 'textdataparsers.png')
# Set the paths for configuration files
FILE_SETTINGS_NEW = os.path.join(DIR_SETTINGS, 'settings.conf')
