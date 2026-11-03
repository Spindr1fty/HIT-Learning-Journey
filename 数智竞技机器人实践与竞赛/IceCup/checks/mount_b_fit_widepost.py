"""Run checks/mount_b_fit.py against the wide-post proposal.

g_mount_b_widepost patches g_mount_b's module constants in place, so importing
it before mount_b_fit is enough -- there is one geometry, not two.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))

import g_mount_b_widepost  # noqa: E402,F401  (patches g_mount_b)
import mount_b_fit  # noqa: E402

if __name__ == "__main__":
    sys.exit(mount_b_fit.main())
