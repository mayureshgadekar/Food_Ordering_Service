from django.shortcuts import render, redirect
from foodapp.models import insert_userdata, insert_resdata, signin_userdata, insert_resmenu, signin_resdata, user_page_display, insert_cart, search_res, res_menu_page_display
from django.http import HttpResponse
from django.template import loader, RequestContext 
from django.contrib import messages
from django.contrib import sessions
from collections import defaultdict
import hashlib
from django.contrib.auth.decorators import login_required
import pyodbc

def index(request):
    request.session.flush()
    return render(request,'login_page.html',{'form':'form'})

def user_signin(request):
    request.session.flush()
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method=="POST":
        if request.POST.get('emailid') and request.POST.get('password'):
            insertstvalues=signin_userdata()
            insertstvalues.emailid = request.POST.get('emailid')
            insertstvalues.pass1 = request.POST.get('password')
            insertstvalues.pass1 = hashlib.sha256(insertstvalues.pass1.encode('utf-8')).hexdigest().upper()
            print(insertstvalues.pass1)
            request.session['emailid'] = insertstvalues.emailid
            cursor=conn.cursor()
            cursor.execute("delete from Cart where emailid='"+insertstvalues.emailid+"'")
            cursor.commit()
            #cursor.execute("Select * from user_data where emailid='"+insertstvalues.emailid+"' and password='"+insertstvalues.pass1+"'") 
            cursor.execute("Select * from user_data where emailid=? and password=?", (insertstvalues.emailid,insertstvalues.pass1)) 
            result=cursor.fetchone()
            if result is not None:
                messages.success(request,insertstvalues.emailid)
                return redirect('user_page')
            else:
                return redirect('user_signin')
    return render(request,'signin_page.html',{'form':'form'})


