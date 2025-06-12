from django.shortcuts import render

posts = [
    {
        'author':'Raj Jivani',
        'title':'Blog Post 1',
        'content':'First Blog Content',
        'date_posted':'June 12,2025'
    },
    {
        'author':'Divyesh Jivani',
        'title':'Blog Post 2',
        'content':'Second Blog Content',
        'date_posted':'June 11,2025'
    }
]

def home(request):
    context = {
        'posts':posts,
        'title':'Home'
    }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title':'About'})

# Create your views here.
