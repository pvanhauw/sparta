#!/bin/bin/env python
__author__ = "Pierre Van Hauwaert"

import os
import pyvista as pv
from loguru import logger as log
from argparse import RawTextHelpFormatter
import argparse
import numpy as np
from copy import copy


def convertToVTP(filePath, save=False, triangulate=False):
    log.info(f"Reading: {filePath}")
    filename, file_extension = os.path.splitext(filePath)
    # meshio_extentions = [".obj"]
    pyvista_extentions = [
        ".vtp",
        ".vtk",
        ".stl",
        ".ply",
        ".vtu"
    ]
    gridpro_extentions = [
        ".tria",
        ".quad",
    ]
    if file_extension in gridpro_extentions:
        import toolspampero.preprocessing.converters.GridProSurfaceIO as GridProSurfaceIO
        pv_surf_mesh = GridProSurfaceIO.getPolyDataFromGPSurfaceFile(filePath, cleanPolyData=True)
    # elif file_extension in meshio_extentions:
    #     import meshio
    #     import tempfile
    #     filePathTmp = os.path.join(tempfile.gettempdir(), "%s.%s" % (filename, "vtk"))
    #     mio = meshio.read(filePath)
    #     meshio.write(filePathTmp, mio)
    #     pv_surf_mesh = pv.read(filePathTmp)
    elif file_extension in pyvista_extentions:
        pv_surf_mesh = pv.read(filePath)
    else:
        raise Exception("extension %s is not handle %s" % (file_extension, filePath))
    pv_surf_mesh = pv_surf_mesh.extract_surface()
    if triangulate:
        log.info("triangulate")
        pv_surf_mesh_tria = pv_surf_mesh.triangulate()
        pv_surf_mesh_tria = pv_surf_mesh_tria.clean()
    else:
        pv_surf_mesh_tria = pv_surf_mesh
    

    # pv_surf_mesh_tria.compute_normals(cell_normals=True, point_normals=True, inplace=True)
    # pv_surf_mesh_tria.compute_cell_sizes(area=True)
    if save:
        filePathOut = os.path.join("%s-saved.%s" % (filename, "vtp"))
        pv_surf_mesh_tria.save(filePathOut)
    return pv_surf_mesh_tria

def get_synchonize_normal_mesh(mesh, display=False):
    # Compute normals without consistent computation
    normals_no_consistent = mesh.compute_normals(cell_normals=True, point_normals=False, consistent_normals=False, non_manifold_traversal=False)
    # Compute normals with consistent computation
    normals_consistent = mesh.compute_normals(cell_normals=True, point_normals=False, consistent_normals=True, non_manifold_traversal=False)
    if display:
        pl = pv.Plotter(shape=(1, 2))
        pl.subplot(0, 0)
        pl.add_mesh(normals_consistent, scalars="Normals", component=2)
        pl.subplot(0, 1)
        pl.add_mesh(normals_no_consistent, scalars="Normals", component=2)
        pl.link_views()
    faces = mesh.faces.reshape(-1,4)
    new_faces = faces.copy()
    # Compare normals and adjust triangles if necessary
    count_reverse = 0
    # TODO: get ride o pythin loop
    for i in range(mesh.n_cells):
        nc = np.array(normals_consistent.cell_normals[i])
        nnc = np.array(normals_no_consistent.cell_normals[i])
        dot = np.dot(nc, nnc)
        if dot < 0 :
            # Invert the triangle vertices for this cell
            face = faces[i, 1:3]
            new_faces[i, 1:3] = face[::-1]
            new_faces[i, 0] = 3
            count_reverse += 1
    new_faces = new_faces.ravel()
    mesh.faces = new_faces
    if count_reverse > 0:
        log.warning(f"reverse {count_reverse} faces")
    return mesh 

