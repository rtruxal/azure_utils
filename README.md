Azure VM Utilities!
===================
**NOTE**:
 - Entering your `"subscription_id"` in `azure_utils/data/config/host_config.json` is **NOT** optional.
 - Everything else **IS** optional.

**WARNING**:
IT IS NOT SAFE TO PERMANENTLY STORE YOUR AZURE SERVICE-PRINCIPAL CREDENTIALS IN A PLAINTEXT JSON DOC.
DO NOT SKIP THE README SECTION ON STORING CREDENTIALS.

# Usage:

```sh
## The -j flag indicates you're using the default json-file to store your AAD service-principal credentials.
~$ azureutils -j turnon remotehost-A
remotehost-A has been turned on.

## Note that the statusof keyword retrieves the actual hostname.
~$ azureutils -j statusof remotehost-A
Webserver-A-WestUS2 is currently running. It's been on since: 2016-09-30 22:04:22.355673+00:00

## Note also that we can get long-form stats by using the -l flag.
~$ azureutils -jl statusof remotehost-A
REMOTEHOST-A:
resource_id: ==> 8ee39295-312a-4df0-a928-80a23028fc87
hostname: ==> Webserver-A-WestUS2
last_up: ==> 2016-09-30 22:04:22.355673+00:00
prov_state: ==> Updating
power_state: ==> VM running
location: ==> westus2

## Turning off a vm is not the same as deallocating it! Good for rebooting without changing your dynamic-ip.
~$ azureutils -j turnoff remotehost-A
remotehost-A has been shut down.

~$ azureutils -j statusof remotehost-A
Webserver-A-WestUS2 is currently stopped (vm is still allocated).

~$ azureutils -j deallocate remotehost-A
remotehost-A has been deallocated.

~$ azureutils -jl statusof remotehost-A
REMOTEHOST-A:
resource_id: ==> 8ee39295-312a-4df0-a928-80a23028fc87
hostname: ==> Webserver-A-WestUS2
last_up: ==> 2017-09-30 22:04:22.355673+00:00
prov_state: ==> Provisioning succeeded
power_state: ==> VM deallocated
location: ==> westus2
```

aaaand that's all for now.

# Pre-Install:

This package has dependencies on: `msrest`, `msrestazure`, `azure`, & `azure-common`.

To get them all, run the following command from the shell:
```sh
~$ pip install msrest==0.4.0 msrestazure==0.4.0 azure=="2.0.0rc5" azure-common==1.1.4
```
After that,
```sh
~$ git clone https://github.com/rtruxal/azure_utils.git && cd ./azure_utils
```
Now, you're going to need to populate your host-list & determine if you wanna use the credential-file.
Either way, you're gonna need to:
### **GO TO THE `azure_utils/config/ DIRECTORY.`**
Then you're prly gonna wanna...
### EDIT `azure_utils/config/data/host_config.json`
### &
### `azure_utils/config/data/credentials_config.json`

K now when you're done, proceed.


# Installation:
```sh
~$ pwd
/path/to/azure_utils
~$ pip install .
```
& bam you're done.

# Storing or Passing-in Credentials:

   you need to explicitly pass in your service principals via 1 of 3 mechanisms.

```sh
# Here are your 3 options:


# 1.
#-----by using the internal JSON file (AND READING THE DAMN WARNING.txt)
~$ azureutils [-j|--json-credentials] turnon myVM1
myVM1 has been turned on.


# 2.
#----arg placement dont matta. .ini or xml-style plz.
~$ azureutils deallocate myVM2 [-i|--infile-credentials] /path/to/service/principal/credentials.txt
host2 successfully deallocated.

# 3.
#----prompt! (this'n is the default!...for safety!)
~$ azureutils restart myVM1
enter the exact tenant ID including dashes:
enter the exact Application/Client ID including dashes:
enter your secret service-principal code:

myVM1 restarted.
```


# Reference:

### layout of `host_config.json`:
```json
{
  "subscription_id": "11111111-1111-1111-111-111111111111",

  "default_resource_group": "ExampleResourceGroup",
  "hosts": [
    {
      "cmdline_hostname": "foo_host_1",
      "azure_hostname": "FooDBServer"
    },
    {
      "cmdline_hostname": "foo_host_2",
      "azure_hostname": "FooWebServer"
      "resource_group": "NotTheExampleDefaultOne"
    }
  ]
}

```
