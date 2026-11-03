from cadgen import step

import parts_data as P
from flatpart import build_flat


@step(out="../oldSTEP/eight_circle.step")
def eight_circle():
    return build_flat(P.EIGHT_CIRCLE["outline"], P.EIGHT_CIRCLE["holes"],
                      P.EIGHT_CIRCLE["slots"], P.THICKNESS, "eight_circle")


if __name__ == "__main__":
    eight_circle()
