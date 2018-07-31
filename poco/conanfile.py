from conans import ConanFile, tools, CMake

class PocoPyReuseConan(ConanFile):
    name = "PocoPy"
    version = "0.1"
    requires = " Poco/1.9.0@pocoproject/stable ", "pybind11/2.2.2@conan/stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"python_version": ["2.7"]}
    default_options = "python_version=2.7"
    exports = "*"
    generators = "cmake"
    build_policy = "missing"

    def conan_info(self):
        self.info.settings.clear()

    def configure(self):
        self.options["Poco"].shared=True

    def build(self):
        cmake = CMake(self)
        pythonpaths = "-DPYTHON_INCLUDE_DIR=/usr/include/python2.7 -DPYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so"
        self.run('cmake %s %s -DEXAMPLE_PYTHON_VERSION=%s' % (cmake.command_line, pythonpaths, self.options.python_version))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy('*.py*')
        self.copy("*.so")

    def package_info(self):
        print self.package_folder
        self.env_info.PYTHONPATH.append(self.package_folder)
