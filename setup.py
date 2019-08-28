from setuptools import setup, find_packages

setup(name='maths_test',
      version='1.0',
      description='Application to allow teachers to create maths tests for students',
      author='Connor Charles',
      author_email='ccharles.gb@gmail.com',
      url='',
      packages=find_packages(),
      python_requires=">=3.6",
      entry_points={
          'console_scripts': [
              'maths-test:maths_test.cli:cli',
          ], },
      install_requires=[
          "flask>=1.1",
          "flask_sqlalchemy>=2.4",
          "python-dotenv",
          "jsmin",
          "flask_assets",
          "uwsgi",
          "flask-marshmallow",
          "marshmallow-sqlalchemy",
          "flask-dotenv"
      ],
      extras_require={
          "dev": [
              "pytest",
              "coverage"
          ]
      }
      )
