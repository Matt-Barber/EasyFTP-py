#EasyFTP : Python

How often do you find yourself doing a repetitive task with FTP in python and think - this would be easier if X, Y, or Z - well look no further! (or a little further as this isn't quite finished)

##Motivation
I spend a lot of time having to either login to FTP locations and download files, or remove files or upload files - usually of the same type. Recently someone enquired if I could download HTML from 150 FTP locations - there is no way I'm manually logging into 150 FTP locations, recursively hunting for HTML files and downloading them.

##Real applications
The real applications behind this where I can see it being useful, is synchronisation of backups, and pulling down certain types of files. For instance all of your PHP files off of an FTP while maintaining the folder structure that they existed in on the server. It's like a filtered copy and paste.

##Example : Downloading all of the JPGs from an FTP site
```
>>> from EasyFTP import EasyFTP
>>> easyftp = EasyFTP(username='myusername', password='mypassword', url='ftp.something.com')
>>>
>>> # Example download JPGs
>>> ftp_paths =  [
>>>        {
>>>         'path': '/images',
>>>         'depth': -1,
>>>         'file_types': ['jpg']
>>>     }
>>> ]
>>> easyftp.download(
>>>    ftp_paths,
>>>    local/file/path
>>> )
>>>
[
    'local/file/path/images/image1.jpg',
    'local/file/path/images/other_images/image3.jpg'
]

```

#Instantiation
When creating a new EasyFTP supply the following kwargs.

- username : username to the ftp site
- password : password to the ftp site
- url : ftp host address

#Download Method Params
Downloads files given parameters to the local_path
A path can be a list of direct files ['/test.txt','/test/test2.txt']
A path can be a list of folders ['/test', '/test2']
A path can be a list of dictionaries with options :
[
    {
        'path': 'just/path', # path to search
        'depth': -1  # -1 for recursive or # for depth starting at 1,
        'file_types': ['html'] # a list of file extenstions to download
    }
]
ftp_paths, a list of strings, or dictionaries, representing remote paths
local, a string representing a local location to download to

##Dependancies
Stock library - yay! :)

##Unit Tests
Please do try the unit tests, I'd recommend with coverage, nose and nose-timer:
```
# from the parent dir of the module
python -m nose --with-cover --cover-erase --cover-package=EasyFTP --with-timer
```

##Bugs
- Can't allocate port number
- Can't upload files
- Can't remove files
- Lots more, please raise issues and feel free to fork / pull
- This is VERY much a WIP project.

##Author
Me, Myself and I
