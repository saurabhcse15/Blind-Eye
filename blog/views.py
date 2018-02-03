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
        return parse2(parsed)
        #print ("Response:")
        #print (json.dumps(parsed, sort_keys=True, indent=2))
        conn.close()
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

def sample(request):
    if request.method == 'POST':
        global cur_img

        data= request.POST.get('photo1')
        cur_img=data
        img=base64.b64decode(data[22:])
        p=random.randint(0, 5000)
        filename='./blog/static/sam'+str(p)+'.png'
        s='no'
        l=10
        with open(filename,'wb') as f:
            f.write(img)
            url='http://ec2-52-39-175-212.us-west-2.compute.amazonaws.com:8087/static/sam'+str(p)+'.png'
            s=Comp_vision(url)+" '+face_api(url)
            l=len(s.split())        
            
    return render(request, 'blog/audio.html', {'posts': s,'num':l})

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

