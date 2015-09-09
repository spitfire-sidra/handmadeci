# -*- coding: utf-8 -*-
import os

from webhook import app
from webhook import config

if __name__ == "__main__":
    port = int(os.environ.get('PORT', config.PORT_NUMBER))
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
