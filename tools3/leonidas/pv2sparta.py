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


def pv2sparta(filePathIn, filePathOut, triangulate=False, display=False):
    # log.info(f"Reading {filePathIn} ...")
    mesh = convertToVTP(filePathIn, save=False, triangulate=triangulate)
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
        # toWrite = np.concatenate((pointsIndexes, mesh.points), axis=1)
        # np.savetxt(fout, toWrite, fmt="%d %lf %lf %lf")
        np.savetxt(fout, toWrite, fmt="%s %s %s %s")
        countTriaTh = mesh.faces.shape[0]
        countTriaReal = mesh.n_faces * 4
        if countTriaReal != countTriaTh:
            raise ValueError(f"Expect {mesh.n_faces} to be triangles but {mesh.faces.shape[0]/4} should be stored. Use the --triangulate option")
            # TODO check actual for all cells, one by one comparing with
            # https://vtk.org/doc/nightly/html/vtkCellType_8h_source.html
        conn = copy(mesh.faces.reshape(-1, 4)[:, 1:])
        conn += 1
        triaIndexesStr = np.arange(start=0 + offset, stop=mesh.n_faces + offset, dtype=int).reshape(-1, 1).astype(str)
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
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise Exception(f"Could not find {args.input}")
    if args.outputName is None:
        outputName = os.path.join("output.ss")
        log.info(f"outputName is undefined, so outputName={outputName} shall be used")
    else:
        outputName = args.outputName
    pv2sparta(
        filePathIn=args.input, filePathOut=outputName, triangulate=args.triangulate, display=args.display,
    )


if __name__ == "__main__":
    main()
