from cadgen import step

import parts_data as P
from flatpart import build_flat


@step(out="../oldSTEP/short_item.step")
def short_item():
    return build_flat(P.SHORT_ITEM["outline"], P.SHORT_ITEM["holes"],
                      P.SHORT_ITEM["slots"], P.THICKNESS, "short_item")


if __name__ == "__main__":
    short_item()
