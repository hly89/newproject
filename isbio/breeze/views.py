# -*- coding: utf-8 -*-
import os, copy, tempfile, zipfile, shutil, fnmatch
from datetime import datetime
from collections import OrderedDict
from django.db.models import Q
from django.contrib import auth
from django.core.files import File
from django.core.servers.basehttp import FileWrapper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.context import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.conf import settings
from multiprocessing import Process
from django.utils import simplejson
from dateutil.relativedelta import relativedelta
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt

import xml.etree.ElementTree as xml
import shell as rshell
import auxiliary as aux
import rora as rora

import forms as breezeForms
from breeze.models import Rscripts, Jobs, DataSet, UserProfile, InputTemplate, Report, ReportType, Project, Post, Group, Statistics, Script_categories, CartInfo, User_date, Institute

class RequestStorage():
    form_details = OrderedDict()
    def get_param_list(self):
        class creepy():
            pass
        tmp = creepy()
        plist = list()
        pkeys = self.form_details.keys()
        for key in pkeys:
            tmp.var = self.form_details[key][0].cleaned_data['inline_var']
            tmp.type = self.form_details[key][0].cleaned_data['type']
            plist.append(copy.deepcopy(tmp))
        return plist

    def del_param(self, var):
        del self.form_details[var]

storage = RequestStorage()
storage.progress = 10


