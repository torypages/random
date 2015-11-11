import multiprocessing                                                                                                                     
import time                                                                                                                                
import os                                                                                                                                  
import boto3                                                                                                                               
                                                                                                                                           
class Consumer(multiprocessing.Process):                                                                                                   
                                                                                                                                           
    def __init__(self, task_queue, result_queue):                                                                                          
        multiprocessing.Process.__init__(self)                                                                                             
        self.task_queue = task_queue                                                                                                       
        self.result_queue = result_queue                                                                                                   
                                                                                                                                           
        # Get S3 client                                                                                                                    
        script_path = os.path.dirname(os.path.realpath(__file__))                                                                          
        conf_str = os.path.join(script_path, 's3_credentials.conf')                                                                      
        conf_f = open(conf_str, 'r')                                                                                                       
        access_key = conf_f.readline().strip()                                                                                             
        secret_access_key = conf_f.readline().strip()                                                                                      
        region = conf_f.readline().strip()                                                                                                 
                                                                                                                                           
        self.s3_client = boto3.Session(aws_access_key_id=access_key,                                                                       
                           aws_secret_access_key=secret_access_key,                                                                        
                           region_name=region).client('s3')                                                                                
                                                                                                                                           
                                                                                                                                           
    def run(self):                                                                                                                         
        proc_name = self.name                                                                                                              
        while True:                                                                                                                        
            next_task = self.task_queue.get()                                                                                              
            if next_task is None:
                # Poison pill means shutdown
                #print('Exiting', proc_name)
                self.task_queue.task_done()
                break
            #print(proc_name, next_task)
            answer = next_task(self.s3_client)
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class Task(object):
    def __init__(self, prefix):
        # self.a = a
        # self.b = b
        self.prefix = prefix

    def __call__(self, s3_client):
        if not self.prefix:
            return None
        #print("s3_client", s3_client)
        paginator = s3_client.get_paginator('list_objects')
        bucket = 'bucket-name'
        keys = []
        for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=self.prefix, PaginationConfig={'PageSize': 5000}):
           if result.get('CommonPrefixes') is not None:
                for subdir in result.get('CommonPrefixes'):
                    tasks.put(Task(subdir.get('Prefix')))

           if result.get('Contents') is not None:
               for file in result.get('Contents'):
                   x = file.get('Key')
                   keys.append(x)

        return keys 
    #def __str__(self):
    #    return '%s * %s' % (self.a, self.b)


if __name__ == '__main__':
    # Establish communication queues
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()
    
    # Start consumers
    num_consumers = multiprocessing.cpu_count() * 2 * 3
    print('Creating {} consumers'.format(num_consumers))
    consumers = [ Consumer(tasks, results)
                  for i in range(num_consumers) ]
    for w in consumers:
        w.start()
    
    # Enqueue jobs
    #num_jobs = 2
    #for i in range(num_jobs):
    tasks.put(Task('someKey/'))

    # Wait for all of the tasks to finish
    tasks.join()

    # Add a poison pill for each consumer
    for i in range(num_consumers):
        tasks.put(Task(None))
        tasks.put(None)

    # Start printing results
    key_count = 0
    none_count = 0
    while True:
       if none_count == num_consumers:
           break
       result = results.get()
       if not result:
           none_count += 1
       else:
           key_count += len(result)

    print("Num Keys: {}".format(key_count))
