from cadgen import step

import parts_data as P
from flatpart import build_flat


@step(out="../oldSTEP/six_circle.step")
def six_circle():
    return build_flat(P.SIX_CIRCLE["outline"], P.SIX_CIRCLE["holes"],
                      P.SIX_CIRCLE["slots"], P.THICKNESS, "six_circle")


if __name__ == "__main__":
    six_circle()
