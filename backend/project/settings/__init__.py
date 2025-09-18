from .config import env_setting

if env_setting.DEBUG:
    from .dev import *  # noqa: F403
else:
    from .prod import *  # noqa: F403
