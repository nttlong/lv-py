from win_unc import DiskDrive, UncDirectory,    UncCredentials,              UncDirectoryConnection, UncDirectoryMount

c = UncCredentials(
    r'lvfileservice',
    'l/\cviet2022')
d = UncDirectory(
    r'\\192.168.18.36\lv-media-work-folder',
    c)
print(d)
conn = UncDirectoryConnection(d, persistent=True)
ok =conn.connect()
print(ok)
