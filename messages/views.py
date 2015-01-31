from django.shortcuts import render
from forms import WriteMessageForm, WriteReviewToMessageForm
from models import Message
import datetime
import json
from django.http import HttpResponse
from urlparse import urlparse, parse_qs


def get_tree(level, message, suspected_msgs):
    messages = suspected_msgs.filter(parent=message).order_by('-date_and_time')
    response = []
    for msg in messages:
        response += [msg.in__dict({"level":level*3})]
        response += get_tree(level+1, msg, suspected_msgs.filter(node_history__startswith=msg.node_history))
    return response


def get_wall_of_messages(level, msgs, childs, trees):
    response = []
    msg_ids = set(msgs.values_list('id', flat=True))
    if not(msg_ids&childs or msg_ids&trees):
        return [x.in__dict({"level":level*3}) for x in msgs]
    for msg in msgs:
        response += [msg.in__dict({"level":level*3})]
        if msg.id in trees:
            response += get_tree(level+1, msg, Message.objects.filter(node_history__startswith=msg.node_history))
        else:
            response += get_wall_of_messages(level+1, Message.objects.filter(parent__id=msg.id).order_by('-date_and_time'),childs, trees)
    return response


def home(request):
    context = {}
    child_ids = tree_ids = heirs_of_tree = set()
    if request.method == 'GET':
        if request.GET.has_key("childs"):
            child_ids = child_ids.union(get_int_if_error_zero(i) for i in request.GET.getlist('childs'))
        if request.GET.has_key("trees"):
            tree_ids = tree_ids.union([get_int_if_error_zero(i) for i in request.GET.getlist('trees')])
            msgs = Message.objects.filter(id__in=tree_ids)
            for msg in msgs:
                heirs_of_tree |= set(Message.objects.filter(node_history__startswith=msg.node_history).values_list('id', flat=True))
    context['messages'] = get_wall_of_messages(0, Message.objects.filter(parent=None).order_by('-date_and_time'),
                                               child_ids, tree_ids)
    form = WriteReviewToMessageForm()
    context['form'] = form
    context['trees'] = list(heirs_of_tree)
    context['childs'] = list(child_ids)
    if request.is_ajax():
        return HttpResponse(json.dumps(context), mimetype = 'application/json' )
    return render(request, "home.html", context)

def show_childs_or_tree(request):
    context={}
    if request.method == 'GET':
        if request.GET.has_key("childs") and request.GET['childs']:
            key = "childs"
        elif request.GET.has_key("trees") and request.GET['trees']:
            key = "trees"
        id = get_int_if_error_zero(request.GET[key])
        msg = Message.objects.get(id=id)
        if(key=="trees"):
            context[key] = list(Message.objects.filter(node_history__startswith=msg.node_history).values_list('id', flat=True))
            context['messages'] = get_tree(msg.node_history.count('-'), msg, Message.objects.filter(node_history__startswith=msg.node_history))
        elif(key=="childs"):
            context['messages'] = get_wall_of_messages(msg.node_history.count('-'), Message.objects.filter(parent=msg).order_by('-date_and_time'), set(), set())
            context[key] = id
        new_url = urlparse(request.META.get('HTTP_REFERER'))
        query = parse_qs(new_url.query)
        context['location'] = new_url.path+'?'+'%s=%s&%s'%(key, id,''.join('%s=%s&'%(k,get_int_if_error_zero(query[k][0])) for k in query))
        context['id'] = id
        return HttpResponse(json.dumps(context), mimetype = 'application/json')


def write_message(request):
    context = {}
    if request.method == 'POST' and request.is_ajax:
        form = WriteMessageForm(request.POST.copy())
        if form.is_valid():
            message = Message()
            message.text = form.cleaned_data['text']
            message.date_and_time = datetime.datetime.now()
            message.save()
            context['message_type'] = 'success'
        else:
            context['message_type'] = 'errors'
            context['errors'] = dict(form.errors)
        return HttpResponse(json.dumps(context), mimetype = 'application/json' )
    form = WriteMessageForm()
    context['form'] = form
    context['HTTP_REFERER'] = '/'if not(request.META.get('HTTP_REFERER')) else request.META.get('HTTP_REFERER')
    return render(request, "write_message.html", context)


def write_review(request):
    context = {}
    if request.method == 'POST' and request.is_ajax:
        form = WriteReviewToMessageForm(request.POST.copy())
        if form.is_valid():
            message = Message()
            message.text = form.cleaned_data['text']
            message.parent_id = int(form.cleaned_data['message_parent_id'])
            message.save()
            context['message_type'] = 'success'
            context['parent_id'] =  message.parent_id
        else:
            context['message_type'] = 'errors'
            context['errors'] = dict(form.errors)
        return HttpResponse(json.dumps(context), mimetype = 'application/json')

def get_int_if_error_zero(strInInt):
    try:
        return int(strInInt)
    except():
        return 0
