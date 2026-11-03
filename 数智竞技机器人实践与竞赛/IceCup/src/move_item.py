from cadgen import step

import parts_data as P
from flatpart import build_flat


@step(out="../oldSTEP/move_item.step")
def move_item():
    return build_flat(P.MOVE_ITEM["outline"], P.MOVE_ITEM["holes"],
                      P.MOVE_ITEM["slots"], P.THICKNESS, "move_item")


if __name__ == "__main__":
    move_item()
