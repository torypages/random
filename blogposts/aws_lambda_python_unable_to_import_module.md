# aws lambda python unable to import module

There is the obvious of how you need to specify your handler as `fileWithoutExtension.funcName`, there is also a permissions issue discussed here http://stackoverflow.com/questions/35340921/aws-lambda-import-module-error-in-python but if you have a code issue in your module this can also happen! In my case I had an issue with one of my import statements. Unfortunately the error reporting here is a bit weak. 
