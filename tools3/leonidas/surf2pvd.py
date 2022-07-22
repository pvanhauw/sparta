#!/bin/bin/env python
__author__ = "Pierre Van Hauwaert"

import os
import pyvista as pv
from loguru import logger as log
from argparse import RawTextHelpFormatter
import argparse
import pandas as pd
import numpy as np
from tqdm import tqdm
import concurrent.futures
from concurrent.futures import as_completed
from itertools import repeat

def sdata2vtp(sdataPathIn) :
    log.info(f"Reading: {sdataPathIn}")
    with open(sdataPathIn, "r") as fin:
        lines = fin.readlines()
        foundPointNumbers = False
        foundTriangleNumbers = False
        foundBlockPoint = False
        foundBlockTriangle = False
        for i, line in enumerate(lines):
            if line and len(line.split()) == 2 :
                try :
                    v0 = line.split()[0]
                    v1 = line.split()[1]
                    num = int(v0)
                    name= str(v1)
                    log.info(f"{name}: {num}")
                except :
                    log.error(f"could not parse: {line}")
                if name == "points" :
                    foundPointNumbers = True
                    numP = num
                elif name == "triangles" :
                    foundTriangleNumbers = True
                    numT = num
            elif line and len(line.split()) == 4 :
                foundBlockPoint = True
                df_points = pd.read_csv(sdataPathIn, skiprows=i, nrows=numP, sep=" ", names=["id", "x", "y", "z"])
                index_restart = i + numP
            if (foundPointNumbers and foundTriangleNumbers and foundBlockPoint):
                break
        for i, line in enumerate(lines[index_restart:]):
            if line and len(line.split()) == 4 :
                foundBlockTriangle = True
                df_triangles = pd.read_csv(sdataPathIn, skiprows=i + index_restart, nrows=numT, sep=" ", names=["id", "i", "j", "k"])
            if (foundBlockTriangle):
                break
        df_points.loc[:, "id"] -= 1
        for v in list(df_triangles.columns):
            df_triangles.loc[:, v] -= 1
        faces = np.empty((numT, 4), dtype=int)
        faces[:, 0] = 3
        faces[:, 1:4] = df_triangles[["i", "j", "k"]].to_numpy()
        mesh = pv.PolyData(df_points[["x", "y", "z"]].to_numpy(), faces)
        return mesh


def getListOfVariables(path, headerRow):
    with open(path) as myfile:
        head = [next(myfile) for x in range(headerRow)]
    names = head[headerRow - 1]
    names = names.replace("ITEM: SURFS ", "").replace("\n", "")
    names = names.split(" ")
    names = [x for x in names if x != ""]
    return names


def getTimeStep(path, ):
    with open(path) as myfile:
        head = [next(myfile) for x in range(2)]
    try :
        timeStep = int(head[2 - 1])
        # log.info(f"TIMESTEP: {timeStep}")
    except:
        timeStep = None
        log.error("could not read TIMESTEP")
    return timeStep


def createVtp(pvMesh, dfData, outputpathVtp):
    variables = list(dfData)
    variables = [x for x in variables if x != "id"]
    dfData = dfData.sort_values(["id"], axis=0)
    mesh = pvMesh.copy()
    for v in variables :
        mesh[v] = dfData[v]
    # log.info(f"Writting: {outputpathVtp}")
    mesh.save(outputpathVtp)


def convertMesh(mesh, path, headerRow, pvDir, odg, outputName, i):
    names = getListOfVariables(path=path, headerRow=headerRow)
    df = pd.read_csv(path, sep="\s+", skiprows=headerRow, names=names)
    outputpathVtp = os.path.join(pvDir, f"{outputName}_%0*d.vtp" % (odg, i))
    createVtp(pvMesh=mesh, dfData=df, outputpathVtp=outputpathVtp)


def surf2pvd(sdataPathIn, listResultsFilePaths, outputName, numberOfThreads):
    pvDir = f"{outputName}"
    if not os.path.exists(pvDir):
        os.mkdir(pvDir)
    mesh = sdata2vtp(sdataPathIn)
    listResultsFilePaths.sort(key=os.path.getctime)
    odg = int(np.ceil(np.log10(len(listResultsFilePaths))))
    headerRow = 9
    MT = False
    if numberOfThreads > 1 :
        MT = True
    if not MT :
        for i, path in enumerate(listResultsFilePaths) :
            log.info(f"Processing: {path}")
            convertMesh(mesh, path, headerRow, pvDir, odg, outputName, i)
    else :
        n = len(listResultsFilePaths)
        i_s = range(n)
        numberOfThreads = 4
        with tqdm(total=n) as pbar:
            with concurrent.futures.ProcessPoolExecutor(max_workers=numberOfThreads) as executor:
                for res in tqdm(executor.map(
                        convertMesh,
                        repeat(mesh),
                        listResultsFilePaths,
                        repeat(headerRow),
                        repeat(pvDir),
                        repeat(odg),
                        repeat(outputName),
                        i_s,
                    )):
                    pbar.update(1)
    # pv
    timeStep2VtpDict = {}
    for i, path in enumerate(listResultsFilePaths) :
        outputpathVtp = os.path.join(pvDir, f"{outputName}_%0*d.vtp" % (odg, i))
        timeStep2VtpDict[getTimeStep(path=path)] = outputpathVtp
    #
    pathPvd = os.path.join(f"{outputName}.pvd")
    streamStart = '''<?xml version='1.0'?>
<VTKFile type='Collection' version='0.1' byte_order='LittleEndian'>
<Collection>\n'''
    streamStop = '''</Collection>
</VTKFile>\n'''
    with open(pathPvd, "w") as fout:
        fout.write(streamStart)
        for timeStep, outputpathVtp in timeStep2VtpDict.items():
            fout.write(f"<DataSet timestep='{timeStep}' group='' part='0'  file='{outputpathVtp}'/>\n")
        fout.write(streamStop)
    log.info(f"wrote: {pathPvd}")


def main():
    defaultOutPut = "pvOutput"
    parser = argparse.ArgumentParser(description="Convert sparta surface file and results into pvd format", formatter_class=RawTextHelpFormatter)
    parser.add_argument("input", help="surface input file", type=str)
    parser.add_argument('-r', '--result', help="Optional list of SPARTA dump result files", nargs='+')
    parser.add_argument("-o", "--outputName", help="tag prefix for output", type=str, default=defaultOutPut)
    parser.add_argument("-n", "--numberOfThreads", help="run conversion in parallel", type=int, default=4)
    args = parser.parse_args()
    if not os.path.exists(args.input):
        raise Exception(f"Could not find {args.input}")
    if args.outputName == defaultOutPut:
        log.warning(f"outputName is undefined. using: {args.outputName}")
    surf2pvd(
        sdataPathIn=args.input,
        listResultsFilePaths=args.result,
        outputName=args.outputName,
        numberOfThreads=args.numberOfThreads,
    )


if __name__ == "__main__":
    main()
