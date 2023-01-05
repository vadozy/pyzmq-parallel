from setuptools import setup, find_packages

setup(name='zpen',
      version='0.1',
      description='Zero MQ sandbox',
      license='MIT',
      packages=find_packages(where='src'),
      package_dir={'': 'src'})
