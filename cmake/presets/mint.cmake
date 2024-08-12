# mpi = Linux box/cluster, g++, installed MPI

# ################### BEGIN SPARTA OPTIONS ####################
set(SPARTA_MACHINE
    mint
    CACHE STRING
          "Descriptive string to describe \"spa_\" executable configuration"
          FORCE)
set(SPARTA_CXX_COMPILE_FLAGS
    -fPIC  -DSPARTA_BIGBIG
    CACHE STRING "Compiler flags use when building .o files for spa_*")
# ################### END SPARTA OPTIONS ####################

# ################### BEGIN TPL OPTIONS ####################
# ################### END   TPL OPTIONS ####################

# ################### BEGIN PACKAGE OPTIONS ####################
# ################### END   PACKAGE OPTIONS ####################

# ################### BEGIN CMAKE OPTIONS ####################
set(CMAKE_C_COMPILER
    "mpicc"
    CACHE STRING "")
set(CMAKE_CXX_COMPILER
    "mpic++"
    CACHE STRING "")
set(CMAKE_CXX_FLAGS
    "-O3"
    CACHE STRING "")
set(CMAKE_AR
    "ar"
    CACHE STRING "")
set(CMAKE_SHARED_LINKER_FLAGS
    "-fPIC -shared"
    CACHE STRING "")
set(CMAKE_EXE_LINKER_FLAGS
    "-O"
    CACHE STRING "")
set(BUILD_JPEG
    "ON"
    CACHE BOOL "")
set(BUILD_PNG
    "ON"
    CACHE BOOL "")
set(PKG_FFT
    "FFTW3"
    CACHE STRING "")
set(PKG_FFT
    "FFTW3"
    CACHE STRING "")
set(SPARTA_ENABLE_TESTING
    "OFF"
    CACHE BOOL "")
set(CMAKE_BUILD_TYPE
   "Release"
    CACHE STRING "")
set(BUILD_SHARED_LIBS
   "ON"
    CACHE BOOL "")


# ################### END CMAKE OPTIONS ####################
