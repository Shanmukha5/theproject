from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
import pyrebase
from django.contrib import auth
import numpy

config = {
    "apiKey": "AIzaSyD7MVWjMWPnyguId_WKdJueN1TMK-8kkc4",
    "authDomain": "the-project-6ca2f.firebaseapp.com",
    "databaseURL": "https://the-project-6ca2f.firebaseio.com",
    "projectId": "the-project-6ca2f",
    "storageBucket": "the-project-6ca2f.appspot.com",
    "messagingSenderId": "28467301382"
  }

firebase= pyrebase.initialize_app(config)

firebaseauth = firebase.auth()

database = firebase.database()

def home(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
		details = database.child('users').child("Company").child(a).child('details').child('name').get().val()
		workeruids = database.child('users').child('worker').get().val()
		javalist = []
		originaljavalist = []
		pythonlist = []
		originalpythonlist = []
		verifiedlist = []
		marketinglist = []
		originalmarketinglist =[]
		webdesignerlist = []
		originalwebdesignerlist = []
		for i in workeruids:
			if(database.child('users').child('worker').child(i).child('verfication').child('verfication').get().val()=='Verified'):
				verifiedlist.append(i)

		for i in verifiedlist:
			if(database.child('users').child('worker').child(i).child('Submitted').child('questionnairepython').get().val()=='Yes'):
				pythonlist.append(i)
			if(database.child('users').child('worker').child(i).child('Submitted').child('questionnairejava').get().val()=='Yes'):
				javalist.append(i)
			if(database.child('users').child('worker').child(i).child('Submitted').child('questionnairemarketing').get().val()=='Yes'):
				marketinglist.append(i)
			if(database.child('users').child('worker').child(i).child('Submitted').child('questionnairewebdesigner').get().val()=='Yes'):
				webdesignerlist.append(i)
			
		javacount = 0
		pythoncount = 0
		marketingcount = 0
		webdesignercount = 0

		for i in numpy.arange(5.0,-1.0,-0.1):
			k = float("{0: .2f}".format(i))
			
			if(javacount<2):
				for p in javalist:
					if(database.child('users').child('worker').child(p).child('rating').child('Java').child('rating').get().val()!=None and int(database.child('users').child('worker').child(p).child('rating').child('Java').child('rating').get().val())==k):
						originaljavalist.append(p)
						javacount = javacount+1

			if(pythoncount<2):
				for p in pythonlist:
					if(database.child('users').child('worker').child(p).child('rating').child('Python').child('rating').get().val()!=None and int(database.child('users').child('worker').child(p).child('rating').child('Python').child('rating').get().val())==k):
						originalpythonlist.append(p)
						pythoncount = pythoncount+1
			
			if(marketingcount<2):
				for p in marketinglist:
					if(database.child('users').child('worker').child(p).child('rating').child('Marketing').child('rating').get().val()!=None and int(database.child('users').child('worker').child(p).child('rating').child('Marketing').child('rating').get().val())==k):
						originalmarketinglist.append(p)
						marketingcount = marketingcount+1

			if(webdesignercount<2):
				for p in webdesignerlist:
					if(database.child('users').child('worker').child(p).child('rating').child('WebDesginer').child('rating').get().val()!=None and int(database.child('users').child('worker').child(p).child('rating').child('Marketing').child('rating').get().val())==k):
						originalwebdesignerlist.append(p)
						webdesignercount = webdesignercount+1


		return render(request,'company/home.html', {'details': details,'originalpythonlist': originalpythonlist, 'originaljavalist': originaljavalist, 'originalmarketinglist': originalmarketinglist, 'originalwebdesignerlist': originalwebdesignerlist})
	except Exception as ex:
		return HttpResponse(ex)
		message = None
		detials = None
		return render(request, 'company/home.html',{'msg': message})


def signup(request):
	message = None
	return render(request, 'company/signup.html',{'msg':message})


def signupsubmit(request):
	name = request.POST.get('name')
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.create_user_with_email_and_password(email, password)
	except Exception as ex:
		message = "Unable to create account. Try again"
		print(ex)
		return render(request, 'company/home.html',{'msg':message})
	uid = user['localId']
	data = {
		'name':name,
		'email':email,
	}
	verfication = {
		'verfication': "Not yet Verified!"
	}
	database.child("users").child('Company').child(uid).child('details').set(data)
	database.child('users').child('Company').child(uid).child('verfication').set(verfication)
	message = "Your account has created successfully. Now Sign in."
	return render(request, 'company/signup.html',{'msg':message})


def signin(request):
	details = None
	return render(request, 'company/signin.html')

def signinsubmit(request):
	email = request.POST.get('email')
	password = request.POST.get('password')
	try:
		user = firebaseauth.sign_in_with_email_and_password(email, password)
	except:
		message = "Invalid Credentials"
		return render(request, 'company/home.html',{'msg':message})
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	b = a['users'][0]['localId']
	data = database.child('users').child('Company').child(b).child('details').child('name').get().val()
	message = "Your are logged in successfully"
	return render(request, 'company/home.html',{"details":data,"msg":message})




def logout(request):
	auth.logout(request)
	return redirect(home)



def submitdoc(request):
	a = None
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
	except Exception as ex:
		a = str(ex)
		if "INVALID_ID_TOKEN" in a:
			return HttpResponse("User Not logged In")
	return render(request, 'company/submitdoc.html')

def submitdocsubmit(request):
	url = request.POST.get('url')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	companyname = request.POST.get('companyname')
	jobrole = request.POST.get('jobrole')
	officialmail = request.POST.get('officialmail')
	websiteurl = request.POST.get('websiteurl')
	phonenumber = request.POST.get('phonenumber')
	gstcode = request.POST.get('gstcode')

	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users']
	a = a[0]
	a = a['localId']
	data = {
		'firstname':firstname,
		'lastname': lastname,
		'companyname': companyname,
		'jobrole': jobrole,
		'officialmail': officialmail,
		'websiteurl': websiteurl,
		'phonenumber': phonenumber,
		'gstcode': gstcode,
		'url':url,
	}
	abc = database.child('users').child("Company").child(a).child('profile').set(data)
	return HttpResponse(abc)





def editprofile(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users']
		a = a[0]
		a = a['localId']
		try:
			editdetails = database.child('users').child("Company").child(a).child('profile').shallow().get().val()
		except:
			return HttpResponse("You haven't submitted your profile yet!")
		firstname = database.child('users').child('Company').child(a).child('profile').child('firstname').get().val()
		lastname = database.child('users').child('Company').child(a).child('profile').child('lastname').get().val()
		companyname = database.child('users').child('Company').child(a).child('profile').child('companyname').get().val()
		jobrole = database.child('users').child('Company').child(a).child('profile').child('jobrole').get().val()
		officialmail = database.child('users').child('Company').child(a).child('profile').child('officialmail').get().val()
		websiteurl = database.child('users').child('Company').child(a).child('profile').child('websiteurl').get().val()
		phonenumber = database.child('users').child('Company').child(a).child('profile').child('phonenumber').get().val()
		gstcode = database.child('users').child('Company').child(a).child('profile').child('gstcode').get().val()
		name = database.child('users').child('Company').child(a).child('details').child('name').get().val()
		return render(request,'company/editprofile.html', {'firstname':firstname, 'lastname': lastname,'phonenumber': phonenumber, 'jobrole': jobrole, 'companyname':companyname, 'officialmail':officialmail, 'websiteurl': websiteurl, 'gstcode': gstcode, 'name': name})
	except:
		return render(request, 'company/editprofile.html')


def editprofilesubmit(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	companyname = request.POST.get('companyname')
	jobrole = request.POST.get('jobrole')
	officialmail = request.POST.get('officialmail')
	websiteurl = request.POST.get('websiteurl')
	phonenumber = request.POST.get('phonenumber')
	gstcode = request.POST.get('gstcode')
	idToken = request.session['uid']
	a = firebaseauth.get_account_info(idToken)
	a = a['users'][0]['localId']
	data = {
		'firstname': firstname,
		'lastname': lastname,
		'companyname': companyname,
		'jobrole': jobrole,
		'officialmail': officialmail,
		'websiteurl': websiteurl,
		'phonenumber': phonenumber,
		'gstcode': gstcode
	}
	database.child('users').child('Company').child(a).child('profile').set(data)
	return HttpResponse("Profile Updated")


def status(request):
	try:
		idToken = request.session['uid']
		a = firebaseauth.get_account_info(idToken)
		a = a['users'][0]['localId']
	except:
		return HttpResponse("User not logged in!")
	status = database.child('users').child('Company').child(a).child('verfication').child('verfication').get().val()
	return render(request, 'company/status.html', {'status': status})


def seeresults(request):
	return render(request, 'company/seeresults.html')


#Checking view for just to check the new implementation techniques

def checking(request):
	return HttpResponse("Checking Point")