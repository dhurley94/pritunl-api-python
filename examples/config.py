from pritunl_api import *

import os

pritunl = Pritunl(url=os.getenv("PRITUNL_BASE_URL", "https://yoursite.com"),
                  token="PRITUNL_API_TOKEN",
                  secret="PRITUNL_API_SECRET")