def breeze(request):
    return render_to_response('index.html', RequestContext(request, {'layout': 'inline' }))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def register_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    if request.method == 'POST':
        form = breezeForms.RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                    email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            g = Group.objects.get(name='USERS')
            g.user_set.add(user)
            user.is_staff = False
            user.save()
            profile = UserProfile(user=user, first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'], fimm_group=form.cleaned_data['fimm_group'])
            profile.save()
            return render_to_response('forms/welcome_modal.html', RequestContext(request))
        else:
            return render_to_response('forms/register.html', RequestContext(request, {'form': form}))
    else:
        form = breezeForms.RegistrationForm()
        return render_to_response('forms/register.html', RequestContext(request, {'form': form}))

    return 1

def base(request):
    return render_to_response('base.html')

@login_required(login_url='/')
def home(request, state="feed"):
    occurrences = dict()
    #print(state)
    if state == 'feed' or state == None:
        menu = 'feed_menu'
        show_menu = 'show_feed'
        explorer_tab = 'datasets_tab'
        explorer_pane = 'show_datasets'
        pref_tab = 'projects_tab'
        pref_pane = 'show_projects'
        stat_tab = 'analysis_stat_tab'
        stat_pane = 'show_analysis_stat'
    elif state == 'projects':
        menu = 'preferences_menu'
        show_menu = 'show_preferences'
        explorer_tab = 'datasets_tab'
        explorer_pane = 'show_datasets'
        pref_tab = 'projects_tab'
        pref_pane = 'show_projects'
        stat_tab = 'analysis_stat_tab'
        stat_pane = 'show_analysis_stat'
    elif state == 'groups':
        menu = 'preferences_menu'
        show_menu = 'show_preferences'
        explorer_tab = 'datasets_tab'
        explorer_pane = 'show_datasets'
        pref_tab = 'usergroups_tab'
        pref_pane = 'show_usergroups'
        stat_tab = 'analysis_stat_tab'
        stat_pane = 'show_analysis_stat'

    projects = Project.objects.exclude(~Q(author__exact=request.user) & Q(collaborative=False)).order_by("name")
    groups = Group.objects.filter(author__exact=request.user).order_by("name")
    
    # get all the script info
    #rscripts = Rscripts.objects.all().get(draft=True)
    # get all the report info
    stats = Statistics.objects.all()
    occurrences['jobs_running'] = Jobs.objects.filter(juser__exact=request.user).filter(status__exact="active").count()
    occurrences['jobs_scheduled'] = Jobs.objects.filter(juser__exact=request.user).filter(status__exact="scheduled").count()
    occurrences['jobs_history'] = Jobs.objects.filter(juser__exact=request.user).exclude(status__exact="scheduled").exclude(status__exact="active").count()

    occurrences['scripts_total'] = Rscripts.objects.filter(draft="0").count()
    occurrences['scripts_tags'] = Rscripts.objects.filter(draft="0").filter(istag="1").count()

    # Get Screens
    screens = dict() #rora.get_screens_info()

    # Patients
    patients = dict()

    posts = Post.objects.all().order_by("-time")
    return render_to_response('home.html', RequestContext(request, {
        'home_status': 'active',
        str(menu): 'active',
        str(show_menu): 'active',
        str(explorer_tab): 'active',
        str(explorer_pane): 'active',
        str(pref_tab): 'active',
        str(pref_pane): 'active',
        str(stat_tab): 'active',
        str(stat_pane): 'active',
        'dbStat': occurrences,
        'projects': projects,
        'groups': groups,
        'posts': posts,
        'screens': screens,
        'patients': patients,
        'stats': stats
    }))

@login_required(login_url='/')
def jobs(request, state="scheduled"):
    if state == "scheduled":
        tab = "scheduled_tab"
        show_tab = "show_sched"
    else:
        tab = "history_tab"
        show_tab = "show_hist"
    # sheduled scripts
    scheduled_jobs = Jobs.objects.filter(juser__exact=request.user).filter(status__exact="scheduled").order_by("-id")
    history_jobs = Jobs.objects.filter(juser__exact=request.user).exclude(status__exact="scheduled").exclude(status__exact="active").order_by("-id")
    active_jobs = Jobs.objects.filter(juser__exact=request.user).filter(status__exact="active").order_by("-id")
    active_reports = Report.objects.filter(status="active", author__exact=request.user).order_by('-created')
    #print(active_reports)
    merged_active = aux.merge_job_history(active_jobs, active_reports)
    #print(len(merged_active))
    if(len(merged_active)>3):
        merged_active = merged_active[0:3]
    #print(merged_active.count())
    ready_reports = Report.objects.filter(author__exact=request.user).exclude(status__exact="scheduled").exclude(status__exact="active").order_by('-created')
    #ready_reports = Report.objects.exclude(status="active").filter(author__exact=request.user).order_by('-created')

    #merged_history = aux.merge_job_history(history_jobs, ready_reports)

    #paginator = Paginator(merged_history,15)  # show 15 items per page
    paginator = Paginator(history_jobs,15)
    paginator_report = Paginator(ready_reports, 15)
    # If AJAX - check page from the request
    # Otherwise ruturn the first page
    if request.is_ajax() and request.method == 'GET':
        page = request.GET.get('page')
        #print(request.GET)
        if request.GET.get('type')=='script':
            print(request.GET.get('type'))
            try:
                hist_jobs = paginator.page(page)
            except PageNotAnInteger:  # if page isn't an integer
                #print("page isn't an integer")
                hist_jobs = paginator.page(1)
            except EmptyPage:  # if page out of bounds
                hist_jobs = paginator.page(paginator.num_pages)

            return render_to_response('jobs-hist-paginator.html', RequestContext(request, { 'history_script': hist_jobs }))
        else:
            try:
                hist_jobs = paginator_report.page(page)
            except PageNotAnInteger:  # if page isn't an integer
                #print("page isn't an integer")
                hist_jobs = paginator_report.page(1)
            except EmptyPage:  # if page out of bounds
                hist_jobs = paginator_report.page(paginator_report.num_pages)

            return render_to_response('report-hist-paginator.html', RequestContext(request, { 'history_report': hist_jobs }))
        
    else:
        hist_jobs = paginator.page(1)
        print(active_reports)
        if len(merged_active)<=3:
            dash_history = hist_jobs[0:4-len(merged_active)]
        else:
            dash_history = hist_jobs[0]
        return render_to_response('jobs.html', RequestContext(request, {
            str(tab): 'active',
            str(show_tab): 'active',
            'jobs_status': 'active',
            'dash_history': dash_history,
            'scheduled': scheduled_jobs,
            'history_script': history_jobs,
            'history_report': ready_reports,
            'current': merged_active,
            'current_script': active_jobs,
            'current_report': active_reports,
            'pagination_number': paginator.num_pages,
            'pagination_report_number': paginator_report.num_pages,
        }))

@login_required(login_url='/')
def scripts(request, layout="list"):
    if layout == "nails":
        nails = True
    else:
        nails = False
    categories = Script_categories.objects.all()
    # all_scripts = Rscripts.objects.all()
    user = User.objects.get(username=request.user)
    all_scripts = user.users.all()
    cat_list = dict()
    cate = list()
    for each_cate in categories:
        if all_scripts.filter(category=each_cate, istag="0", draft="0").count() > 0:
            cat_list[str(each_cate.category).capitalize()] = all_scripts.filter(category=each_cate, istag="0", draft="0")
            cate.append(str(each_cate.category).capitalize())
    
    #cat_list['reports'] = all_scripts.filter(istag="1")
    #reports = all_scripts.filter(istag="1")
    print(cate)
    report_types = ReportType.objects.filter(access=request.user)
    ''''
    cat_list = dict()
    categories = list()
    for script in all_scripts:
        if str(script.category).capitalize() not in categories:
            categories.append(str(script.category).capitalize())
            cat_list[str(script.category).capitalize()] = Rscripts.objects.filter(category__exact=str(script.category)).filter(draft="0").filter(istag="0")
    '''
    # if request.user.has_perm('breeze.add_rscripts'):
    #    cat_list['_My_Scripts_'] = Rscripts.objects.filter(author__exact=request.user)
    #    cat_list['_Datasets_'] = DataSet.objects.all()
    
    return render_to_response('scripts.html', RequestContext(request, {
        'script_list': all_scripts,
        'scripts_status': 'active',
        'cate': cate,
        'cat_list': sorted(cat_list.iteritems()),
        'reports': report_types,
        'thumbnails': nails
    }))

@login_required(login_url='/')
def reports(request):
    print("i am here")
    all_reports = Report.objects.filter(status="succeed").order_by('-created')
    report_type_lst = ReportType.objects.filter(access=request.user)
    # later all_users will be changed to all users from the same insitute
    all_users = User.objects.all()
    all_projects = Project.objects.all()
    paginator = Paginator(all_reports,30)  # show 3 items per page

    # If AJAX - check page from the request
    # Otherwise ruturn the first page
    if request.is_ajax() and request.method == 'GET':
        page = request.GET.get('page')
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:  # if page isn't an integer
            reports = paginator.page(1)
        except EmptyPage:  # if page out of bounds
            reports = paginator.page(paginator.num_pages)
            print("i love u!")
        return render_to_response('reports-paginator.html', RequestContext(request, { 'reports': reports }))
    else:
        reports = paginator.page(1)
        return render_to_response('reports.html', RequestContext(request, {
            'reports_status': 'active',
            'reports': reports,
            'rtypes': report_type_lst,
            'users': all_users,
            'projects': all_projects,
            'pagination_number': paginator.num_pages
        }))

@login_required(login_url='/')
def dbviewer(request):
    return render_to_response('dbviewer.html', RequestContext(request, {
        'dbviewer_status': 'active',
    }))

def ajax_patients_data(request, which):
    """
        Generic function to extract data from RORA tables;
        Aimed to serve: Patients (ENTITY), Screens and Samples
        in json format for DataTables
    """
    # copy parameters
    params = request.GET

    # Call corresponding rora (R) function
    data_tbl = rora.get_patients_info(params, str(which))

    aadata = data_tbl['aaData']

    iTotalRecords = data_tbl['iTotalRecords']
    iTotalDisplayRecords = data_tbl['iTotalRecords']

    response_data = {
        'draw': int(params.get('draw')),
        'data' : aadata,
        'recordsTotal': iTotalRecords,
        'recordsFiltered': iTotalDisplayRecords
    }

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

def ajax_rora_action(request):

    params = request.POST
    table = params.get('table', '')


    action = params.get('action', '')

    if action == 'remove':
        # Clean up row IDs:
        ids = aux.clean_up_dt_id( params.getlist('id[]', '') )

        if ids and table in ['patients', 'grouSps', 'content', 'screen']:
            feedback = rora.remove_row(table=table, ids=ids)

    elif action == 'create':
        data = dict()
        data['group_name'] = params.get('data[group_name]', '')
        data['group_user'] = params.get('group_author', 'unknown')

        if len(data['group_name']):
            feedback = rora.insert_row(table=table, data=data)

    elif action == 'edit':
        par = [ params.get('id', '') ]
        group = aux.clean_up_dt_id( par )
        screens = params.getlist('screens[]', '')

        if table in ['patients', 'groups']:
            feedback = rora.update_row(table=table, content=screens, iid=group)

    response_data = {}

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
    
@login_required(login_url='/')
def addtocart(request, sid=None):
    # check if this item in the cart already
    try:
        
        scr = Rscripts.objects.get(id = sid)
        #print(scr.author)
        if(scr.author == request.user): return HttpResponse(simplejson.dumps({"author": "Yes"}), mimetype='application/json')
        else:
            items = CartInfo.objects.get(product = sid)
            return HttpResponse(simplejson.dumps({"exist": "Yes"}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        #print("shit")
        scripts = Rscripts.objects.get(id = sid)
        #print(scripts)
        mycart = CartInfo()
        mycart.script_buyer = request.user
        mycart.product = scripts
        if(scripts.price>0): mycart.type_app = False
        else: mycart.type_app = True
        mycart.active = True
        mycart.save()
        return HttpResponse(simplejson.dumps({"exist": "No"}), mimetype='application/json')

@login_required(login_url='/')
def deletecart(request, sid=None):
    #print(sid)
    try:
        items = CartInfo.objects.get(product = sid)
        cate = items.type_app
        #print(cate)
        count_app = CartInfo.objects.filter(type_app=cate).count()
        #print(count_app)
        items.delete()
        #print("he")
        return HttpResponse(simplejson.dumps({"delete": "Yes", 'count_app': count_app}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"delete": "No"}), mimetype='application/json')
        
@login_required(login_url='/')
def install(request, sid=None):
    #print(sid)
    try:
        items = Rscripts.objects.get(id = sid)
        ud = User_date()
        ud.user = request.user
        #ud.install_date= datetime.datetime.today()
        ud.save()
        #print("haha")
        # first check if has already installed
        items_users = items.access.all()
        if request.user in items_users: 
            cate = CartInfo.objects.get(product = sid).type_app
            count_app = CartInfo.objects.filter(type_app=cate).count()
            # delete this app from cart
            CartInfo.objects.get(product = sid).delete()
            #items.install_date.add(ud)
            return HttpResponse(simplejson.dumps({"install_status": "exist", 'count_app':count_app}), mimetype='application/json')
        else:
            items.install_date.add(ud)
            cate = CartInfo.objects.get(product = sid).type_app
            items.access.add(request.user)
            count_app = CartInfo.objects.filter(type_app=cate).count()
            # delete this app from cart
            CartInfo.objects.get(product = sid).delete()
            return HttpResponse(simplejson.dumps({"install_status": "Yes", 'count_app': count_app}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"install_status": "No"}), mimetype='application/json')
    
@login_required(login_url='/')
def deletefree(request):
    print("hello!")
    #print(sid)
    try:
        items = CartInfo.objects.filter(type_app = True)
        #products = CartInfo.objects.filter(type_app = True).values()
        print(items)
        items.delete()
        #print("he")
        return HttpResponse(simplejson.dumps({"delete": "Yes"}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"delete": "No"}), mimetype='application/json')
        
