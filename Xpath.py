from lxml import etree


text = '''  
<div>
    <ul>
        <li class="item-0"><a href="link1.html">first item</a></li>
        <li class="item-1"><a href="link2.html">second item</a></li>
        <li class="item-2"><a href="link3.html">third item</a>
    </ul>
</div>  
'''

html = etree.HTML(text)
result = etree.tostring(html)
print(result.decode('utf-8'))

s = html.xpath('//*')#所有节点
print(s)
print('--------------------------')
s = html.xpath('//li')#li节点
print(s)

print('--------------------------')
s = html.xpath('//li/a')#li节点的a节点
print(s)

print('--------------------------')
s = html.xpath('//ul//a')#ul节点下的所有子孙a节点,//a换成/a则为空
print(s)


#获取父节点属性
print('--------------------------获取父节点属性')
s = html.xpath('//a[@href="link3.html"]/../@class')#选取href属性为link3.html的a节点,然后获取其父节点,在获取服务节点的class属性
print(s)

#过滤
print('--------------------------过滤')
s = html.xpath('//li[@class="item-0"]')#选取href属性为link3.html的a节点,然后获取其父节点,在获取服务节点的class属性
print(s)
