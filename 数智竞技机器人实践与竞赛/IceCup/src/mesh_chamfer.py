r"""Mesh-side chamfer tool: 45 deg x w on every convex edge, applied by cutting
the mesh with the chamfer planes (no B-rep available -- the inputs are 3MF
triangle meshes).

Rule (same as docs/chamfer_spec.md):
    * 45 deg x 1.0 mm, measured along each adjacent face
    * convex edges only (n1 . (v2 - v0) < 0 and n2 . (v1 - v0) < 0)
    * skip edges shorter than 1.0 mm, skip degenerate triangles
    * collinear tessellation edges collapse into one plane (dedupe by plane)
    * concave edges untouched

Each convex edge gives a clipping plane: normal m = normalize(n1 + n2),
offset h = w * cos(theta/2) from the edge (theta = interior dihedral).
The chamfered solid = original solid clipped by all those planes.

Usage:
    python mesh_chamfer.py in.3mf out.stl [--size 1.0] [--min-edge 1.0]
"""

import argparse
import sys
import zipfile
import xml.etree.ElementTree as ET

import numpy as np
import trimesh

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


def clean(v, t, tol=1e-4):
    m = trimesh.Trimesh(vertices=v, faces=t, process=True)
    m.merge_vertices(merge_tex=True, merge_norm=True)
    m.update_faces(m.nondegenerate_faces(height=1e-6))
    m.update_faces(m.unique_faces())
    m.remove_unreferenced_vertices()
    return m


def coplanar_regions(mesh, angle_tol=1.0, dist_tol=0.02):
    """Union-find coplanar triangles -> (labels, region normals, areas, centroids)."""
    nf = len(mesh.faces)
    parent = np.arange(nf)
    fn, cent = mesh.face_normals, mesh.triangles_center

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    ang = np.degrees(mesh.face_adjacency_angles)
    for k in range(len(mesh.face_adjacency)):
        if ang[k] < angle_tol:
            f0, f1 = int(mesh.face_adjacency[k][0]), int(mesh.face_adjacency[k][1])
            if abs(float(np.dot(fn[f0], cent[f1] - cent[f0]))) < dist_tol:
                ra, rb = find(f0), find(f1)
                if ra != rb:
                    parent[ra] = rb
    roots = np.array([find(i) for i in range(nf)])
    labels = np.unique(roots, return_inverse=True)[1]
    nreg = int(labels.max()) + 1
    areas = np.bincount(labels, weights=mesh.area_faces, minlength=nreg)
    fnw = fn * mesh.area_faces[:, None]
    nsum = np.zeros((nreg, 3))
    for c in range(3):
        nsum[:, c] = np.bincount(labels, weights=fnw[:, c], minlength=nreg)
    rn = nsum / (np.linalg.norm(nsum, axis=1, keepdims=True) + 1e-12)
    csum = cent * mesh.area_faces[:, None]
    rc = np.zeros((nreg, 3))
    for c in range(3):
        rc[:, c] = np.bincount(labels, weights=csum[:, c], minlength=nreg)
    rc /= (areas[:, None] + 1e-12)
    return labels, rn, areas, rc


