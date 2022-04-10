item={}
item['username'] = 'r.sbor'
item['follow_type'] = 'follower'
item['follow_name'] = 'vvv'

path_standard = "_____.jpg"

dir_path = '/'.join([item['username'].replace('.', '_'), item['follow_type']])
path_new = '/'.join([dir_path, path_standard[5:]])
print(path_new)
