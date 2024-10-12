import tomllib

def load_config(path):
    with open(path, "rb") as f:
        return tomllib.load(f)

if __name__ == "__main__":
    config = load_config("config.toml")
    print(config)