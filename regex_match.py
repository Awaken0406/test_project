import re
content = "Hello 123 4567 World_This is a Regex Demo"
print(len(content))
result = re.match('^Hello\s\d\d\d\s\d{4}\s\w{10}',content)
print(result)
print(result.group())
print(result.span())




c = "Hello 1234567 World_This is a Regex Demo"
s = re.match('^Hello\s(\d+)\sWorld',c)
print(s)
print(s.group())#打印完整匹配结果
print(s.group(1))#打印第一个被()包围的匹配结果
print(s.span())#打印整个字符长度


result = re.match('^Hello.*Demo',content)# .任意字符 *字符无限次 ? 非贪婪匹配
print(result)
print(result.group())
print(result.span())

#re.search()#match的开始的字符必须与字符串一致才可以匹配,search则会扫描整个字符串，但只返回与表达式匹配的第一个字符串
#re.findall()#与search一致，但会返回与表达式匹配的所有字符串

c2 = "wd12fds53aa"
s2 = re.sub('\d+','',c2)#替换所有数字
print(s2)

#可以把表达式保存成对象
ojb = re.compile('^Hello\s\d\d\d\s\d{4}\s\w{10}')
sObj = re.search(ojb,content)
