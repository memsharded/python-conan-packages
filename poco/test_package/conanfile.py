from conans import ConanFile, tools

class PocoPyTestConan(ConanFile):
    requires = "PocoPy/0.1@memsharded/testing"

    def test(self):
      # self.conanfile_directory
      with tools.pythonpath(self):
          import poco
          print("Random float from POCO: %s" % poco.random_float())
