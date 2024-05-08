#!/bin/sh
# rm -rf build ; mkdir build ; cd build ; cmake -LH -DBUILD_JPEG:BOOL=ON -DBUILD_PNG:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -DSPARTA_ENABLE_TESTING:BOOL=ON -DFFT:BOOL=FFTW3 ../cmake/ ;
#cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -LH -DBUILD_JPEG:BOOL=ON -DBUILD_PNG:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -DSPARTA_ENABLE_TESTING:BOOL=ON -DFFT:BOOL=NONE -DPKG_FFT:STRING=ON -DBUILD_SHARED_LIBS=ON ../cmake/ ; make -j 16 
#cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -LH -DBUILD_JPEG:BOOL=ON -DBUILD_PNG:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -DSPARTA_ENABLE_TESTING:BOOL=ON -DFFT:BOOL=NONE -DPKG_FFT:STRING=ON -DSPARTA_ENABLE_ALL_PKGS:BOOL=ON -DSPARTA_MACHINE:STRING=mint ../cmake/ ; make -j 16
#cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -C ../cmake/presets/mint.cmake -LH -DBUILD_JPEG:BOOL=ON -DBUILD_PNG:BOOL=ON -DCMAKE_BUILD_TYPE:STRING=Release -DSPARTA_ENABLE_TESTING:BOOL=ON  -DPKG_FFT:STRING=FFTW3 -DSPARTA_MACHINE:STRING=mint ../cmake/ ; make -j 16

cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake mode=shlib -C ../cmake/presets/mint.cmake -LH   ../cmake/ ; make -j 16
#cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -C ../cmake/presets/kokkos_mint.cmake -LH   ../cmake/ ; make -j 16
#cd ~/workspace/sparta/; rm -rf build ; mkdir build ; cd build ; cmake -C ../cmake/presets/kokkos_cuda.cmake -LH   ../cmake/ ; make -j 16

