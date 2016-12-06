from conans import ConanFile, tools

class HelloPythonReuseConan(ConanFile):
    requires = "HelloPy/0.1@memsharded/testing"

    def build(self):
        with tools.pythonpath(self):
            from hello import hello
            hello()