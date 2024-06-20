# main.py
from configuration import get_config
from models import Model

if __name__ == "__main__":
    config = get_config()
    model = Model(config['setting1'])
    print(model.greet())
