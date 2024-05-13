import os
from typing import List


class Object(object):
    pass


def load_env_vars(env_var_names_string: str) -> Object:
    # We expect a multiline string with the format:
    # env_var_name1,
    # env_var_name2,
    # etc.
    names = env_var_names_string.split('\n')
    names = [x.strip() for x in names if x.strip()]
    names = [x.replace(',', '') for x in names]
    # Confirm that all names are alphanumeric.
    for name in names:
        if not name.replace('_', '').isalnum():
            raise ValueError(f"Env var name '{name}' is not alphanumeric with optional underscores.")
    return load_env_vars_from_environment(names), names


def load_env_vars_from_environment(env_var_names: List[str]) -> Object:
    possible_empty_vars = ['REDIS_PASSWORD']
    missing_vars = []
    for name in env_var_names:
        if name not in os.environ:
            missing_vars.append(name)
        elif os.environ[name] == '':
            if name not in possible_empty_vars:
                missing_vars.append(name)
    if missing_vars:
        raise ValueError(f'Missing env vars in environment: {missing_vars}')
    env = Object()
    for name in env_var_names:
        setattr(env, name, os.environ[name])
    return env
