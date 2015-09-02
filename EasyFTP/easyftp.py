import ftplib
import ntpath
import os
from .config import log_decorator as logger


class EasyFTP():
    username = 'anonymous'
    password = ''
    url = ''
    port = 0

    def __init__(self, **kwargs):
        [setattr(self, k, v) for k, v in kwargs.items()]
        if 'url' not in kwargs.keys():
            raise AttributeError(
                'url must be passed on instantiation'
            )

    def __del__(self):
        pass

    def path_end(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def login(self):
        """ Login to an FTP location and generate an attribute to access this

        :rtype boolean
        """
        try:
            self.conn = ftplib.FTP(self.url)
            self.conn.login(self.username, self.password)
            return True
        except:
            raise AttributeError(
                '{u} or {p} incorrect. Authentication Failed'.format(
                    u=self.username,
                    p=self.password
                )
            )

    def logout(self):
        """ Logout of an FTP location
        """
        try:
            self.conn.quit()
        except:
            self.conn.close()
        del self.conn

    @logger.log_func_call
    def mlsd_hunt(
        self,
        search_type,
        current_dir,
        depth,
        current_depth=0,
        found_dirs=[]
    ):
        """ Performs a recursive hunt for a type (dir or file) in an ftp
        location returning a list of values of that type

        :param search_type, a string of either dirs or files
        :param current_dir, a string, the current dir to search
        :param depth, an integer of how deep to go
        :param current_depth, an integer of how deep we are
        :param found_dirs, a list of the found directories
        """
        if search_type == 'dir' and current_dir not in found_dirs:
            found_dirs.append(current_dir)
        if depth != current_depth:
            for data in self.conn.mlsd(current_dir):
                name, desc = data
                if current_dir == '/':
                    found = "{}{}".format(current_dir, name)
                else:
                    found = "{}/{}".format(current_dir, name)
                if desc.get('type') == search_type:
                    found_dirs.append(found)
                if desc.get('type') == 'dir':
                    self.mlsd_hunt(
                        search_type,
                        found,
                        depth,
                        current_depth+1,
                        found_dirs
                    )
        return found_dirs

    def view_directories(self, depth=-1):
        """ returns a list of all directories on the FTP
        :param depth, an integer - if given will limit the recursive search
        """
        if self.login():
            directories = self.mlsd_hunt('dir', self.conn.pwd(), depth, 0, [])
            self.logout()
            return directories

    def view_files(self, depth=-1):
        """ returns a list of all files on the FTP
        :param depth, an integer - if given will limit the recursive search
        """
        if self.login():
            files = self.mlsd_hunt('file', self.conn.pwd(), depth, 0, [])
            self.logout()
            return files

    def download_file(self, ftp_file, local_path, allowed_types=[]):
        """ downloads a file from an ftp location given the path + filename

        :param ftp_file, a string of path and file name
        :param local_path, a string of the local path to download to
        :param allowed_types, a list of extensions that are allowed.
        """
        filename, ext = os.path.splitext(ftp_file)
        if len(allowed_types) == 0 or ext[1:] in allowed_types:
            local_file = local_path + ftp_file
            local_dir = os.path.dirname(r'{}'.format(local_file))
            if not os.path.exists(local_dir):
                os.makedirs(local_dir)
            if not os.path.exists(local_file):
                with open(local_file, 'wb') as f:
                    self.conn.retrbinary(
                        'RETR {}'.format(ftp_file), f.write
                    )
                return local_file
        return False

    def upload_file(self, local_file, ftp_path):
        pass

    def download(self, ftp_paths, local):
        """ downloads files given parameters to the local_path
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
        :param ftp_paths, a list of strs, or dicts, representing remote paths
        :param local, a str representing a local location to dl to
        """
        downloaded_files = []
        if self.login():
            for directory in ftp_paths:
                if type(directory) == str:
                    ftp_path = directory
                    recursion_depth = 1
                    allowed_types = []
                elif type(directory) == dict:
                    try:
                        ftp_path = directory.get('path')
                    except:
                        raise KeyError(
                            '{} must supply path'.format(directory)
                        )
                    recursion_depth = directory.get('depth', -1)
                    allowed_types = directory.get('file_types', [])
                else:
                    raise AttributeError(
                        'Must be a list of path strings, or dictionaries'
                    )
            for ftp_file in self.mlsd_hunt(
                'file', ftp_path, recursion_depth, 0, []
            ):
                local_file = self.download_file(ftp_file, local, allowed_types)
                if not local_file:
                    continue
                else:
                    downloaded_files.append(local_file)
            self.logout()
        return downloaded_files

    def upload(self, local, ftp_file):
        uploaded_files = []
        if self.login():
            self.logout
            pass
        return uploaded_files