#@login_required(login_url='/')
#@ensure_csrf_cookie
@csrf_exempt
def deletescript(request, sid=None):
    #print(sid)
    #print(request.POST['category'])
    try:
        scr=Rscripts.objects.get(id=sid)
        
        all_scripts = request.user.users.all()
        #print("hi")
        if(request.POST['category']=="all"):
            count_app = request.user.users.all().count()
            #print(count_app)
        elif(request.POST['category']=="reports"):
            count_app = all_scripts.filter(istag="1").count()
            #print(count_app)
        else:
            count_app = all_scripts.filter(category=request.POST['category'].lower(), istag="0", draft="0").count()
        # if scr.author = request.user:
            #scr.delete()
            #return HttpResponse(simplejson.dumps({"delete": "author", "count_app": count_app}), mimetype='application/json')
        # else:
            #scr.access.remove(request.user)
        scr.access.remove(request.user)
        scr.install_date.get(user=request.user).delete()
        return HttpResponse(simplejson.dumps({"delete": "Yes", "count_app": count_app}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"delete": "No"}), mimetype='application/json')
        
@login_required(login_url='/')
def installfree(request):
    #print(sid)
    try:
        items = CartInfo.objects.filter(type_app = True)
        items.delete()
        #print("he")
        return HttpResponse(simplejson.dumps({"delete": "Yes"}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"delete": "No"}), mimetype='application/json')
        
@login_required(login_url='/')
def deletenonfree(request):
    #print(sid)
    try:
        items = CartInfo.objects.filter(type_app = False)
        items.delete()
 
        return HttpResponse(simplejson.dumps({"delete": "Yes"}), mimetype='application/json')
    except CartInfo.DoesNotExist:
        return HttpResponse(simplejson.dumps({"delete": "No"}), mimetype='application/json')
        
def ajax_rora_screens(request, gid):

    response_data = rora.getScreenGroupContent(groupID=gid)

    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')
    
def ajax_user_stat(request):
    timeinfo = User.objects.values_list('date_joined', flat=True)
    # only keep year and month info
    timeinfo = [ each.strftime('%Y-%m') for each in timeinfo]
    # get current time
    current_time = datetime.today()
    # store the date for the last 12 months
    period = [current_time]
    for each_mon in range(1, 12):
        period.append(current_time+ relativedelta(months=-each_mon))
    # format the period
    period = [ each_month.strftime('%Y-%m') for each_month in period]
    
    # sort and group the time info  
    #time_group = sorted(set(timeinfo))
    response_data = {}
    #response_data['result'] = [["Aug", 1], ["Sep", 2],["Oct", 3], ["Noe", 4]]
    for idx, each_group in enumerate(period):
        count = 0
        for each_time in timeinfo:
            if(each_time<=each_group):
                count = count+1
        response_data[idx] = [each_group, count]
    #response_data['message'] = ["Aug", "Sep", "Oct", "Nov"]
    
    return HttpResponse(simplejson.dumps(response_data), mimetype='application/json')

