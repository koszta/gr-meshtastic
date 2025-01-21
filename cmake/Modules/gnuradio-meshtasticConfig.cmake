find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_MESHTASTIC gnuradio-meshtastic)

FIND_PATH(
    GR_MESHTASTIC_INCLUDE_DIRS
    NAMES gnuradio/meshtastic/api.h
    HINTS $ENV{MESHTASTIC_DIR}/include
        ${PC_MESHTASTIC_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_MESHTASTIC_LIBRARIES
    NAMES gnuradio-meshtastic
    HINTS $ENV{MESHTASTIC_DIR}/lib
        ${PC_MESHTASTIC_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-meshtasticTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_MESHTASTIC DEFAULT_MSG GR_MESHTASTIC_LIBRARIES GR_MESHTASTIC_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_MESHTASTIC_LIBRARIES GR_MESHTASTIC_INCLUDE_DIRS)
