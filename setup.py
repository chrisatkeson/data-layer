from setuptools import setup, find_packages

# When you update the module, you'll need to up the version or
# you could just uninstall using pip and reinstall. But incrementing
# version would be preferable.

setup(name='data-layer',
      version='0.1.0',
      description='data layer python code that can be installed via pip.',
      long_description='An abstraction layer for data storage and retrieval.',
      url='https://github.com/chrisatkeson/data-layer',
      author='Chris Atkeson',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      python_requires='>=3.11'
      )