#@csrf_exempt
def reports_search(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = aux.get_query(query_string, ['title', 'body',])

        # found_entries = Entry.objects.filter(entry_query).order_by('-pub_date')

    return render_to_response('search/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries },
                          context_instance=RequestContext(request))


@login_required(login_url='/')
def report_overview(request, rtype, iname, iid=None, mod=None):
    tags_data_list = list()  # a list of 'tag_data' dictionaries
    # filter tags according to report type (here we pick non-draft tags):
    tags = Rscripts.objects.filter(draft="0").filter(istag="1").filter(report_type=ReportType.objects.get(type=rtype)).order_by('order')

    overview = dict()
    overview['report_type'] = rtype
    overview['instance_name'] = iname
    overview['instance_id'] = iid
    overview['details'] = rshell.get_report_overview(rtype, iname, iid)

    if request.method == 'POST':
        # Validates input info and creates (submits) a report
        property_form = breezeForms.ReportPropsForm(request.POST, request=request)
        tags_data_list = breezeForms.validate_report_sections(tags, request)

        sections_valid = breezeForms.check_validity(tags_data_list)

        if property_form.is_valid() and sections_valid:
            rshell.build_report(overview, request, property_form, tags)
            #print(rtype)
            for tag in tags:
                secID = 'Section_dbID_' + str(tag.id)
                if secID in request.POST and request.POST[secID] == '1':
                    # update the statistics table

                    
                    try:
                        stat = Statistics.objects.get(script=tag.name)
                        stat.times += 1
                        stat.save()
                    except Statistics.DoesNotExist:
                        stat = Statistics()
                        stat.script = tag.name
                        stat.author = tag.author
                        stat.istag = tag.istag
                        stat.times = 1
                        stat.save()
                    
                else:
                    pass
                
            return HttpResponse(True)
    else:
        # Renders report overview and available tags
        property_form = breezeForms.ReportPropsForm(request=request)
        tags_data_list = breezeForms.create_report_sections(tags, request)

    return render_to_response('search.html', RequestContext(request, {
        'overview': True,
        'reports_status': 'active',
        'overview_info': overview,
        'props_form': property_form,
        'tags_available': tags_data_list
    }))


@login_required(login_url='/')
def search(request, what=None):
    report_type_lst = ReportType.objects.filter(search=True)
    ds = DataSet.objects.all()
    ds_count = len(ds)

    overview = dict()
    query_val = str()
    overview['report_type'] = str()

    # when query
    if request.method == 'POST':
        result_type = what

        # search for ENTITIES (right bar)
        if what == 'entity':
            report_type = request.POST['type']
            query_val = str(request.POST['query'])
            rtype = ReportType.objects.get(type=report_type)

            if rtype.search:
                # if searchable
                overview['report_type'] = report_type
                output = rshell.report_search(ds, overview['report_type'], query_val)
            else:
                # if not searchable - redirects directly to overview
                if (len(query_val) == 0):
                    query_val = "Noname"
                res = '/reports/overview/%s-%s-00000' % (report_type, query_val)
                return HttpResponseRedirect(res)

        # search for DATASETS (left bar)
        if what == 'dataset':
            output = ds

        return render_to_response('search.html', RequestContext(request, {
            'search_status': 'active',
            'search_bars': True,
            'search_result': True,
            'rtypes': report_type_lst,
            'ds_count': ds_count,
            'result_type': result_type,
            'query_value': query_val,
            'overview_info': overview,
            'output': output
        }))

    else:
        pass

    return render_to_response('search.html', RequestContext(request, {'search_status': 'active', 'search_bars': True, 'ds_count': ds_count, 'rtypes': report_type_lst }))

@login_required(login_url='/')
def resources(request):
    return render_to_response('resources.html', RequestContext(request, {'resources_status': 'active', }))

@login_required(login_url='/')
def manage_scripts(request):
    all_scripts = Rscripts.objects.all()
    paginator = Paginator(all_scripts, 25)
    # If AJAX - check page from the request
    # Otherwise ruturn the first page
    if request.is_ajax() and request.method == 'GET':
        page = request.GET.get('page')
        try:
            scripts = paginator.page(page)
        except PageNotAnInteger:  # if page isn't an integer
            scripts = paginator.page(1)
        except EmptyPage:  # if page out of bounds
            scripts = paginator.page(paginator.num_pages)
        #print("error!")
        return render_to_response('manage-scripts.html', RequestContext(request, { 'script_list': scripts }))
    else:
        scripts = paginator.page(1)
        return render_to_response('manage-scripts.html', RequestContext(request, {
            'resources_status': 'active',
            'script_list': scripts,
            'pagination_number': paginator.num_pages
        }))

@login_required(login_url='/')
def manage_pipes(request):
    all_pipelines = ReportType.objects.all()
    paginator = Paginator(all_pipelines, 10)

    # If AJAX - check page from the request
    # Otherwise ruturn the first page
    if request.is_ajax() and request.method == 'GET':
        page = request.GET.get('page')
        try:
            pipes = paginator.page(page)
        except PageNotAnInteger:  # if page isn't an integer
            pipes = paginator.page(1)
        except EmptyPage:  # if page out of bounds
            pipes = paginator.page(paginator.num_pages)

        return render_to_response('manage-pipelines-paginator.html', RequestContext(request, {'pipe_list': pipes}))
    else:
        pipes = paginator.page(1)
        return render_to_response('manage-pipes.html', RequestContext(request, {
            'resources_status': 'active',
            'pipe_list': pipes,
            'pagination_number': paginator.num_pages
        }))

@login_required(login_url='/')
def dochelp(request):
    return render_to_response('help.html', RequestContext(request, {'help_status': 'active'}))

@login_required(login_url='/')
def abortjobs(request, jid=None):
    try:
        current_jobs = Jobs.objects.filter(status="active")
        if current_jobs:
            count = current_jobs.count()
        abortjob = Jobs.objects.get(id=jid)
        abortjob.status = "aborted"
        abortjob.save()
        return HttpResponse(simplejson.dumps({"abort": "Yes", "count_app": count}), mimetype='application/json')
    except Jobs.DoesNotExist:
        return HttpResponse(simplejson.dumps({"abort": "No"}), mimetype='application/json')
        

@login_required(login_url='/')
def abortreports(request, jid=None):
    try:
        current_report = Report.objects.filter(status="active")
        if current_report:
            count = current_report.count()
        
        abortreport = Report.objects.get(id=jid)
        abortreport.status = "aborted"
        abortreport.save()
        return HttpResponse(simplejson.dumps({"abort": "Yes", "count_app": count}), mimetype='application/json')
    except Report.DoesNotExist:
        return HttpResponse(simplejson.dumps({"abort": "No"}), mimetype='application/json')
    

@login_required(login_url='/')
def store(request):
    categories = Script_categories.objects.all()
    cate = list()
    scripts = Rscripts.objects.filter(draft="0", istag="0")
    count_app = CartInfo.objects.all().count()
    if count_app == 1:
        apps = 'app'
    elif count_app > 1:
        apps = 'apps'
    else:
        apps = ''
    cat_list = dict()
    #categories = list()
    for each_cate in categories:
        if Rscripts.objects.filter(category=each_cate, istag="0", draft="0").count() > 0:
            cat_list[str(each_cate.category).capitalize()] = Rscripts.objects.filter(category=each_cate, istag="0", draft="0")
            cate.append(str(each_cate.category).capitalize())
    
    cat_list['reports'] = Rscripts.objects.filter(istag="1")
    '''
    for script in all_scripts:
        if str(script.category).capitalize() not in categories:
            categories.append(str(script.category).capitalize())
            cat_list[str(script.category).capitalize()] = Rscripts.objects.filter(category__exact=str(script.category)).filter(draft="0").filter(istag="0")
    '''
    return render_to_response('store.html', RequestContext(request, {
        'store_status': 'active',
        'cate': cate,
        'script_list': scripts,
        'cat_list': sorted(cat_list.iteritems()),
        'count_mycart': count_app,
        'apps':apps
    }))
    
@login_required(login_url='/')
def mycart(request):
    #print("ha!")
    #all_items = CartInfo.objects.filter(script_buyer=request.user)
    items_free = CartInfo.objects.filter(script_buyer=request.user, type_app=True)
    items_nonfree = CartInfo.objects.filter(script_buyer=request.user, type_app=False)
    html = render_to_string('cartinfo.html', {
        #'mycart_status': 'active',
        'items_free': items_free,
        'items_nonfree': items_nonfree
        #'all_items': all_items 
    })
    return HttpResponse(html)
    
@login_required(login_url='/')
def updatecart(request):
    count_mycart = CartInfo.objects.filter(script_buyer=request.user).count()
    html = render_to_string('countcart.html', {'count_mycart': count_mycart})
    return HttpResponse(html)
    #return render_to_response('base.html', RequestContext(request, {
        #'count_mycart': count_mycart,
        #'store_status': 'active'
    #}))

######################################
###      SUPPLEMENTARY VIEWS       ###
######################################

@login_required(login_url='/')
def script_editor(request, sid=None, tab=None):
    script = Rscripts.objects.get(id=sid)

    f_basic = breezeForms.ScriptBasics(edit=script.name, initial={'name': script.name, 'inline': script.inln })
    f_attrs = breezeForms.ScriptAttributes(instance=script)
    f_logos = breezeForms.ScriptLogo()

    if tab is None:
        tab = '-general_tab'

    return render_to_response('script-editor.html', RequestContext(request, {
        str(tab)[1:]: 'active',
        'resources_status': 'active',
        'script': script,
        'basic_form': f_basic,
        'attr_form': f_attrs,
        'logo_form': f_logos
    }))




@login_required(login_url='/')
def script_editor_update(request, sid=None):
    if request.method == 'POST':
        script = Rscripts.objects.get(id=sid)

        # General Tab
        if request.POST['form_name'] == 'general':
            f_basic = breezeForms.ScriptBasics(script.name, request.POST)
            if f_basic.is_valid():
                rshell.update_script_dasics(script, f_basic)
                return HttpResponseRedirect('/resources/scripts/script-editor/' + str(script.id) + '-general_tab')
        else:
            f_basic = breezeForms.ScriptBasics(edit=script.name, initial={'name': script.name, 'inline': script.inln })

        # Description Tab
        if request.POST['form_name'] == 'description' and request.is_ajax():
            return HttpResponse(rshell.update_script_description(script, request.POST))
        else:
            pass

        # Attributes Tab
        if request.POST['form_name'] == 'attributes':
            f_attrs = breezeForms.ScriptAttributes(request.POST, instance=script)
            if f_attrs.is_valid():
                f_attrs.save()
                script.creation_date = datetime.now()
                script.save()
                return HttpResponseRedirect('/resources/scripts/script-editor/' + str(script.id) + '-attribut_tab')
        else:
            f_attrs = breezeForms.ScriptAttributes(instance=script)

        # Form Builder Tab
        if request.POST['form_name'] == 'xml_data' and request.is_ajax():
            return HttpResponse(rshell.update_script_xml(script, request.POST['xml_data']))
        else:
            pass  # return HttpResponse(False)

        # Sources Tab
        if request.POST['form_name'] == 'source_files' and request.is_ajax():
            rshell.update_script_sources(script, request.POST)
            return HttpResponse(True)
        else:
            pass  # return HttpResponse(False)

        # Logos Tab
        if request.POST['form_name'] == 'logos':
            f_logos = breezeForms.ScriptLogo(request.POST, request.FILES)
            if f_logos.is_valid():
                rshell.update_script_logo(script, request.FILES['logo'])
                return HttpResponseRedirect('/resources/scripts/script-editor/' + str(script.id) + '-logos_tab')
        else:
            f_logos = breezeForms.ScriptLogo()

        return render_to_response('script-editor.html', RequestContext(request, {
                'resources_status': 'active',
                'script': script,
                'basic_form': f_basic
                # 'attr_form': f_attrs,
                # 'logo_form': f_logos
            }))
    # if NOT POST
    return HttpResponseRedirect('/resources/scripts/script-editor/' + script.id)

@login_required(login_url='/')
def get_form(request, sid=None):
    script = Rscripts.objects.get(id=sid)
    builder_form = ""

    if request.method == 'GET' and sid is not None:
        file_path = rshell.settings.MEDIA_ROOT + str(script.docxml)

        if os.path.isfile(file_path):
            tree = xml.parse(file_path)
            if tree.getroot().find('builder') is not None:
                builder_form = tree.getroot().find('builder').text
            else:
                builder_form = "False"
        else:
            builder_form = "False"

    return HttpResponse(builder_form)


@login_required(login_url='/')
def get_rcode(request, sid=None, sfile=None):
    script = Rscripts.objects.get(id=sid)
    rcode = ""
    if request.method == 'GET' and sid is not None:

        if sfile == 'Header':
            file_path = rshell.settings.MEDIA_ROOT + str(script.header)
        elif sfile == 'Main':
            file_path = rshell.settings.MEDIA_ROOT + str(script.code)

        if os.path.isfile(file_path):
            handle = open(file_path, 'r')
            rcode = handle.read()
            handle.close()
        else:
            rcode = "file does not exist"

    return HttpResponse(rcode)

@login_required(login_url='/')
def delete_job(request, jid):
    job = Jobs.objects.get(id=jid)
    if (job.status == "scheduled"):
        tab = ""
    else:
        tab = "history"
    rshell.del_job(job)
    return HttpResponseRedirect('/jobs/' + tab)

@login_required(login_url='/')
def delete_script(request, sid):
    script = Rscripts.objects.get(id=sid)
    rshell.del_script(script)
    return HttpResponseRedirect('/resources/scripts/')

@login_required(login_url='/')
def delete_pipe(request, pid):
    pipe = ReportType.objects.get(id=pid)
    rshell.del_pipe(pipe)
    return HttpResponseRedirect('/resources/pipes/')

@login_required(login_url='/')
def delete_report(request, rid, redir):

    if redir == '-dash':
        redir = '/jobs/history'
    else:
        redir = '/reports/'

    report = Report.objects.get(id=rid)
    rshell.del_report(report)
    return HttpResponseRedirect(redir)

@login_required(login_url='/')
def delete_project(request, pid):
    project = Project.objects.get(id=pid)
    aux.delete_project(project)

    return HttpResponseRedirect('/home/projects')

@login_required(login_url='/')
def delete_group(request, gid):
    group = Group.objects.get(id=gid)
    aux.delete_group(group)

    return HttpResponseRedirect('/home/groups')

@login_required(login_url='/')
def read_descr(request, sid=None):
    script = Rscripts.objects.get(id=sid)
    return render_to_response('forms/descr_modal.html', RequestContext(request, { 'scr': script }))

@login_required(login_url='/')
def edit_job(request, jid=None, mod=None):
    job = Jobs.objects.get(id=jid)
    tree = xml.parse(str(settings.MEDIA_ROOT) + str(job.docxml))
    user_info = User.objects.get(username=request.user)

    if mod is not None:
        mode = 'replicate'
        tmpname = str(job.jname) + '_REPL'
        edit = ""
    else:
        mode = 'edit'
        tmpname = str(job.jname)
        edit = str(job.jname)

    if request.method == 'POST':
        head_form = breezeForms.BasicJobForm(request.user, edit, request.POST)
        custom_form = breezeForms.form_from_xml(xml=tree, req=request, usr=request.user)
        if head_form.is_valid() and custom_form.is_valid():

            if mode == 'replicate':
                tmpscript = job.script
                job = Jobs()
                job.script = tmpscript
                job.status = "scheduled"
                job.juser = request.user
                job.progress = 0
            else:
                loc = rshell.get_job_folder(str(job.jname), str(job.juser.username))
                shutil.rmtree(loc)

            rshell.assemble_job_folder(str(head_form.cleaned_data['job_name']), str(request.user), tree, custom_form,
                                                    str(job.script.code), str(job.script.header), request.FILES)

            job.jname = head_form.cleaned_data['job_name']
            job.jdetails = head_form.cleaned_data['job_details']

            job.rexecut.save('name.r', File(open(str(settings.TEMP_FOLDER) + 'rexec.r')))
            job.docxml.save('name.xml', File(open(str(settings.TEMP_FOLDER) + 'job.xml')))
            job.rexecut.close()
            job.docxml.close()

            rshell.schedule_job(job, request.POST)

            # improve the manipulation with XML - tmp folder not a good idea!
            os.remove(str(settings.TEMP_FOLDER) + 'job.xml')
            os.remove(str(settings.TEMP_FOLDER) + 'rexec.r')
            return HttpResponseRedirect('/jobs')
    else:
        head_form = breezeForms.BasicJobForm(user=request.user, edit=str(job.jname), initial={'job_name': str(tmpname), 'job_details': str(job.jdetails)})
        custom_form = breezeForms.form_from_xml(xml=tree, usr=request.user)

    return render_to_response('forms/user_modal.html', RequestContext(request, {
        'url': "/jobs/edit/" + str(jid),
        'name': str(job.script.name),
        'inline': str(job.script.inln),
        'headform': head_form,
        'custform': custom_form,
        'layout': "horizontal",
        'mode': mode,
        'email': user_info.email
    }))

@login_required(login_url='/')
def create_job(request, sid=None):
    script = Rscripts.objects.get(id=sid)

    new_job = Jobs()
    tree = xml.parse(str(settings.MEDIA_ROOT) + str(script.docxml))
    script_name = str(script.name)  # tree.getroot().attrib['name']
    script_inline = script.inln
    user_info = User.objects.get(username=request.user)
    #print(request.method)
    if request.method == 'POST':
        # after fill the forms for creating the new job
        head_form = breezeForms.BasicJobForm(request.user, None, request.POST)
        custom_form = breezeForms.form_from_xml(xml=tree, req=request, usr=request.user)

        if head_form.is_valid() and custom_form.is_valid():
            rshell.assemble_job_folder(str(head_form.cleaned_data['job_name']), str(request.user), tree, custom_form,
                                                    str(script.code), str(script.header), request.FILES)
            new_job.jname = head_form.cleaned_data['job_name']
            new_job.jdetails = head_form.cleaned_data['job_details']
            new_job.script = script
            new_job.status = request.POST['job_status']
            new_job.juser = request.user
            new_job.progress = 0
            new_job.rexecut.save('name.r', File(open(str(settings.TEMP_FOLDER) + 'rexec.r')))
            new_job.docxml.save('name.xml', File(open(str(settings.TEMP_FOLDER) + 'job.xml')))
            new_job.rexecut.close()
            new_job.docxml.close()


            rshell.schedule_job(new_job, request.POST)
            try:
                stat = Statistics.objects.get(script=script.name)
                stat.times += 1
                stat.save()
            except Statistics.DoesNotExist:
                stat = Statistics()
                stat.script = script.name
                stat.author = script.author
                stat.istag = script.istag
                stat.times = 1
                stat.save()

            # improve the manipulation with XML - tmp folder not a good idea!
            os.remove(str(settings.TEMP_FOLDER) + 'job.xml')
            os.remove(str(settings.TEMP_FOLDER) + 'rexec.r')

            if 'run_job' in request.POST:
                p = Process( target=rshell.run_job, args=(new_job,) )
                p.start()
                #print("running jobs")
            #return HttpResponseRedirect('/home/')
            return HttpResponseRedirect('/jobs/')
    else:
        head_form = breezeForms.BasicJobForm(user=request.user, edit=None)
        custom_form = breezeForms.form_from_xml(xml=tree, usr=request.user)

    return render_to_response('forms/user_modal.html', RequestContext(request, {
        'url': "/scripts/apply-script/" + str(sid),
        'name': script_name,
        'inline': script_inline,
        'headform': head_form,
        'custform': custom_form,
        'layout': "horizontal",
        'mode': 'create',
        'email': user_info.email
    }))

@login_required(login_url='/')
def run_script(request, jid):
    job = Jobs.objects.get(id=jid)
    script = str(job.script.code)
    p = Process(target=rshell.run_job, args=(job, script))
    p.start()

    return HttpResponseRedirect('/jobs/')

@login_required(login_url='/')
def delete_param(request, which):
    storage.del_param(which)
    local_representation = storage.get_param_list()
    return render_to_response('new-script.html', RequestContext(request, {
            'hidden_form': storage.hidden_form,
            'general_form': storage.form_general,
            'params_form': local_representation,
            'source_form': storage.form_sources,
            'layout': 'inline',
            'curr_tab': 'params',
            'status': 'info',
        }))

@login_required(login_url='/')
def append_param(request, which):
    basic_form = breezeForms.AddBasic(request.POST or None)
    extra_form = None
    extra_form_valid = True
    if which == 'NUM':
        msg = 'NUMERIC'
    elif which == 'CHB':
        msg = 'CHECK BOX'
    elif which == 'DRP':
        msg = 'DROP DOWN'
        extra_form = breezeForms.AddOptions(request.POST or None)
        extra_form_valid = extra_form.is_valid()
    elif which == 'RAD':
        msg = 'RADIO BUTTONS'
        extra_form = breezeForms.AddOptions(request.POST or None)
        extra_form_valid = extra_form.is_valid()
    elif which == 'TEX':
        msg = 'TEXT INPUT'
    elif which == 'TAR':
        msg = 'TEXT AREA'
    elif which == 'FIL':
        msg = 'FILE INPUT'
    elif which == 'HED':
        msg = 'SECTION NAME'
    elif which == 'TPL':
        msg = 'TEMPLATE INPUT'
        extra_form = breezeForms.AddTemplateInput(request.POST or None)
        extra_form_valid = extra_form.is_valid()
    elif which == 'DTS':
        msg = 'DATASET SELECTOR'
        extra_form = breezeForms.AddDatasetSelect(request.POST or None)
        extra_form_valid = extra_form.is_valid()
    else:
        pass

    if basic_form.is_valid() and extra_form_valid:
        # implement adding new param as a separate function in STORAGE class
        storage.form_details[str(basic_form.cleaned_data['inline_var'])] = list()
        storage.form_details[str(basic_form.cleaned_data['inline_var'])].append(basic_form)
        storage.form_details[str(basic_form.cleaned_data['inline_var'])].append(extra_form)
        local_representation = storage.get_param_list()
        return render_to_response('new-script.html', RequestContext(request, {
            'hidden_form': storage.hidden_form,
            'general_form': storage.form_general,
            'params_form': local_representation,
            'source_form': storage.form_sources,
            'layout': 'inline',
            'curr_tab': 'params',
            'status': 'info',
        }))
    return render_to_response('forms/new_param_modal.html', RequestContext(request, {
        'msg': msg, 'basic': basic_form, 'extra': extra_form, "type": which,
    }))

@login_required(login_url='/')
@permission_required('breeze.add_rscripts', login_url="/")
def create_script(request):
    tab = 'general'
    if request.method == 'POST':
        storage.hidden_form = breezeForms.HiddenForm(request.POST)
        tab = storage.hidden_form['next'].value()
        if storage.hidden_form['curr'].value() == 'general':
            storage.form_general = breezeForms.ScriptMainForm(request.POST, request.FILES)
            storage.form_general.is_valid()
            local_representation = storage.get_param_list()
        elif storage.hidden_form['curr'].value() == 'params':
            local_representation = storage.get_param_list()
        elif storage.hidden_form['curr'].value() == 'source':
            storage.form_sources = breezeForms.ScriptSources(request.POST, request.FILES)
            local_representation = storage.get_param_list()
            if storage.form_sources.is_valid():
                storage.code = request.FILES['code']
        elif storage.hidden_form['curr'].value() == 'summary':
            pass
    else:
        storage.hidden_form = breezeForms.HiddenForm()
        storage.form_general = breezeForms.ScriptMainForm()
        storage.form_details = OrderedDict()
        local_representation = storage.get_param_list()
        storage.form_sources = breezeForms.ScriptSources()

    return render_to_response('new-script.html', RequestContext(request, {
        'hidden_form': storage.hidden_form,
        'general_form': storage.form_general,
        'params_form': local_representation,
        'source_form': storage.form_sources,
        'layout': 'inline',
        'curr_tab': tab,
        'status': 'info',
        'scripts_status': 'active',
        }))

@login_required(login_url='/')
def save(request):
    # validate form_details also somehow in the IF below
    if  storage.form_general.is_valid() and storage.form_sources.is_valid():
        # .xml_from_form() - creates doc in tmp for now
        breezeForms.xml_from_form(storage.form_general, storage.form_details, storage.form_sources)
        rshell.build_header(storage.form_sources.cleaned_data['header'])

        dbinst = storage.form_general.save(commit=False)

        dbinst.author = request.user
        dbinst.code = storage.code
        dbinst.docxml.save('name.xml', File(open(str(settings.TEMP_FOLDER) + 'test.xml')))
        dbinst.header.save('name.txt', File(open(str(settings.TEMP_FOLDER) + 'header.txt')))

        dbinst.save()

        # improve the manipulation with XML - tmp folder not a good idea!
        os.remove(str(settings.TEMP_FOLDER) + 'test.xml')
        os.remove(str(settings.TEMP_FOLDER) + 'header.txt')

        return HttpResponseRedirect('/scripts/')
    else:
        # need an error handler here!
        return HttpResponseRedirect('/scripts/')

def show_rcode(request, jid):
    job = Jobs.objects.get(id=jid)
    docxml = xml.parse(str(settings.MEDIA_ROOT) + str(job.docxml))
    script = job.jname  # docxml.getroot().attrib["name"]
    inline = job.script.inln  # docxml.getroot().find('inline').text

    fields = list()
    values = list()
    input_array = docxml.getroot().find('inputArray')
    if input_array != None:
        for input_item in input_array:
            fields.append(input_item.attrib["comment"])
            values.append(input_item.attrib["val"])
    parameters = zip(fields, values)

    return render_to_response('forms/code_modal.html', RequestContext(request, {
        'name': str(job.jname),
        'script': script,
        'inline': inline,
        'description': str(job.jdetails),
        'input': parameters,
    }))

def veiw_project(request, pid):
    project = Project.objects.get(id=pid)
    context = { 'project': project }

    return render_to_response('forms/project_info.html', RequestContext(request, context))

def view_group(request, gid):
    group = Group.objects.get(id=gid)
    context = { 'group': group }

    return render_to_response('forms/group_info.html', RequestContext(request, context))

@login_required(login_url='/')
def send_zipfile(request, jid, mod=None):
    job = Jobs.objects.get(id=jid)
    loc = rshell.get_job_folder(str(job.jname), str(job.juser.username))
    files_list = os.listdir(loc)
    zipname = 'attachment; filename=' + str(job.jname) + '.zip'

    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)

    if mod is None:
        for item in files_list:
            archive.write(loc + item, str(item))
    elif mod == "-code":
        for item in files_list:
            if fnmatch.fnmatch(item, '*.r') or fnmatch.fnmatch(item, '*.Rout'):
                archive.write(loc + item, str(item))
    elif mod == "-result":
        for item in files_list:
            if not fnmatch.fnmatch(item, '*.xml') and not fnmatch.fnmatch(item, '*.r*') and not fnmatch.fnmatch(item, '*.sh*'):
                archive.write(loc + item, str(item))

    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = zipname  # 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response

