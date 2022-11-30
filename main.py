import os

print("loading all the scenes")
# path to all env
path = "./ressources/all_env"
scenes = []
files_ = []

for root, dirs, files in os.walk(path):
    files_ = files

for file in files:
    env_loaded = env(os.path.join(path, file))
    if env_loaded._is_correct:
        scenes.append(env_loaded)

