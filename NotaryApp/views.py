from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import hashlib
from .models import NotaryDocument, UserProfile

def index(request):
    return render(request, 'NotaryApp/index.html')

def Login(request):
    return render(request, 'NotaryApp/login.html')

def Signup(request):
    return render(request, 'NotaryApp/signup.html')

def LoginAction(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('t1')
        password = request.POST.get('t2')
        try:
            # First try to get user by username
            user = authenticate(username=username_or_email, password=password)
            
            if user is None:
                # If authentication failed, try to get user by email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('AddNotary')
            else:
                messages.error(request, 'Invalid credentials')
        except Exception as e:
            messages.error(request, f'Login failed: {str(e)}')
        return redirect('Login')
    return redirect('Login')

def SignupAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1')
        password = request.POST.get('t2')
        email = request.POST.get('t3')
        
        try:
            # Create Django user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user
            )
            
            messages.success(request, 'Registration successful')
            return redirect('Login')
            
        except Exception as e:
            messages.error(request, str(e))
            return redirect('Signup')
    return redirect('Signup')

@login_required
def AddNotary(request):
    return render(request, 'NotaryApp/add_notary.html')

@login_required
def AddNotaryAction(request):
    if request.method == 'POST':
        details = request.POST.get('t1')
        pin = request.POST.get('t2')
        document = request.FILES.get('t3')
        
        if document:
            fs = FileSystemStorage()
            filename = fs.save(document.name, document)
            
            # Calculate document hash
            hash_md5 = hashlib.md5()
            for chunk in document.chunks():
                hash_md5.update(chunk)
            document_hash = hash_md5.hexdigest()
            
            # Save document
            NotaryDocument.objects.create(
                user=request.user,
                filename=filename,
                document_hash=document_hash,
                pin=pin,
                details=details
            )
            
            messages.success(request, 'Document added successfully')
            return redirect('ViewNotary')
    return redirect('AddNotary')

@login_required
def ViewNotary(request):
    documents = NotaryDocument.objects.filter(user=request.user)
    return render(request, 'NotaryApp/view_notary.html', {'documents': documents})

@login_required
def delete_notary(request, doc_id):
    if request.method == 'POST':
        try:
            doc = NotaryDocument.objects.get(id=doc_id, user=request.user)
            doc.delete()
            messages.success(request, 'Document deleted successfully')
        except NotaryDocument.DoesNotExist:
            messages.error(request, 'Document not found')
    return redirect('ViewNotary')

def LogoutAction(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('index')