@login_required(login_url='/')
def send_template(request, name):
    template = InputTemplate.objects.get(name=name)
    path_to_file = str(settings.MEDIA_ROOT) + str(template.file)
    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(myfile, mimetype='application/force-download')
    folder, slash, file = str(template.file).rpartition('/')
    response['Content-Disposition'] = 'attachment; filename=' + file
    return response

@login_required(login_url='/')
def send_file(request, ftype, fname):
    """
        Supposed to be generic function that can send single file to client.
        Each IF case prepare dispatch data of a certain type.
        ! Should supbstitute send_template() function soon !
    """
    if ftype == 'dataset':
        fitem = DataSet.objects.get(name=str(fname))
        local_path = str(fitem.rdata)
        path_to_file = str(settings.MEDIA_ROOT) + local_path

    if ftype == 'report':
        fitem = Report.objects.get(id=fname)
        local_path = fitem.home + '/report.html'
        path_to_file = str(settings.MEDIA_ROOT) + local_path

    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(myfile, mimetype='application/force-download')
    folder, slash, file = local_path.rpartition('/')
    response['Content-Disposition'] = 'attachment; filename=' + file
    return response

@login_required(login_url='/')
def update_jobs(request, jid, item):
    if item == 'script':
        sge_status = rshell.track_sge_job(Jobs.objects.get(id=jid))
        # request job instance again to be sure that the data is updated
        job = Jobs.objects.get(id=jid)
        
        response = dict(id=job.id, name=str(job.jname), staged=str(job.staged), status=str(job.status), progress=job.progress, sge=sge_status)
    else:
        sge_status = rshell.track_sge_job(Report.objects.get(id=jid))
        # request job instance again to be sure that the data is updated
        report = Report.objects.get(id=jid)
        #report = rshell.run_report(report)
        report.status = "succeed"
        response = dict(id=report.id, name=str(report.name), staged=str(report.created), status=str(report.status), progress=report.progress, sge=sge_status)


    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

