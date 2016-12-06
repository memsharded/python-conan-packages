from conans import ConanFile, tools, CMake

class PocoPyReuseConan(ConanFile):
    name = "PocoPy"
    version = "0.1"
    requires = "Poco/1.7.3@lasote/stable", "pybind11/any@memsharded/stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"python_version": ["2.7"]}
    default_options = "python_version=2.7"
    exports = "*"
    generators = "cmake"
    build_policy = "missing"

    def conan_info(self):
        self.info.settings.clear()

    def build(self):
        cmake = CMake(self.settings)
        pythonpaths = "-DPYTHON_INCLUDE_DIR=C:/Python27/include -DPYTHON_LIBRARY=C:/Python27/libs/python27.lib"
        self.run('cmake %s %s -DEXAMPLE_PYTHON_VERSION=%s' % (cmake.command_line, pythonpaths, self.options.python_version))
        self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy('*.py*')
        self.copy("*.so")

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)

        