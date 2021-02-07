from setuptools import setup, find_packages

setup(name='aisimpoker',
      version='0.1',
      description='The poker player behavior simulator.',
      license='MIT',
      install_requires=[
          'lark-parser',
          'python-dotenv',
          'treys',
          'pandas',
          'numpy',
          'sklearn',
          'matplotlib',
          'xgboost',
          'Flask',
          'click',
          'sqlalchemy',
          'psycopg2-binary',
          'celery==4.4.7',
          'redis==3.4.1'
      ],
      zip_safe=False, packages=find_packages())