@login_required(login_url='/')
def send_dbcontent(request, content, iid=None):
    response = dict()

    if content == "datasets":
        clist = DataSet.objects.all()
    elif content == "templates":
        clist = InputTemplate.objects.all()
    elif content == "description":
        script = Rscripts.objects.get(id=int(iid[1:]))
        response["description"] = script.details
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')
    else:
        # return empty dictionary if content was smth creepy
        return HttpResponse(simplejson.dumps(response), mimetype='application/json')

    for item in clist:
        response[item.name] = item.description

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')


@login_required(login_url='/')
def builder(request):
    form = breezeForms.ScriptMainForm()
    return render_to_response('form-builder.html', RequestContext(request, {'forma': form, }))


@login_required(login_url='/')
def new_script_dialog(request):
    """
        This view provides a dialog to create a new script and save new script in DB.
        If script name is valid, the view creates an instance in DB which has the following fields completed:
        Name, Category, Creation Date, Author and Script's root folder.
    """
    form = breezeForms.NewScriptDialog(request.POST or None)

    if form.is_valid():
        sname = str(form.cleaned_data.get('name', None))
        sinline = str(form.cleaned_data.get('inline', None))
        newpath = rshell.init_script(sname, sinline, request.user)
        #print(newpath)
        return HttpResponseRedirect('/resources/scripts/')

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': form,
        'action': '/new-script/',
        'header': 'Create New Script',
        'layout': 'horizontal',
        'submit': 'Add'
    }))

