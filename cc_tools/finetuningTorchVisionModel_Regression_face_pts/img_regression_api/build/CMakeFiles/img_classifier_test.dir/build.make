# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.14

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build

# Include any dependencies generated for this target.
include CMakeFiles/img_classifier_test.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/img_classifier_test.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/img_classifier_test.dir/flags.make

CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o: CMakeFiles/img_classifier_test.dir/flags.make
CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o: ../main_img_classifier.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o -c /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/main_img_classifier.cpp

CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/main_img_classifier.cpp > CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.i

CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/main_img_classifier.cpp -o CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.s

# Object files for target img_classifier_test
img_classifier_test_OBJECTS = \
"CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o"

# External object files for target img_classifier_test
img_classifier_test_EXTERNAL_OBJECTS =

img_classifier_test: CMakeFiles/img_classifier_test.dir/main_img_classifier.cpp.o
img_classifier_test: CMakeFiles/img_classifier_test.dir/build.make
img_classifier_test: libimg_classifier.so
img_classifier_test: CMakeFiles/img_classifier_test.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable img_classifier_test"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/img_classifier_test.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/img_classifier_test.dir/build: img_classifier_test

.PHONY : CMakeFiles/img_classifier_test.dir/build

CMakeFiles/img_classifier_test.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/img_classifier_test.dir/cmake_clean.cmake
.PHONY : CMakeFiles/img_classifier_test.dir/clean

CMakeFiles/img_classifier_test.dir/depend:
	cd /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build /home/admin/data/xfeng/finetuningTorchVisionModel_Regression_face_pts/img_regression_api/build/CMakeFiles/img_classifier_test.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/img_classifier_test.dir/depend