def add_cart(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    emailid=request.session['emailid']
    request.session['emailid'] = emailid
    messages.success(request,emailid)
    res=""
    results = request.POST.get('name_of_item')
    if not request.POST.get('name_of_item') == None:
        res= results.split(",")
    #print(res)  
    r_name=request.POST.get('r_name')
    cursor=conn.cursor()
    #cursor.execute("insert into Cart values('"+emailid+"','"+res[0]+"','"+res[1]+"','"+r_name+"')")
    cursor.execute("insert into Cart values(?,?,?,?)",(emailid,res[0],res[1],r_name))
    cursor.commit()
    #cursor.execute("select Price from Cart where emailid='"+emailid+"'") 
    cursor.execute("select Price from Cart where emailid=?",(emailid))
    total = cursor.fetchall()
    #print (total)
    ov_total = 0
    for k in total:
        ov_total = ov_total + k[0]
    #print(ov_total) 
    request.session['ov_total'] = ov_total 
    return redirect('user_page')
    #return render(request,'user_page.html',{'form': 'form'})


def delete_cart(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    emailid=request.session['emailid']
    request.session['emailid'] = emailid
    messages.success(request,emailid)
    res=""
    results = request.POST.get('name_of_item')
    if not request.POST.get('name_of_item') == None:
        res= results.split(",")
    #print(res)  
    r_name=request.POST.get('r_name')
    #print(r_name)
    cursor=conn.cursor()
    #cursor.execute("Delete from Cart where emailid='"+emailid+"' and Item='"+res[0]+"'")
    cursor.execute("Delete from Cart where emailid=? and Item=?",(emailid,res[0]))
    cursor.commit()
    #cursor.execute("select Price from Cart where emailid='"+emailid+"'")
    cursor.execute("select Price from Cart where emailid=?",(emailid)) 
    total = cursor.fetchall()
    ov_total = 0
    for k in total:
        ov_total = ov_total + k[0]
    #print(ov_total) 
    request.session['ov_total'] = ov_total 
    return redirect('billing')


def user_page(request):
    emailid=request.session['emailid']
    request.session['emailid'] = emailid
    messages.success(request,emailid)
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM menu l INNER JOIN res_data r ON l.r_emailid = r.r_emailid") 
    results = cursor.fetchall()

    list1 = results
    list2 = results
    
    #my_dict = {t[9]: t[:9] for t in results}
    
    dict1 = {value5: [(key, value1, value2, value3, value4, value6, value7, value8, value9)] for key, value1, value2, value3, value4, value5, value6, value7, value8, value9 in list1}
    for key, value1, value2, value3, value4, value5, value6, value7, value8, value9 in list2:
        dict1[value5].append((key, value1, value2, value3, value4, value6, value7, value8, value9))
    
    for k in dict1:
        del dict1[k][0]
    redirect('user_page')
    return render(request,'user_page.html',{'results': dict1})


def billing(request):
    emailid=request.session['emailid']
    request.session['emailid'] = emailid
    messages.success(request,emailid)
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    cursor=conn.cursor()
    #cursor.execute("Select * from Cart where emailid='"+emailid+"' ") 
    cursor.execute("Select * from Cart where emailid=?",(emailid))
    results = cursor.fetchall()
    #print (results)
    list1 = results
    list2 = results
    
    #my_dict = {t[9]: t[:9] for t in results}
    
    dict1 = {value3: [(key, value1, value2)] for key, value1, value2, value3 in list1}
    for key, value1, value2, value3 in list2:
        dict1[value3].append((key, value1, value2))
    
    for k in dict1:
        del dict1[k][0]
    print (dict1)
    return render(request,'billing_page.html',{'results': dict1})

def res_signin(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method=="POST":
        if request.POST.get('r_emailid') and request.POST.get('r_password'):
            insertstvalues=signin_userdata()
            insertstvalues.r_emailid = request.POST.get('r_emailid')
            insertstvalues.r_pass1 = request.POST.get('password')
            insertstvalues.r_pass1 = hashlib.sha256(insertstvalues.r_pass1.encode('utf-8')).hexdigest().upper()
            request.session['r_emailid'] = insertstvalues.r_emailid
            cursor=conn.cursor()
            #cursor.execute("delete from Cart where emailid='"+insertstvalues.emailid+"'")
            cursor.execute("delete from Cart where emailid=?",(insertstvalues.emailid))
            cursor.commit()
            #cursor.execute("Select * from res_data where r_emailid='"+insertstvalues.r_emailid+"' and r_password='"+insertstvalues.r_pass1+"'") 
            cursor.execute("Select * from res_data where r_emailid=? and r_password=?",(insertstvalues.r_emailid,insertstvalues.r_pass1))
            result=cursor.fetchone()
            if result is not None:
                messages.success(request,insertstvalues.emailid)
                redirect('res_menu_display')
            else:
                redirect('res_signin')
    return render(request,'restaurant_signin.html',{'form':'form'})

def delete_res_menu_item(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    r_emailid=request.POST.get('r_emailid')
    res=""
    results = request.POST.get('name_of_item')
    if not request.POST.get('name_of_item') == None:
        res= results.split(",")
    print(res)  
    print(r_emailid)
    cursor=conn.cursor()
    #cursor.execute("Delete from menu WHERE r_emailid='"+r_emailid+"' and Item='"+res[0]+"'")
    cursor.execute("Delete from menu WHERE r_emailid=? and Item=?",(r_emailid,res[0]))
    cursor.commit()
    request.session['r_emailid'] = r_emailid
    return redirect('res_menu_display')
    #return render(request,'res_menu_display.html')

def res_menu_display(request):
    # r_emailid= res_menu_page_display()
    if request.POST.get('r_emailid'):
        r_emailid = request.POST.get('r_emailid')
        request.session['r_emailid'] = r_emailid
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
        cursor=conn.cursor()
        cursor.execute("select * from menu where r_emailid=?",(r_emailid))
        results = cursor.fetchall()
        list1 = results
        list2 = results
        dict1 = {key: [(value1, value2 )] for key, value1, value2 in list1}
        for key, value1, value2 in list2:
            dict1[key].append((value1, value2))
        for k in dict1:
            del dict1[k][0]
        print (dict1)
        return render(request,'res_menu_display.html',{'results': dict1})
    else:
        r_emailid = request.session['r_emailid']
        #r_email = r_emailid
        request.session['r_emailid'] = r_emailid
        #if not request.POST.get('name_of_item') == None:
        #    r_email= r_emailid
        #request.session['r_emailid'] = r_emailid
        #messages.success(request,emailid)
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
        cursor=conn.cursor()
        #cursor.execute("SELECT * FROM menu l INNER JOIN res_data r ON l.r_emailid = r.r_emailid") 
        #cursor.execute("select * from menu where r_emailid= '"+ r_emailid +"' ")
        cursor.execute("select * from menu where r_emailid=?",(r_emailid))
        results = cursor.fetchall()
        list1 = results
        list2 = results
        #my_dict = {t[9]: t[:9] for t in results}
        dict1 = {key: [(value1, value2 )] for key, value1, value2 in list1}
        for key, value1, value2 in list2:
            dict1[key].append((value1, value2))
        for k in dict1:
            del dict1[k][0]
        print (dict1)
    return render(request,'res_menu_display.html',{'results': dict1})





def signout(request):
    request.session.flush()
    # request.session.set_expiry(0)
    # request.session.clear_expired()
    return render(request,'signin_page.html')
    
def signup(request):
    template = loader.get_template('signup.html')
    return HttpResponse(template.render())

# def data_submitted(request):
#     template = loader.get_template('data_submitted.html')
#     return HttpResponse(template.render())
    
def user_reg(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method == 'POST':
        if request.POST.get('emailid') and request.POST.get('password') and request.POST.get('name') and request.POST.get('phone_number') and request.POST.get('address') and request.POST.get('city') and request.POST.get('country'):
            insertstvalues=insert_userdata()
            insertstvalues.emailid=request.POST.get('emailid')
            insertstvalues.password=request.POST.get('password')
            s = insertstvalues.password
            capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            smallalphabets="abcdefghijklmnopqrstuvwxyz"
            specialchar="$@_"
            digits="0123456789"
            l=0
            u=0
            p=0
            d=0
            if (len(s) >= 8):
                for i in s:
            
                    # counting lowercase alphabets
                    if (i in smallalphabets):
                        l+=1           
            
                    # counting uppercase alphabets
                    if (i in capitalalphabets):
                        u+=1           
            
                    # counting digits
                    if (i in digits):
                        d+=1           
            
                    # counting the mentioned special characters
                    if(i in specialchar):
                        p+=1       
            if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s)):
                print("Valid Password")
                insertstvalues.password = hashlib.sha256(insertstvalues.password.encode('utf-8')).hexdigest().upper()
                insertstvalues.name=request.POST.get('name')
                insertstvalues.phone_number=request.POST.get('phone_number')
                insertstvalues.address=request.POST.get('address')
                insertstvalues.city=request.POST.get('city')
                insertstvalues.country=request.POST.get('country')
                ph_num=str(insertstvalues.phone_number)
                cursor=conn.cursor()
                #cursor.execute("insert into user_data values('"+insertstvalues.emailid+"','"+insertstvalues.password+"','"+ insertstvalues.name+"','"+ph_num+"', '"+insertstvalues.address+"', '"+insertstvalues.city+"', '"+insertstvalues.country+"' )")
                cursor.execute("insert into user_data values(?,?,?,?,?,?,?)",(insertstvalues.emailid,insertstvalues.password,insertstvalues.name,ph_num,insertstvalues.address,insertstvalues.city,insertstvalues.country) )
                cursor.commit()
                return redirect('user_signin')
            else:
                print("Invalid Password")
                request.session['invalid_password'] = "Invalid password"
        else:
            return render(request, 'user_registration.html',{'form':'form'})
    return render(request, 'user_registration.html',{'form':'form'})

def restaurant_reg(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method == 'POST':
        if request.POST.get('r_emailid') and request.POST.get('r_password') and request.POST.get('r_name') and request.POST.get('r_phone_number') and request.POST.get('r_address') and request.POST.get('r_city') and request.POST.get('r_country'):
            insertstvalues=insert_resdata()
            insertstvalues.r_emailid=request.POST.get('r_emailid')
            insertstvalues.r_password=request.POST.get('r_password')
            s = insertstvalues.r_password
            capitalalphabets="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            smallalphabets="abcdefghijklmnopqrstuvwxyz"
            specialchar="$@_"
            digits="0123456789"
            l=0
            u=0
            p=0
            d=0
            if (len(s) >= 8):
                for i in s:
            
                    # counting lowercase alphabets
                    if (i in smallalphabets):
                        l+=1           
            
                    # counting uppercase alphabets
                    if (i in capitalalphabets):
                        u+=1           
            
                    # counting digits
                    if (i in digits):
                        d+=1           
            
                    # counting the mentioned special characters
                    if(i in specialchar):
                        p+=1
            if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s)):
                print("Valid Password")
                insertstvalues.r_password = hashlib.sha256(insertstvalues.password.encode('utf-8')).hexdigest().upper()       
                insertstvalues.r_name=request.POST.get('r_name')
                insertstvalues.r_phone_number=request.POST.get('r_phone_number')
                insertstvalues.r_address=request.POST.get('r_address')
                insertstvalues.r_city=request.POST.get('r_city')
                insertstvalues.r_country=request.POST.get('r_country')
                ph_num=str(insertstvalues.r_phone_number)
                cursor=conn.cursor()
                cursor.execute("insert into res_data values(?,?,?,?,?,?,?)",(insertstvalues.r_emailid,insertstvalues.r_password, insertstvalues.r_name, ph_num, insertstvalues.r_address, insertstvalues.r_city,insertstvalues.r_country))
                cursor.commit()            
                return redirect('res_signin')
            else:
                print("Invalid Password")
                request.session['invalid_password'] = "Invalid password"
        else:
            return render(request, 'restaurant_registration.html',{'form':'form'})
    return render(request, 'restaurant_registration.html',{'form':'form'})



def restaurant_menu(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method == 'POST':
        #if request.POST.get('r_emailid') and request.POST.get('Item') and request.POST.get('Price'):
        if request.POST.get('Item') and request.POST.get('Price'):
            insertstvalues=insert_resmenu()
            insertstvalues.Item=request.POST.get('Item')
            insertstvalues.Price=request.POST.get('Price')
            #insertstvalues.r_emailid=request.POST.get('r_emailid')
            Price=str(insertstvalues.Price)
            insertstvalues.r_emailid=request.session['r_emailid']
            request.session['r_emailid'] = insertstvalues.r_emailid
            cursor=conn.cursor()
            #cursor.execute("insert into menu values('"+insertstvalues.r_emailid+"','"+ insertstvalues.Item+"','"+Price+"')")
            cursor.execute("insert into menu values(?,?,?)",(insertstvalues.r_emailid,insertstvalues.Item,Price))
            cursor.commit()
            #return render(request, 'restaurant_page.html',{'form':'form'})
            #messages.success(request,insertstvalues.r_emailid)
            return redirect('restaurant_menu')
        else:
            return redirect('res_signin')
            #return render(request, 'restaurant_page.html',{'form':'form'})
    return render(request,'restaurant_page.html',{'form':'form'})
    #return redirect('restaurant_menu')
    

def payment(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    cursor=conn.cursor()
    emailid=request.session['emailid']
    request.session['emailid'] = emailid
    #cursor.execute("select Price from Cart where emailid='"+emailid+"'") 
    cursor.execute("select Price from Cart where emailid=?",(emailid))
    total = cursor.fetchall()
    ov_total = 0
    for k in total:
        ov_total = ov_total + k[0]
    #print(ov_total) 
    request.session['ov_total'] = ov_total 
    return render(request, 'payment.html',{'ov_total':ov_total})


def search(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    if request.method == 'POST':
        if request.POST.get('search_string'):
            searchvalues=search_res()
            searchvalues.r_name=request.POST.get('search_string')
            #index = searchvalues.r_name.find(searchvalues.r_name)
            # if index != -1:
            #     print("Found the substring at index", index)
            # else:
            #     print("Did not find the substring.")
            searchvalues.Item=request.POST.get('search_string')
            request.session['search_string'] = searchvalues.r_name
            cursor=conn.cursor()
            #cursor.execute("select * from menu l INNER JOIN res_data r ON l.r_emailid = r.r_emailid where r_name='"+searchvalues.r_name+"' ") 
            cursor.execute("select * from menu l INNER JOIN res_data r ON l.r_emailid = r.r_emailid where r_name=?",(searchvalues.r_name))
            search_result = cursor.fetchall()
            if search_result is not None:
                list1 = search_result
                list2 = search_result
                dict1 = {value5: [(key, value1, value2, value3, value4, value6, value7, value8, value9)] for key, value1, value2, value3, value4, value5, value6, value7, value8, value9 in list1}
                for key, value1, value2, value3, value4, value5, value6, value7, value8, value9 in list2:
                    dict1[value5].append((key, value1, value2, value3, value4, value6, value7, value8, value9))
                for k in dict1:
                    del dict1[k][0]   
                return render(request,'user_page.html',{'results': dict1})
    return redirect('user_page')

def order_sum_to_res(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    cursor=conn.cursor()
    r_emailid=""
    r_emailid = request.session['r_emailid']
    request.session['r_emailid'] = r_emailid
    cursor.execute("select * from Cart c INNER JOIN res_data r ON c.r_name = r.r_name where r_emailid=?",(r_emailid))
    order_sum_to_res = cursor.fetchall()
    if order_sum_to_res is not None:
        list1 = order_sum_to_res
        list2 = order_sum_to_res
        dict1 = {key: [(value1, value2, value3,value4,value5,value6,value7,value8,value9,value10)] for key, value1, value2, value3,value4,value5,value6,value7,value8,value9,value10 in list1}
        for key, value1, value2, value3,value4,value5,value6,value7,value8,value9,value10 in list2:
            dict1[key].append((value1, value2, value3,value4,value5,value6,value7,value8,value9,value10))
        for k in dict1:
            del dict1[k][0]
        return render(request,'Order_summary.html',{'results':dict1})
    return render(request,'Order_summary.html')
        
def out_for_delivery(request):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-N1M6BCLV\MSSQLSERVER2019;DATABASE=tomazodb;UID=sa;PWD=toor')
    cursor=conn.cursor()
    emailid=""
    emailid = request.POST.get('emailid')
    res = ""
    results = request.POST.get('name_of_item')
    if not request.POST.get('name_of_item') == None:
        res= results.split(",")
    #print(res)
    #print(emailid)
    cursor.execute("Delete from Cart where emailid=? and Item=?",(emailid,res[0]))
    cursor.commit()
    return redirect('order_sum_to_res')
    
def thankyou(request):
    return render(request, 'thank_you.html')