@login_required(login_url='/')
def new_rtype_dialog(request):
    """
        This view provides a dialog to create a new report type in DB.
    """
    form = breezeForms.NewRepTypeDialog(request.POST or None)

    if form.is_valid():
        rshell.init_pipeline(form, request.user)
        return HttpResponse(True)

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': form,
        'action': '/new-rtype/',
        'header': 'Create New Report Type',
        'layout': 'horizontal',
        'submit': 'Add'
    }))
    
@login_required(login_url='/')
def new_cate_dialog(request):
    """
        This view provides a dialog to create a new category in DB.
    """
    form = breezeForms.NewCategoryDialog(request.POST or None)

    if form.is_valid():
        #rshell.init_pipeline(form)
        new_cate = Script_categories()
        new_cate = form.save()
        return HttpResponse(True)

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': form,
        'action': '/new-cate/',
        'header': 'Create New Category',
        'layout': 'horizontal',
        'submit': 'Add'
    }))
    


@login_required(login_url='/')
def new_project_dialog(request):
    """
        This view provides a dialog to create a new Project in DB.
    """
    project_form = breezeForms.NewProjectForm(request.POST or None)
    print("first time")
    if project_form.is_valid():
        print("second time")
        aux.save_new_project(project_form, request.user)
        return HttpResponseRedirect('/home/projects')

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': project_form,
        'action': '/projects/create',
        'header': 'Create New Project',
        'layout': 'horizontal',
        'submit': 'Save'
    }))

