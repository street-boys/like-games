function remove_cmake_files() {
  rm -rf services/c++/like/CMakeFiles \
  services/c++/like/Makefile \
  services/c++/like/CMakeCache.txt \
  services/c++/like/cmake_install.cmake \
  services/c++/like/like
}

$(remove_cmake_files)
