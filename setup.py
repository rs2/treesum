from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='treesum',
      version='1.0',
      description='Tree sum solver',
      long_description=readme(),
      url='http://github.com/rs2/treesum',
      author='rs2',
      packages=['treesum'],
      install_requires=[],
      include_package_data=True,
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose'],      
      )
