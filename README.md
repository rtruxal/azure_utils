Azure VM Utilities!
===================

***WARNING:** IT IS NOT SAFE TO PERMANENTLY STORE YOUR AZURE SERVICE-PRINCIPAL CREDENTIALS IN A PLAINTEXT JSON DOC. DO NOT SKIP THE README SECTION ON STORING CREDENTIALS.

##Usage:

```sh
# Assuming you're TEMPORARILY storing creds in the designated JSON file.
~$ azureutils turnon host1
host1 has been turned on.

# Using the --infile-credentials (-i) option:
~$ azureutils deallocate host2 -i /path/to/service/principal/credentials.txt
host2 successfully deallocated.

```

#Installation:
This package has dependancies on: `msrest`, `msrestazure`, & `azure`.  

To get them all, run the following command from the shell:
```sh
~$ pip install msrest msrestazure azure
```
###Install:
```sh
~$ git clone https://github.com/rtruxal/azure_utils.git

~$ nano azure_utils/config/host_config.json

~$ pip install .
```





**NOTE**: 
 - `"subscription_id"` in `host_config.json` is **NOT** optional. 
 - Everything else **IS** optional.


###layout of `host_config.json`:
```json
{
  "subscription_id": "11111111-1111-1111-111-111111111111",
  
  "resource_group": "ExampleResourceGroup",
  "hosts": [
    {
      "cmdline_hostname": "foo_host_1",
      "azure_hostname": "FooDBServerExampleResourceGroup"
    },
    {
      "cmdline_hostname": "foo_host_2",
      "azure_hostname": "FooWebServerExampleResourceGroup"
    }
  ]
}

```
