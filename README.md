Azure VM Utilities!
===================

***WARNING:** IT IS NOT SAFE TO PERMANENTLY STORE YOUR AZURE SERVICE-PRINCIPAL CREDENTIALS IN A PLAINTEXT JSON DOC. DO NOT SKIP THE README SECTION ON STORING CREDENTIALS.

## Usage:

```sh

# Hardest things about this:
#   you need to find the file azure_utils/config/data/host_config.json and change it.
#   you need to explicitly pass in your credential type via 1 of 3 options.

# Here are your 3 options:


# 1.
#-----by using the internal JSON file.
~$ azureutils [-j|--json-credentials] turnon myVM1 
myVM1 has been turned on.


# 2.
#----arg placement dont matta. Also don't use this option yet. 
~$ azureutils deallocate myVM2 [-i|--infile-credentials] /path/to/service/principal/credentials.txt
host2 successfully deallocated.

# 3.
#----prompt!
~$ azureutils restart myVM1
enter the exact tenant ID including dashes: 
enter the exact Application/Client ID including dashes: 
enter your secret service-principal code: 

myVM1 restarted.
```

# Installation:
This package has dependencies on: `msrest`, `msrestazure`, & `azure`.  

To get them all, run the following command from the shell:
```sh
~$ pip install msrest msrestazure azure
```
## Install:
```sh
~$ git clone https://github.com/rtruxal/azure_utils.git && cd ./azure_utils

~$ nano azure_utils/config/data/host_config.json

~$ pip install .
```





**NOTE**: 
 - `"subscription_id"` in `host_config.json` is **NOT** optional. 
 - Everything else **IS** optional.


### layout of `host_config.json`:
```json
{
  "subscription_id": "11111111-1111-1111-111-111111111111",
  
  "resource_group": "ExampleResourceGroup",
  "hosts": [
    {
      "cmdline_hostname": "foo_host_1",
      "azure_hostname": "FooDBServer"
    },
    {
      "cmdline_hostname": "foo_host_2",
      "azure_hostname": "FooWebServer"
    }
  ]
}

```
