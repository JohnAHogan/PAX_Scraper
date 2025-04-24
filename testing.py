import re
def remove_between(text, start_delimiter, end_delimiter):
    pattern = re.escape(start_delimiter) + ".*?" + re.escape(end_delimiter)
    return re.sub(pattern, start_delimiter+end_delimiter, text)


line ='<p><span style="font-weight: bold;"><span>Category: Systems Administrator</span><br><span>Travel Required:&nbsp;No</span><br><span>Remote Type: No</span><br><span>Clearance: TS/SCI w/ Polygraph </span></span></p>'
list = remove_between(line, '<','>').split('<>')
while '' in list:
    list.remove('')
for index, item in enumerate(list):
    #I can't oneline this and it's killing me
    item = item.replace("&nbsp;","")
    list[index] = item
print(list)