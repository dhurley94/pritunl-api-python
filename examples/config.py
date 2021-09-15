from pritunl_api import *

import os

pritunl = Pritunl(url=os.getenv("PRITUNL_BASE_URL", "https://yoursite.com"),
                  token=os.getenv("PRITUNL_API_TOKEN", "<your api token>"),
                  secret=os.getenv("PRITUNL_API_SECRET", "<your api secret>"))
