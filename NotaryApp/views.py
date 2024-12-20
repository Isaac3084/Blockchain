from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import hashlib
from .models import NotaryDocument, UserProfile
import qrcode
from io import BytesIO
import base64

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
            try:
                fs = FileSystemStorage()
                filename = fs.save(document.name, document)
                
                # Calculate document hash
                hash_md5 = hashlib.md5()
                for chunk in document.chunks():
                    hash_md5.update(chunk)
                document_hash = hash_md5.hexdigest()
                
                # Create document record
                notary_doc = NotaryDocument.objects.create(
                    user=request.user,
                    filename=filename,
                    document_hash=document_hash,
                    pin=pin,
                    details=details
                )
                
                # Generate key pair
                notary_doc.generate_key_pair()
                notary_doc.save()
                
                # Generate QR code with document info and public key
                qr_data = f"""
                Document Hash: {document_hash}
                Public Key: {notary_doc.public_key[:50]}...
                Timestamp: {notary_doc.timestamp}
                """
                
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                # Create QR code image
                qr_img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                qr_img.save(buffer, format="PNG")
                qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                messages.success(request, 
                    f'Document added successfully!<br>'
                    f'Your Private Key (keep secure): {notary_doc.private_key[:50]}...<br>'
                    f'Your Public Key: {notary_doc.public_key[:50]}...<br>'
                    f'<img src="data:image/png;base64,{qr_code_base64}" class="qr-code">'
                )
                return redirect('ViewNotary')
                
            except Exception as e:
                messages.error(request, f'Error processing document: {str(e)}')
                return redirect('AddNotary')
                
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

@login_required
def verify_document(request):
    return render(request, 'NotaryApp/verify_document.html')

@login_required
def verify_document_action(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        pin = request.POST.get('pin')
        document = request.FILES.get('document')

        # Verify user credentials
        user = authenticate(username=request.user.username, password=password)
        if not user or user.email != email:
            messages.error(request, 'Invalid credentials')
            return redirect('verify_document')

        if document:
            # Calculate document hash
            hash_md5 = hashlib.md5()
            for chunk in document.chunks():
                hash_md5.update(chunk)
            document_hash = hash_md5.hexdigest()

            # Try to find the document
            try:
                doc = NotaryDocument.objects.get(
                    user=request.user,
                    document_hash=document_hash,
                    pin=pin
                )
                doc.is_verified = True
                doc.save()
                messages.success(request, 'Document verified successfully!')
                
                # Generate verification QR code
                qr = qrcode.QRCode(version=1, box_size=10, border=5)
                qr_data = f"""
                Document Hash: {document_hash}
                Verified: Yes
                Timestamp: {doc.timestamp}
                Owner: {doc.user.email}
                """
                qr.add_data(qr_data)
                qr.make(fit=True)
                
                # Create QR code image
                qr_img = qr.make_image(fill_color="black", back_color="white")
                buffer = BytesIO()
                qr_img.save(buffer, format="PNG")
                qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
                
                messages.success(request, 
                    f'Verification QR Code:<br>'
                    f'<img src="data:image/png;base64,{qr_code_base64}" class="qr-code">'
                )
                
            except NotaryDocument.DoesNotExist:
                messages.error(request, 'Document not found or PIN incorrect')
        else:
            messages.error(request, 'Please upload a document')
            
    return redirect('verify_document')