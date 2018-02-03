from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.http import HttpResponse
import base64


########### Python 2.7 #############
import httplib, urllib, base64, json
import math
subscription_key1 = 'd5bac69b1ace45efb94ee361bc985749'
subscription_key = 'aeead2d5d34548fe9fe2475a3190a187'

uri_base = 'westcentralus.api.cognitive.microsoft.com'


def write_1(a,b):
    f=open("./data.txt",'a')
    f.write(a+' '+b+'\n')
    f.close()

FaceList={}
def read_1():
    f2=open("./data.txt","r")
    for l in f2:
        b=l.strip().split()
        try:
            FaceList[b[0]]=b[1]
        except:
            pass


def add_in_list(url_photo,a): 
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'aeead2d5d34548fe9fe2475a3190a187',
    }


    params = urllib.urlencode({

    })
    key_p=''
    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/facelists/first_list/persistedFaces?%s" % params, "{ 'url': '" +url_photo+"' }", headers)
        response = conn.getresponse()
        data = response.read()
        parsed = json.loads(data)
        try:
            key_p=parsed["persistedFaceId"]
        except:
            pass    
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror)) 
    if key_p :    
        write_1(key_p,a)
        read_1()


def find_face(fac_id):
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'aeead2d5d34548fe9fe2475a3190a187',
    }

    params = urllib.urlencode({
    })
    body="""{    
        "faceId": " """ +fac_id+""" ",
        "faceListId":"first_list",  
        "maxNumOfCandidatesReturned":5,
        "mode": "matchPerson"
    }"""

   
    conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/face/v1.0/findsimilars?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    parsed = json.loads(data)
    ans=''
    try:
        l=len(parsed)
        read_1()
        for i in xrange(0,l):
            if parsed[i]["persistedFaceId"] in FaceList.keys():
                if parsed[i]["confidence"] > 0.40 :
                    ans=FaceList[parsed[i]["persistedFaceId"]]
                break
    except:
        pass 
    conn.close()
    if ans=='':
        ans='stranger'
    return ans



def check_emotion(dict1):
    i=0
    a=''
    #print dict1
    for y in dict1.keys():
        #print y
        if dict1[y] > i:
            a=y
            i=dict1[y]
    return a        

def parse1( dict1):
    size_value=len(dict1["description"]["captions"])
    desc=""
    try:
        for i in xrange(0,size_value):
            desc=desc+dict1["description"]["captions"][i]["text"]
    except:
        pass        
    return desc
num={1:'first',2:'second',3:'third',4:'fourth',5:'fifth',6:'sixth',7:'seventh'}
face_rec_list=[]

def parse2(list1):
    num_people=len(list1)
    #print num_people
    desc="There are "+str(num_people)+" people. "
    for i in xrange(0,num_people):
        age=1.0
        gender=''
        emotion=''
        facialHair=''
        glass=''
        try:
            age=list1[i]["faceAttributes"]["age"]
        except:
            pass
        try:        
            gender=list1[i]["faceAttributes"]["gender"]
        except:
            pass
        try:    
            emotion=check_emotion(list1[i]["faceAttributes"]["emotion"])
        except:
            pass
        try:        
            if list1[i]["faceAttributes"]["glasses"] != "NoGlasses":
                glass = list1[i]["glasses"]
        except:
            pass
        try:            
            if list1[i]["faceAttributes"]["facialHair":]["beard"] > 0.40 :  
                facialHair="bearded"
        except:
            pass
        face_rec_list.append(list1[i]["faceId"])    
        his='her'    
        if gender == 'male':
            his="his"
        a=str(num[i+1])+" person is "+str( math.floor(age))+" year old "+facialHair+" "+gender+". "+his+" mood is "+emotion+". "    
        desc=desc+a  
        if i==6:
            break;
    return desc         

jsoo=''
def Comp_vision(url_photo):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key1,
    }

    params = urllib.urlencode({
        'visualFeatures': 'Categories,Description,Color',
        'language': 'en',
    })

    body = "{'url': '"+url_photo+"'}"

    try:
        # Execute the REST API call and get the response.
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        return parse1(parsed)
        #print ("Response:")
        global jsoo
        #json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()

    except :
        return "sorry don't get any thing"

####################################
def face_api(url_photo):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    })

    # The URL of a JPEG image to analyze.
    body = "{'url':'"+url_photo+"'}"

    try:
        conn = httplib.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()  
        # 'data' contains the JSON data. The following formats the JSON data for display.
        parsed = json.loads(data)
        #print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
        return parse2(parsed)
    except:
        return "sorry don't get any thing"    
 




#print Comp_vision(url)

#print face_api(url)


# Create your views here.
def post_list(request):
    #show_webcam(mirror=True)
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html', {'posts': posts})

cur_img=''
import random

def decoder_(s):
    json_=s.split('?')
    l=len(json_)
    list2=[]
    for i in xrange(l):
        parsed=json.loads(json_[i])
        list2.append(str(parsed["DisplayText"]).lower())
    l=len(list2)
    found1='NO'
    for i in xrange(l):
        cur_text= list2[i].split()
        if ("save" in cur_text) and ( ("image" or "images") in cur_text) and (len(cur_text) > 3):
            found1=cur_text[3]
            break
    return found1


def sample(request):
    s=''
    l=0
    names=''
    if request.method == 'POST':
        global cur_img
        is_save=request.POST.get('save1')
        json_=request.POST.get('save2')
        data= request.POST.get('photo1')
        cur_img=data
        img=base64.b64decode(data[22:])
        p=random.randint(0, 5000)
        filename='./blog/static/sam'+str(p)+'.png'
        s='no'
        l=10
        url='http://ec2-52-39-175-212.us-west-2.compute.amazonaws.com:8087/static/sam'+str(p)+'.png'
        with open(filename,'wb') as f:
            f.write(img)
            s=Comp_vision(url)+" "+face_api(url)
            l=len(s.split())        
        p=decoder_(json_)
        if p!='NO':
            add_in_list(url,p)  
        names=''    
        global face_rec_list
        l1=len(face_rec_list) 
        for i in xrange(l1):
            names=names+" "+find_face(face_rec_list[i])+ " and "
        names=names[:-4]+" is here."
        face_rec_list=[]
        s=s+names

    return render(request, 'blog/audio.html', {'posts': s,'num':l,'name':names})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

