from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import collections,json

# Create your views here.
def home(request):
    return render(request,'home.html')

def result(request):
    url = request.POST.get('web','default').strip(' ')
    n = int(request.POST.get('N','default'))
    m = int(request.POST.get('M','default'))
    
    try:
        r = requests.get('https://www.github.com/' + url + '/repositories')
        if r.ok:
            pass
        else:
            raise('some error occur in connection')
    except:
        return render(request,'error.html')

    htmlContent = r.content
    soup = BeautifulSoup(htmlContent,'html.parser')
    #print(soup.title.string)
    obj = soup.find_all("li",{'itemprop':"owns"})
    no_of_forks = [i.find_all('a',{'class':'muted-link mr-3'}) for i in obj]
    
    newnumber = []
    for i in no_of_forks:
        for j in i:
            x = j.get_text().strip(' ').strip('\n').strip(' ').replace(',','')
            if x.isnumeric():
                newnumber.append(int(x))
                break
            else:
                newnumber.append(0)
    
    name = [i.find('h3').get_text().strip(' ').strip('\n').strip(' ') for i in obj]
    ele = list(zip(newnumber,name))
    ele.sort(reverse = True)
    #print(ele[:n])
    param = {'n':[],'url':url,'number_n':n,'number_m':m}
    for i,j in enumerate(ele[:n]):
        param['n'].append((str(j[0]),str(j[1]),'https://www.github.com/' + url +'/'+ j[1] +'/graphs/contributors'))
    #print(param)
    return render(request,'result.html',param)

#    for i in range(n):
#        temp = 'https://www.github.com/' + url +'/'+ ele[i][1] +'/graphs/contributors'
#        print(temp)
#        source = requests.get(temp,headers = {'User-Agent':'Mozilla/5.0'})
#        if source.ok:
#            pass
#        else:
#            raise("website can't able to fetch")
        
        #print('your = ')
        #print(dir(source))
        #x = (source.json())
        #print(x[name])
        #htmlContent = source.text
        #soup = BeautifulSoup(htmlContent,'lxml')
        #obj = soup.find('div',{'class':'graphs'})
        #head = obj.get_text()
        #print(head)
        #print(obj.get_text())
        #obj1 = obj.find('div',{'class':'repository-content'})
        #print(obj1.get_text())
        #obj2 = soup.find_all('li',{'class':"contrib-person"})
        #print(soup.title.string)
        #print(soup.get_text())
        #print(soup.prettify)
        #print(obj2[0].get_text())
        #name = [i.find('h3').get_text().strip(' ').strip('\n').strip(' ') for i in obj2]
        #print(name)
        #no_of_commits = [i.find('a',{'class':'link-gray text-normal'}).get_text().strip(' ').strip('\n').strip(' ') for i in obj2]
        #print(no_of_commits)
        #d[i] = list(zip(name,no_of_commits))[:m]
