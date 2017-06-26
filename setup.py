from setuptools import setup, find_packages
setup(name='azure_utils',
      version='0.1.4',
      description='Basic utils for working with azureRM and azureSM. Authentication using a ServicePrincipal',
      url='https://www.bscg.us/app-is-a-dumb-word',
      author='BSCG',
      author_email='ron@bscg.us',
      license='MIT-like (see LICENCE file)',

      packages=find_packages(),

      include_package_data=True,
      package_dir={'data' : 'azure_utils/data'},
      package_data={'data' : ['data/*.json', 'data/*.log']},

      entry_points={
        'console_scripts' : [
            'azureutils = azure_utils.__main__:main'
        ]
      },

      install_requires= [
            'azure',
            'msrest',
            'msrestazure',
      ],

      zipsafe=False
      )
