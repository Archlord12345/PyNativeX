cmake_minimum_required(VERSION 3.22)
project(pynativex_core VERSION 0.1.0 LANGUAGES CXX)

add_library(pynativex_core SHARED src/pynativex_core.cpp)
target_include_directories(
  pynativex_core
  PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
    "$<INSTALL_INTERFACE:include>"
)
target_compile_features(pynativex_core PUBLIC cxx_std_20)
target_compile_options(
  pynativex_core
  PRIVATE
    -fno-exceptions
    -fno-rtti
    -fstack-protector-strong
    -fvisibility=hidden
)

if(ANDROID)
  target_sources(pynativex_core PRIVATE src/android_jni.cpp)
  target_link_libraries(pynativex_core PRIVATE android log)
endif()

include(CTest)
if(BUILD_TESTING)
  add_executable(pynativex_core_test tests/core_test.cpp)
  target_link_libraries(pynativex_core_test PRIVATE pynativex_core)
  add_test(NAME pynativex_core_test COMMAND pynativex_core_test)
endif()