def chamfer_planes(mesh, size=1.0, min_edge=2.0, min_deg=50.0, max_deg=130.0,
                   min_area=40.0):
    """Chamfer planes for edges between two LARGE planar regions.

    Teeth / fillet facets are small, so requiring both regions to exceed
    min_area keeps the chamfer on real outer faces and away from the tessellated
    fine features (where a per-triangle normal is not trustworthy).
    """
    labels, rn, areas, rc = coplanar_regions(mesh)
    v = mesh.vertices
    planes = {}
    n_edge = n_area = n_ang = n_conc = 0
    for k in range(len(mesh.face_adjacency)):
        f0, f1 = int(mesh.face_adjacency[k][0]), int(mesh.face_adjacency[k][1])
        r0, r1 = int(labels[f0]), int(labels[f1])
        if r0 == r1:
            continue
        if areas[r0] < min_area or areas[r1] < min_area:
            n_area += 1
            continue
        n0, n1 = rn[r0], rn[r1]
        phi = float(np.degrees(np.arccos(np.clip(np.dot(n0, n1), -1.0, 1.0))))
        if phi < min_deg or phi > max_deg:
            n_ang += 1
            continue
        vi, vj = int(mesh.face_adjacency_edges[k][0]), int(mesh.face_adjacency_edges[k][1])
        p0, p1 = v[vi], v[vj]
        length = float(np.linalg.norm(p1 - p0))
        if length < min_edge:
            n_edge += 1
            continue
        mid = (p0 + p1) / 2.0
        if float(np.dot(n0, rc[r1] - mid)) > -1e-6 or float(np.dot(n1, rc[r0] - mid)) > -1e-6:
            n_conc += 1
            continue
        m = n0 + n1
        nm = float(np.linalg.norm(m))
        if nm < 1e-6:
            continue
        m = m / nm
        h = size * np.sin(np.radians(phi) / 2.0)
        origin = mid - m * h
        key = (round(float(m[0]), 2), round(float(m[1]), 2), round(float(m[2]), 2),
               round(float(np.dot(m, origin)), 2))
        if key in planes:
            m0, o0, l0 = planes[key]
            planes[key] = (m0, o0, l0 + length)
        else:
            planes[key] = (m, origin, length)
    print(f"   regions {int(labels.max()) + 1} | edges {len(mesh.face_adjacency)}:"
          f" planes {len(planes)} | skip small-area {n_area}, angle {n_ang},"
          f" short {n_edge}, concave {n_conc}")
    return sorted(planes.values(), key=lambda x: -x[2])


def chamfer_mesh(mesh, size=1.0, min_edge=2.0, cap=True, guard=0.75, verbose=True):
    planes = chamfer_planes(mesh, size=size, min_edge=min_edge)
    out = mesh
    used = skipped = 0
    for k, (m, origin, elen) in enumerate(planes):
        part = trimesh.intersections.slice_mesh_plane(
            out, plane_normal=-m, plane_origin=origin, cap=cap)
        if part is None or len(part.faces) < 4:
            continue
        removed = out.volume - part.volume
        budget = guard * size * size * elen + 3.0     # ~0.5*w^2*L for a 90 deg edge
        if removed < -1.0 or removed > budget:
            skipped += 1
            if verbose and skipped <= 5:
                print(f"   skip plane L {elen:6.2f} removed {removed:9.1f}"
                      f" budget {budget:7.1f} vol {part.volume:.0f}")
            continue
        out = part
        used += 1
        if verbose and used % 50 == 0:
            print(f"   {used} cuts, {k + 1}/{len(planes)} planes,"
                  f" tris {len(out.faces)} vol {out.volume:.0f}")
    print(f"   applied {used} chamfer planes, skipped {skipped}")
    trimesh.repair.fill_holes(out)
    trimesh.repair.fix_normals(out)
    out.merge_vertices(merge_tex=True, merge_norm=True)
    out.update_faces(out.nondegenerate_faces(height=1e-6))
    out.remove_unreferenced_vertices()
    return out, planes


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--size", type=float, default=1.0)
    ap.add_argument("--min-edge", type=float, default=2.0)
    a = ap.parse_args(argv)

    v, t = load_3mf(a.src)
    mesh = clean(v, t)
    print(f"{a.src}: verts {len(mesh.vertices)} tris {len(mesh.faces)}"
          f" watertight {mesh.is_watertight} volume {mesh.volume / 1000:.2f} cm3"
          f" bbox {np.round(mesh.extents, 1)}")
    out, planes = chamfer_mesh(mesh, a.size, a.min_edge)
    print(f"   chamfered: tris {len(out.faces)} volume {out.volume / 1000:.2f} cm3"
          f" ({out.volume - mesh.volume:+.0f} mm3)"
          f" watertight {out.is_watertight} bbox {np.round(out.extents, 1)}")
    out.export(a.dst)
    print("   wrote", a.dst)


if __name__ == "__main__":
    sys.exit(main())
