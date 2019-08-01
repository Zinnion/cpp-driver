#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os

class CppDriverConan(ConanFile):
    name = "cpp-driver"
    version = "2.13.0"
    description = "Cassandra C++ Driver"
    url = "https://github.com/zinnion/cpp-driver"
    homepage = "https://github.com/datastax/cpp-driver"
    license = "Apache"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    short_paths = True
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    requires = (
        "libuv/1.29.1@zinnion/stable",
        "OpenSSL/1.1.1b@zinnion/stable",
    )

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
    
    def configure(self):
        del self.settings.compiler.libcxx
        self.options["libuv"].shared = self.options.shared

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['CASS_BUILD_STATIC'] = not self.options.shared
        cmake.definitions['CASS_BUILD_SHARED'] = self.options.shared
        cmake.definitions['LIBUV_ROOT_DIR'] = self.deps_cpp_info["libuv"].rootpath
        cmake.definitions['OPENSSL_ROOT_DIR'] = self.deps_cpp_info["OpenSSL"].rootpath        
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ['cassandra']
        else:
            self.cpp_info.libs = ['cassandra_static']
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["pthread", "rt"])