@login_required(login_url='/')
def new_group_dialog(request):
    """
        This view provides a dialog to create a new Group in DB.
    """
    group_form = breezeForms.GroupForm(request.POST or None)

    if group_form.is_valid():
        aux.save_new_group(group_form, request.user, request.POST)
        return HttpResponseRedirect('/home/groups')

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': group_form,
        'action': '/groups/create',
        'header': 'Create New Group',
        'layout': 'horizontal',
        'submit': 'Save'
    }))

@login_required(login_url='/')
def edit_project_dialog(request, pid):
    """
        This view provides a dialog to create a new Project in DB.
    """
    project_data = Project.objects.get(id=pid)
    form_action = '/projects/edit/' + str(pid)
    form_title = 'Edit Project: ' + str(project_data.name)

    if request.method == 'POST':
        project_form = breezeForms.EditProjectForm(request.POST)
        if project_form.is_valid():
            aux.edit_project(project_form, project_data)
            return HttpResponseRedirect('/home/projects')
    else:
        project_form = breezeForms.EditProjectForm(
            initial={'eid': project_data.external_id, 'wbs': project_data.wbs, 'description': project_data.description}
        )

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': project_form,
        'action': form_action,
        'header': form_title,
        'layout': 'horizontal',
        'submit': 'Save'
    }))

@login_required(login_url='/')
def edit_group_dialog(request, gid):
    """
        This view provides a dialog to edit an existing Group in DB.
    """
    group_data = Group.objects.get(id=gid)
    form_action = '/groups/edit/' + str(gid)
    form_title = 'Edit Group: ' + str(group_data.name)

    if request.method == 'POST':
        group_form = breezeForms.EditGroupForm(request.POST)
        if group_form.is_valid():
            aux.edit_group(group_form, group_data, request.POST)
            return HttpResponseRedirect('/home/groups')
    else:
        team = {}
        for arr in group_data.team.all():
            team[arr.id] = True

        group_form = breezeForms.EditGroupForm(initial={'group_team': team})

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form':   group_form,
        'action': form_action,
        'header': form_title,
        'layout': 'horizontal',
        'submit': 'Save'
    }))

@login_required(login_url='/')
def update_user_info_dialog(request):
    user_info = User.objects.get(username=request.user)
    user_details = UserProfile.objects.get(user=user_info.id)
    #print(request.method)
    if request.method == 'POST':
        personal_form = breezeForms.PersonalInfo(request.POST)
        print("personal_form")
        if personal_form.is_valid():
            user_info.first_name = personal_form.cleaned_data.get('first_name', None)
            user_info.last_name = personal_form.cleaned_data.get('last_name', None)
            user_info.email = personal_form.cleaned_data.get('email', None)
            #user_details.fimm_group = personal_form.cleaned_data.get('group', None)
            #print(int(personal_form.cleaned_data.get('institute', None)))
            user_details.institute_info = Institute.objects.get(id=request.POST['institute'])
            #print(personal_form.cleaned_data.get('institute', None))
            user_info.save()
            user_details.save()
            return HttpResponseRedirect('/home')

    else:
        #print(user_details.institute_info)
        institute = tuple((user_details.institute_info.id,user_details.institute_info.institute))
        print(institute)
        personal_form = breezeForms.PersonalInfo(initial={'first_name': user_info.first_name, 'last_name': user_info.last_name, 'email': user_info.email,'institute': user_details.institute_info.id})
        print(personal_form)

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': personal_form,
        'action': '/update-user-info/',
        'header': 'Update Personal Info',
        'layout': 'horizontal',
        'submit': 'Save'
    }))

@login_required(login_url='/')
@csrf_exempt
def new_institute(request):
    user_info = User.objects.get(username=request.user)
    print(user_info)
    user_details = UserProfile.objects.get(user=user_info.id)
    print(request.is_ajax())
    if request.method == 'POST':
        personal_form = breezeForms.NewInstitute(request.POST)
        if personal_form.is_valid():
            insti = Institute()
            insti.institute = request.POST['name']
            #print(personal_form.cleaned_data.get('institute', None))
            insti.save()
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect('/home')

    else:
        #print(user_details.institute_info)
        #institute = tuple((user_details.institute_info.id,user_details.institute_info.institute))
        #print(user_details.institute_info.institute)
        institue_form = breezeForms.NewInstitute(initial={'name': user_details.institute_info.institute})
        print(institue_form)

    return render_to_response('forms/basic_form_dialog.html', RequestContext(request, {
        'form': institue_form,
        'action': '/new-institute/',
        'header': 'Create New Institute',
        'layout': 'horizontal',
        'submit': 'Save'
    }))
    



@login_required(login_url='/')
def report_search(request):
    #print("haha")
    query_string = ''
    found_entries = None
    entry_query = None
    # report_type_lst = ReportType.objects.all()
    #print(request.POST)
    if 'reset' in request.POST:
        all_reports = Report.objects.filter(status="succeed").order_by('-created')
        paginator = Paginator(all_reports,30)
        found_entries = paginator.page(1)
    else:
        if ('filt_name' in request.POST) and request.POST['filt_name'].strip():
            query_string = request.POST['filt_name']
            entry_query = aux.get_query(query_string, ['name'])
            #print(entry_query)
            #found_entries = Report.objects.filter(entry_query, status="succeed").order_by('-created')
        # filter by type
        if ('filt_type' in request.POST) and request.POST['filt_type']:
        #print("ok")
            query_type = request.POST['filt_type']
            if entry_query:
                entry_query = entry_query & aux.get_query_new(query_type, ['type__type'])
            else:
                entry_query = aux.get_query_new(query_type, ['type__type'])
        # filter by author
        if ('filt_author' in request.POST) and request.POST['filt_author']:
            query_type = request.POST['filt_author']
            if entry_query:
                entry_query = entry_query & aux.get_query_new(query_type, ['author__username'])
            else:
                entry_query = aux.get_query_new(query_type, ['author__username'])
        # filter by project
        if ('filt_project' in request.POST) and request.POST['filt_project']:
            query_type = request.POST['filt_project']
            if entry_query:
                entry_query = entry_query & aux.get_query_new(query_type, ['project__name'])
            else:
                entry_query = aux.get_query_new(query_type, ['project__name'])
        found_entries = Report.objects.filter(entry_query, status="succeed").order_by('-created')

    print(entry_query)
    return render_to_response('reports-paginator.html', RequestContext(request, {
        'reports': found_entries
    }))

@login_required(login_url='/')
def home_paginate(request):
    if request.is_ajax() and request.method == 'GET':
        page = request.GET.get('page')
        table = request.GET.get('table')

        if table == 'screens':
            tag_symbol = 'screens'
            paginator = Paginator(rora.get_screens_info(),15)
            template = 'screens-paginator.html'
        elif table == 'datasets':
            tag_symbol = 'datasets'
            paginator = Paginator(rora.get_screens_info(),15)
            template = 'datasets-paginator.html'
        elif table == 'screen_groups':
            tag_symbol = 'screen_groups'
            paginator = Paginator(rora.get_screens_info(),15)
            template = 'screen-groups-paginator.html'

        try:
            items = paginator.page(page)
        except PageNotAnInteger:  # if page isn't an integer
            items = paginator.page(1)
        except EmptyPage:  # if page out of bounds
            items = paginator.page(paginator.num_pages)

        return render_to_response(template, RequestContext(request, { tag_symbol: items }))
    else:
        return False


    