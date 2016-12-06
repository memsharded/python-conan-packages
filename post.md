---
layout: post
comments: true
title: "Conan, a C, C++ and Python package manager"
---



Conan is versatile: Visual Studio modules, Golang, is able to package from pre-existing binaries, from sources, etc


A basic python package
-----------------------

Let's begin with a simple python package, a "hello world" functionality that we want to package and reuse:


```python
def hello():
    print("Hello World from Python!")
```

To create a package, all we need to do is create the following layout:

```
-| hello.py
 | __init__.py
 | conanfile.py
```

The ``__init__.py`` is blank, and as it is not necessary to build anything, the recipe for the package can remain simple:

```python
from conans import ConanFile

class HelloPythonConan(ConanFile):
    name = "HelloPy"
    version = "0.1"
    exports = '*'
    build_policy = "missing"

    def package(self):
        self.copy('*.py')

    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
```

The ``exports`` will copy both the ``hello.py`` and the ``__init__.py`` in the recipe. The ``package()`` method is also obvious, all is necessary to construct the package is to copy the python sources.

The ``package_info()`` adds the current package folder to the PYTHONPATH conan environment variable. It will not affect the real environment variable unless the end user want it.

It can be seen that this recipe would be practically the same for most python packages, so it can be factored in a ``PythonConanFile`` base class to further simplify it (open a feature request, or better a pull request :) ) 

With this recipe, all we have to do is:

```bash
$ conan export memsharded/testing
$ conan search
```

Of course if you want to share the package with your team, all you have to do is to ``conan upload`` it to a remote server. But to try things, we can test everything locally.

Now the package is ready for consumption. In another folder, we can create a ``conanfile.txt``:

```txt
[requires]
HelloPy/0.1@memsharded/testing
```

And install it with the following command:

```bash
$ conan install -g virtualenv
```

Creating the above ``conanfile.txt`` might be unnecessary for this simple example, as you can directly run ``conan install HelloPy/0.1@memsharded/testing -g virtualenv``, however, using the file is the canonical way.

The specified ``virtualenv`` generator will create an ``activate`` script (in Windows activate.bat), that basically contains the environment, in this case, the ``PYTHONPATH``. Once we activate it, we are able to find the package in the path and use it:

```bash
$ activate
$ python
Python 2.7.12 (v2.7.12:d33e0cf91556, Jun 27 2016, 15:19:22) [MSC v.1500 32 bit (Intel)] on win32
...
>>> import hello
>>> hello.hello()
Hello World from Python!
>>>
```

The above shows an interactive session, but you can import also the functionality in your regular python script!


And this is basically it! Everything you get from conan, you can easily use it for python: transitives dependencies, conflict resolution, dependency overriding... as well as all the advanced steps that conan provides: ``build()``, ``package()``, ``package_info()``, having different packages for different platforms, managing different remotes in git-like decentralized architecture...


As advanced in the introduction, the real goal of this functionality was to have reusable python code among conan recipes for C and C++ packages. Let`s see how can it be done:


Reusing python code in your recipes
------------------------------------

As the conan recipes are python code itself, it is easy to reuse python packages in them. A basic recipe using the created package would be:

```python
from conans import ConanFile, tools

class HelloPythonReuseConan(ConanFile):
    requires = "HelloPy/0.1@memsharded/testing"

    def build(self):
        with tools.pythonpath(self):
            from hello import hello
            hello()
```

The ``requires`` section is just referencing the previously created package. The functionality of that package can be used in several methods of the recipe: ``source()``, ``build()``, ``package()`` and ``package_info()``, i.e. all of the methods used for creating the package itself. Note that in other places it is not possible, as it would require the dependencies of the recipe to be already retrieved, and such dependencies cannot be retrieved until the basic evaluation of the recipe has been executed.

In the above example, the code is reused in the ``build()`` method as an example. Note the use of a helper context, which basically activates/deactivates the PYTHONPATH environment variable with the value assigned in the package. We didn't want to do this activation implicit for all conan packages, but rather make it explicit, which can also help with import clashes.

```python
$ conan install -g env -g txt
...
$ conan build
Hello World from Python!
```


A full python and C/C++ package manager
----------------------------------------

Once we realized what could be achieved with this functionality, we couldn't resist to try a full application. The real utility of this is that conan is a C and C++ package manager. So if we want to create a python package that wraps the functionality of, lets say the Poco C++ library, it can be easily done. Poco itself has transitive (C/C++) dependencies, but they are already handled by conan. Furthermore, a very interesting thing is that nothing has to be done in advance for that library, thanks to useful tools as pybind11, that allows to create python bindings easily:




Conclusion
------------

Not to compete pip

Show the capabilities of Conan

If you are doing C/C++ and occasionally you need some python in your workflow, as in the conan package recipes themselves, or for some other tooling



