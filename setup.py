from setuptools import setup, find_packages
setup(name='azure_utils',
      version='0.1.6rc1',
      description='Basic utils for working with azureRM and azureSM. Authentication using a ServicePrincipal',
      url='https://www.bscg.us/app-is-a-dumb-word',
      author='BSCG',
      author_email='ron@bscg.us',
      license='MIT-like (see LICENCE file)',

      packages=find_packages(),

      # package_dir={'azure_utils' : 'azure_utils/data'},
      package_data={'azure_utils' : ['data/config/*.json', 'data/logs/*.log']},
      include_package_data=True,

      entry_points={
        'console_scripts' : [
            'azureutils = azure_utils.__main__:main'
        ]
      },

      install_requires= [
            'azure',
            'msrest',
            'msrestazure',
            'azure-common'
      ],

      zipsafe=False
      )


