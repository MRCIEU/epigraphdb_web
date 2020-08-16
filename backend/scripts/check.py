from epigraphdb_common_utils import backend_env_configs, docker_web_env_configs


def check_env_configs() -> None:
    print("\n# Check environment configs")
    print("\n## Check environment configs for backend server")
    print(backend_env_configs.__doc__)
    print(backend_env_configs.env_configs)
    print("\n## Check environment configs for web app containers")
    print(docker_web_env_configs.__doc__)
    print(docker_web_env_configs.env_configs)


if __name__ == "__main__":
    check_env_configs()
