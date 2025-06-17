#!/bin/sh
ml load openmpi/4.1.6

cd ~/scratch/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -C ../cmake/presets/mint.cmake -LH   -DSPARTA_BIGBIG=True  ../cmake/ ; make -j 16