def pv2sparta(filePathIn, filePathOut, triangulate=False, display=False, synchronize_normals=False, auto_synch_as_wall=False):
    # log.info(f"Reading {filePathIn} ...")
    mesh = convertToVTP(filePathIn, save=False, triangulate=triangulate)
    if synchronize_normals :
        mesh = get_synchonize_normal_mesh(mesh)
    if auto_synch_as_wall:
        if not synchronize_normals:
            msg = "synchronize_normals shall be enable if auto_synch_as_wall is used"
            log.error(mesh)
            raise ValueError(msg)
        else:
            face_indices = mesh.faces.reshape(-1, 4)[:, 1:]
            # Extract the vertices corresponding to each triangle
            v1 = mesh.points[face_indices[:, 0]]
            v2 = mesh.points[face_indices[:, 1]]
            v3 = mesh.points[face_indices[:, 2]]
            # Compute the cross product of v2 and v3
            cross_product = np.cross(v2, v3)
            # Compute the signed volume contributions
            signed_volumes = np.sum(v1 * cross_product, axis=1) / 6.0
            # Sum the signed volumes and take the absolute value
            volume = signed_volumes.sum()
            if volume < 0:
                mesh.flip_normals()
    # pv_surf_mesh_tria = get_synchonize_normal_mesh(pv_surf_mesh_tria)
    xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
    log.info(f"x Bounds : [{xmin} , {xmax}]")
    log.info(f"y Bounds : [{ymin} , {ymax}]")
    log.info(f"z Bounds : [{zmin} , {zmax}]")
    # mesh = pv.read(filePathIn)
    log.info(f"Writing: {filePathOut}")
    with open(filePathOut, "w") as fout:
        sep = " "
        fout.write(f"# SPARTA surface file, from input file {filePathIn}\n\n")
        fout.write(f"{mesh.n_points} points\n")
        fout.write(f"{mesh.n_cells} triangles\n")
        offset = 1
        pointsIndexes = np.arange(start=0 + offset, stop=mesh.n_points + offset, dtype=int).reshape(-1, 1)
        pointsIndexesStr = pointsIndexes.astype(str)
        pointsStr = mesh.points.astype(str)
        toWrite = np.concatenate((pointsIndexesStr, pointsStr), axis=1)
        log.info(f"Writing {mesh.n_points} points ...")
        fout.write("\nPoints\n\n")
        np.savetxt(fout, toWrite, fmt="%s %s %s %s")
        countTriaTh = mesh.faces.shape[0]
        countTriaReal = mesh.n_cells * 4
        if countTriaReal != countTriaTh:
            raise ValueError(f"Expect {mesh.n_cells} to be triangles but {mesh.faces.shape[0]/4} should be stored. Use the --triangulate option")
            # TODO check actual for all cells, one by one comparing with
            # https://vtk.org/doc/nightly/html/vtkCellType_8h_source.html
        conn = copy(mesh.faces.reshape(-1, 4)[:, 1:])
        conn += 1
        triaIndexesStr = np.arange(start=0 + offset, stop=mesh.n_cells + offset, dtype=int).reshape(-1, 1).astype(str)
        log.info(f"Writing {mesh.n_cells} triangles ...")
        fout.write("\nTriangles\n\n")
        np.savetxt(fout, np.concatenate((triaIndexesStr, conn), axis=1), fmt="%s %s %s %s")
    log.info("checking edges being manifold ...")
    edges = mesh.extract_feature_edges(feature_angle=180, boundary_edges=True, non_manifold_edges=True, feature_edges=False, manifold_edges=False, progress_bar=False)
    if edges.n_cells != 0:
        log.error(f"found {edges.n_cells} edges")
        log.error(edges)
    if display:
        p = pv.Plotter()
        p.add_mesh(mesh, opacity=0.3, color="green", show_edges=False, label="surface")
        if edges.n_cells != 0:
            p.add_mesh(edges, opacity=1, color="red", show_edges=True, label="edges")
        p.show_axes()
        p.show_bounds()
        p.add_legend()
        p.show()


def main():
    parser = argparse.ArgumentParser(description="Convert surface (vtp, tria (GP), vtk, stl) surface file to sparta surface format (.ss)", formatter_class=RawTextHelpFormatter)
    parser.add_argument("input", help="surface input file", type=str)
    parser.add_argument("-o", "--outputName", help="tag prefix for output", type=str, default=None)
    parser.add_argument("-d", "--display", help="vizualise the results on-the-fly", action="store_true")
    parser.add_argument("-t", "--triangulate", help="triangulate input", action="store_true")
    parser.add_argument("-s", "--synchronize_normals", help="use vtk to synchronize the normals", action="store_true")
    parser.add_argument("-a", "--auto_synch_as_wall", help="flip the normal so that the geometry will be identified as a wall. synchronize_normals must be enable and the surface must be watertight and manifold", action="store_true")
    args = parser.parse_args()
    if not os.path.exists(args.input):
        raise Exception(f"Could not find {args.input}")
    if args.outputName is None:
        outputName = os.path.join("output.ss")
        log.warning(f"outputName is undefined, so outputName={outputName} is be used")
    else:
        outputName = args.outputName
    pv2sparta(
        filePathIn=args.input, 
        filePathOut=outputName, 
        triangulate=args.triangulate, 
        display=args.display, 
        synchronize_normals=args.synchronize_normals,
        auto_synch_as_wall=args.auto_synch_as_wall,
    )


if __name__ == "__main__":
    main()
