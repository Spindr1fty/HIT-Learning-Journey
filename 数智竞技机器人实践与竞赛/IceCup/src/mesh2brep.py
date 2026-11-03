r"""3MF (triangle mesh) -> B-rep solid, via OCCT sewing + unify-same-domain.

The four uploaded parts are meshes only, so to chamfer them properly we rebuild
a B-rep: sew the triangles into shells, unify coplanar/same-surface faces,
then make a solid.

    python mesh2brep.py in.3mf out.step
"""

import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from cadgen import build123d as bd
from OCP.BRepBuilderAPI import (BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakePolygon,
                                BRepBuilderAPI_MakeSolid, BRepBuilderAPI_Sewing)
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.gp import gp_Pnt
from OCP.ShapeUpgrade import ShapeUpgrade_UnifySameDomain
from OCP.TopAbs import TopAbs_FACE, TopAbs_SHELL, TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS

NS = "{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}"


def load_3mf(path):
    z = zipfile.ZipFile(path)
    model = [n for n in z.namelist() if n.endswith(".model")][0]
    root = ET.fromstring(z.read(model))
    verts, tris = [], []
    for mesh in root.iter(NS + "mesh"):
        base = len(verts)
        for v in mesh.iter(NS + "vertex"):
            verts.append((float(v.get("x")), float(v.get("y")), float(v.get("z"))))
        for t in mesh.iter(NS + "triangle"):
            tris.append((int(t.get("v1")) + base, int(t.get("v2")) + base,
                         int(t.get("v3")) + base))
    return np.array(verts, float), np.array(tris, int)


def count(shape, kind):
    e = TopExp_Explorer(shape, kind)
    n = 0
    while e.More():
        n += 1
        e.Next()
    return n


def mesh_to_solid(verts, tris, tol=1e-4, unify=True):
    t0 = time.time()
    faces = []
    for tri in tris:
        poly = BRepBuilderAPI_MakePolygon()
        for i in tri:
            poly.Add(gp_Pnt(float(verts[i][0]), float(verts[i][1]), float(verts[i][2])))
        poly.Close()
        if not poly.IsDone():
            continue
        mk = BRepBuilderAPI_MakeFace(poly.Wire())
        if mk.IsDone():
            faces.append(mk.Face())
    print(f"  built {len(faces)} faces in {time.time() - t0:.1f}s")
    sew = BRepBuilderAPI_Sewing(tol)
    for f in faces:
        sew.Add(f)
    sew.Perform()
    sh = sew.SewedShape()
    print(f"  sewed: faces {count(sh, TopAbs_FACE)} shells {count(sh, TopAbs_SHELL)}"
          f" in {time.time() - t0:.1f}s")
    if unify:
        un = ShapeUpgrade_UnifySameDomain(sh, True, True, True)
        un.Build()
        sh = un.Shape()
        print(f"  unified: faces {count(sh, TopAbs_FACE)}"
              f" shells {count(sh, TopAbs_SHELL)}")
    # shell -> solid
    e = TopExp_Explorer(sh, TopAbs_SHELL)
    shells = []
    while e.More():
        shells.append(TopoDS.Shell_s(e.Current()))
        e.Next()
    solid = None
    if len(shells) == 1:
        mk = BRepBuilderAPI_MakeSolid(shells[0])
        if mk.IsDone():
            solid = mk.Solid()
    if solid is not None:
        return bd.Solid(solid)
    return bd.Shell(sh)


def main():
    src, dst = sys.argv[1], sys.argv[2]
    v, t = load_3mf(src)
    print(f"{src}: verts {len(v)} tris {len(t)}")
    shape = mesh_to_solid(v, t)
    b = shape.bounding_box()
    print(f"  result: {type(shape).__name__} valid {BRepCheck_Analyzer(shape.wrapped).IsValid()}"
          f" solids {len(shape.solids())} volume {shape.volume / 1000:.2f} cm3"
          f" bbox {b.max.X - b.min.X:.1f} x {b.max.Y - b.min.Y:.1f} x {b.max.Z - b.min.Z:.1f}")
    bd.export_step(shape, dst)
    print("  wrote", dst)


if __name__ == "__main__":
    main()
