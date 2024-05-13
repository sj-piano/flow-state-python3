from . import const, utils

env_var_names_string = """
    ENVIRONMENT,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
"""

# Load env vars from environment
env, env_var_names = utils.env_vars.load_env_vars(env_var_names_string)

# Set env vars as module-level variables that can be imported from this module.
ENVIRONMENT, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD = (getattr(env, attr) for attr in env_var_names)


# Validation
if env.ENVIRONMENT not in const.Environment.values:
    msg = f"env var ENVIRONMENT value ('{env.ENVIRONMENT}') not in permitted values ({const.Environment.values})."
    raise ValueError(msg)
