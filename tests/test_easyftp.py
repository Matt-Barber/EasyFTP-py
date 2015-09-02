import unittest
from ..EasyFTP import EasyFTP
from io import StringIO
from unittest.mock import mock_open, patch


class TestEasyFTP(unittest.TestCase):

    def mlsd_side_effect(self, *args, **kwargs):
        if args[0] == '/':
            return [
                ('file.txt', {'size': '0', 'modify': '0', 'type': 'file'}),
                ('direct', {'size': '0', 'modify': '0', 'type': 'dir'})
            ]
        elif args[0] == '/images':
            return [
                ('image1.jpg', {'size': '0', 'modify': '0', 'type': 'file'}),
                ('image2.png', {'size': '0', 'modify': '0', 'type': 'file'}),
                ('other_images', {'size': '0', 'modify': '0', 'type': 'dir'})
            ]
        elif args[0] == '/images/other_images':
            return [
                ('image3.jpg', {'size': '0', 'modify': '0', 'type': 'file'})
            ]

        elif args[0] == '/direct':
            return [
                ('inner_direct', {'size': '0', 'modify': '0', 'type': 'dir'})
            ]
        elif args[0] == '/direct/inner_direct':
            return []

    def setUp(self):
        self.username = 'username'
        self.password = 'password'
        self.url = 'ftp.com'

        self.easyftp = EasyFTP(
            username=self.username,
            password=self.password,
            url=self.url
        )

    def test_url_omitted(self):
        with self.assertRaises(AttributeError):
            EasyFTP()

    @patch('ftplib.FTP', autospec=True)
    def test_incorrect_login(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.side_effect = AttributeError('Auth')
        with self.assertRaises(AttributeError):
            self.easyftp.login()

    @patch('ftplib.FTP', autospec=True)
    def test_login(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        res_login = self.easyftp.login()
        self.assertTrue(test_FTP.login.called)
        test_FTP.login.assert_called_with(self.username, self.password)
        self.assertTrue(res_login)

    @patch('ftplib.FTP', autospec=True)
    def test_logout_quit(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        test_FTP.quit.return_value = True
        self.easyftp.login()
        self.easyftp.logout()
        self.assertTrue(test_FTP.quit.called)
        with self.assertRaises(AttributeError):
            self.easyftp.conn

    @patch('ftplib.FTP', autospec=True)
    def test_logout_close(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        test_FTP.close.return_value = True
        test_FTP.quit.side_effect = NameError('Whoops')
        self.easyftp.login()
        self.easyftp.logout()
        self.assertTrue(test_FTP.close.called)
        with self.assertRaises(AttributeError):
            self.easyftp.conn

    @patch('ftplib.FTP', autospec=True)
    def test_mlsd_hunt(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        test_FTP.pwd.return_value = '/'
        test_FTP.mlsd.side_effect = self.mlsd_side_effect
        self.easyftp.login()
        directories = self.easyftp.mlsd_hunt('dir', '/', 1, 0, [])
        self.assertTrue(test_FTP.mlsd.called)
        self.assertListEqual(['/', '/direct'], directories)

    @patch('ftplib.FTP', autospec=True)
    def test_view_directories(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.pwd.return_value = '/'
        test_FTP.mlsd.side_effect = self.mlsd_side_effect
        directories = self.easyftp.view_directories()
        self.assertTrue(test_FTP.pwd.called)
        self.assertListEqual(
            ['/', '/direct', '/direct/inner_direct'], directories
        )

    @patch('ftplib.FTP', autospec=True)
    def test_view_files(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.pwd.return_value = '/'
        test_FTP.mlsd.side_effect = self.mlsd_side_effect
        files = self.easyftp.view_files()
        self.assertTrue(test_FTP.pwd.called)
        self.assertListEqual(['/file.txt'], files)

    @patch('ftplib.FTP', autospec=True)
    def test_download_folder_doesnt_exist(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        test_FTP.quit.return_value = True
        test_FTP.mlsd.return_value = []
        ftp_paths = [
            {
                'path': '/images',
                'depth': -1,
                'file_types': ['jpg']
            }
        ]
        with patch('builtins.open', mock_open(read_data=StringIO('Test'))):
            with patch('os.path.exists', return_value=False):
                with patch('os.makedirs', return_value=True):
                    result = self.easyftp.download(
                        ftp_paths, 'local/file/path'
                    )
                    self.assertTrue(test_FTP.login.called)
        self.assertListEqual(result, [])

    @patch('ftplib.FTP', autospec=True)
    def test_download_file_doesnt_exist(self, FTP):
        pass

    @patch('ftplib.FTP', autospec=True)
    def test_download_files_list(self, FTP):
        pass

    @patch('ftplib.FTP', autospec=True)
    def test_download_files_dictionary(self, FTP):
        test_FTP = FTP.return_value
        test_FTP.login.return_value = True
        test_FTP.quit.return_value = True
        test_FTP.mlsd.side_effect = self.mlsd_side_effect
        ftp_paths = [
            {
                'path': '/images',
                'depth': -1,
                'file_types': ['jpg']
            }
        ]
        with patch('builtins.open', mock_open(read_data=StringIO('Test'))):
            with patch('os.path.exists', return_value=False):
                with patch('os.makedirs', return_value=True):
                    result = self.easyftp.download(
                        ftp_paths, 'local/file/path'
                    )
                    self.assertTrue(test_FTP.login.called)
        self.assertListEqual(
            result,
            [
                'local/file/path/images/image1.jpg',
                'local/file/path/images/other_images/image3.jpg'
            ]
        )

    def test_upload_folder_doesnt_exist(self):
        pass

    def test_upload_file_doesnt_exist(self):
        pass

    def test_upload_files_list(self):
        pass

    def test_upload_files_dictionary(self):
        pass
