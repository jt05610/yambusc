import argparse
import os.path

from yambusc.config import DEFAULT_DEVICE_NAME, DEFAULT_PROJECT_DIR
from yambusc.model import EnumBase
from yambusc.services import generate_device, get_author, generate_ds
from yambusc.renderer import DataModelRenderer


class Scope(EnumBase):
    DEVICE = "device"
    MODEL = "model"


class Action(EnumBase):
    NEW = "new"
    UPDATE = "update"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scope", type=Scope, choices=tuple(Scope))
    parser.add_argument("action", type=Action, choices=tuple(Action))
    parser.add_argument("-n", "--name", type=str, default=DEFAULT_DEVICE_NAME)
    parser.add_argument("-d", "--dir", type=str, default=DEFAULT_PROJECT_DIR)
    parser.add_argument("-a", "--author", type=str, default=get_author())
    args = parser.parse_args()
    renderer = DataModelRenderer(project_dir=args.dir)
    if args.scope == Scope.DEVICE:
        generate_device(renderer, args.name, args.author)
    elif args.scope == Scope.MODEL:
        ds_path = os.path.join(args.dir, "data_structure.yaml")
        generate_ds(renderer, ds_path, args.dir)


if __name__ == "__main__":
    main()
