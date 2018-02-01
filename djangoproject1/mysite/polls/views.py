from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.core.mail import BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from polls.fusioncharts import FusionCharts  
from polls.forms import QuestionForm, ChoiceForm, ContactForm
from polls.forms import SignUpForm, FilterResults
from polls.models import Question, Choice, Contact




class charData(object):
    @classmethod
    def check_valve_data(cls):
        data = {'choice text': [], 'votes': []}
        values = Choice.objects.all().filter(votes_=10).order_by('choice_text')
        for unit in values:
            data['choice text'].append(unit.choice_text)
            data['votes'].append(unit.votes)
        return data

def get_queryset(query):
    if query:
        print("Searching :", query)
        query_list = query.split()
        results={}
        count=0
        for q in query_list:
            try:
                val1 = list(Question.objects.filter(question_text__contains=q))#.filter(question_text__icontains=q).filter(question_text__exact=q)
                if len(val1)>0:
                    results[count]= val1
                    count+= 1
            except ValueError:
                print('')
        finalresults = list(results.values())
        return finalresults


    
    
def IndexView(request):
    template_name = 'polls/index.html'
    
    #dataPlot = choices_filtering  # Choice.objects.all().filter(votes__gte=1).order_by('choice_text')

    print(request.GET)
    query = request.GET.get('q')
    result=[]
    # result.append(query)
    if query:
        result = get_queryset(query)
        if len(result) == 0:
            result.append('')
    else:
        result.append('')

    questions = Question.objects.all()
    form = FilterResults()
    answer = ''
    if request.method == 'POST':
        print(request.POST)
        status = request.POST.get('status')
        
        if status == "1":
            choices_filtering = Choice.objects.all().filter(votes__gte=1).order_by('choice_text')
        elif status == "2":
            choices_filtering = Choice.objects.all().filter(votes__gte=5).order_by('choice_text')
        elif status == "3":
            choices_filtering = Choice.objects.all().filter(votes__gte=10).order_by('choice_text')
        elif status == "4":
            choices_filtering = Choice.objects.all().filter(votes__gte=15).order_by('choice_text')
        elif status == "5":
            choices_filtering = Choice.objects.all().filter(votes__gte=20).order_by('choice_text')
        elif status == "6":
            choices_filtering = Choice.objects.all().filter(votes__lte=5).order_by('choice_text')
        elif status == "7":
            choices_filtering = Choice.objects.all().filter(votes__lte=10).order_by('choice_text')
        elif status == "8":
            choices_filtering = Choice.objects.all().filter(votes__lte=15).order_by('choice_text')
        elif status == "9":
            choices_filtering = Choice.objects.all().filter(votes__lte=20).order_by('choice_text')
                

        dataPlot = choices_filtering  # Choice.objects.all().filter(votes__gte=1).order_by('choice_text')
        columnChart = chart(dataPlot, plotType="column2d", subCaption=status)  # pie3d column2d
        return render(request, template_name,
                            {'title': 'FOOTBALL Index Page', 'head': 'FOOTBALL Index Head', 'questions': questions, 'form': form,
                             'output': columnChart.render()})
    else:
        form = FilterResults()
        return render(request, template_name,
                      {'title': 'FOOTBALL Index Page', 'head': 'FOOTBALL Index Head', 'questions': questions, 'form': form})

def detail(request,question_id):
    template_name = 'polls/detail.html'
    question = get_object_or_404(Question, id=question_id)
    choice = Choice.objects.all()
    sum_up = [c.votes for c in choice if c.question_id == int(question_id)]
    return render(request, template_name, {'question': question, 'question_total_votes': sum(sum_up)})
    
def results(request,question_id):
    template_name = 'polls/result.html'
    question = get_object_or_404(Question, id=question_id)
    return render(request,template_name, {'question': question})

def viewAllResults(request):
    question = Question.objects.all()
    choice = Choice.objects.all()
    score_total = {}
    for q in question:
        count = 0
        for c in choice:
            if c.question_id == q.id:
               count += c.votes
        score_total[q.id] = count
    print(score_total)
    total_votes = Choice.objects.all().aggregate(sumofvotes=Sum('votes'))
    page = request.GET.get('page', 1)
    paginator = Paginator(question, 5)
    try:
        question = paginator.page(page)
    except PageNotAnInteger:
        question = paginator.page(1)
    except EmptyPage:
        question = paginator.page(paginator.num_pages)
    return render(request, 'polls/viewall.html',
                  {'question': question, 'choice': choice, 'total_votes': total_votes, 'score_total': score_total})


def vote(request,question_id):
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
        print("choice",selected_choice.question_id)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question, 'error_message': "Please Select or Create Choice first, Please Contact Administrator",
        })
    else:   
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

def email (request):
    if request.method == 'GET':
        form = ContactForm()

    else:
        form = contactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            emailAddress = form.cleaned_data['emailAddress']
            message = form.cleaned_data['message']
            try:
                print(subject,emailAddress,message)
                obj = Contact(subject=subject, emailAddress=emailAddress, message=message) 
                obj.save() # send_mail(subject, message, contactemail, ['admin@example.com'])

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
    return render(request, "polls/contact.html", {'form': form})

def thanks(request):
    return HttpResponse('Thank you for your message.')

def add_poll(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            questions = Question.objects.all

            
        else:
            print(form.errors)
    else:
        form = QuestionForm()

def add_choice(request, question_id):
    question = Question.objects.get(id=question_id)
    print(question)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():  
           
            form.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            
        else:
            print(form.errors)
    else:
        form = ChoiceForm()
    return render(request, 'polls/add_choice.html', {'form': form, 'question': question})

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, "polls/profile.html", {'user': user})

def delete_question(request, question_id):
    if request.method == 'GET':
        Question.objects.get(id=question_id).delete()
        print("Question Deleted")
    return viewAllResults(request)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'polls/signup.html', {'form': form})

   # Create an object for the Area 2D chart using the FusionCharts class constructor
    # http://www.fusioncharts.com/dev/chart-attributes.html?chart=column2d&attributeName=chart_theme

def chart(dataPlot ,plotType,subCaption):
    """  Data source  """
    chartType = plotType  # "column2d"#pie3d
    chartID = "chart-1"  # chart ID unique for Page
    chartHeight = "800"  # chart Height
    chartWidth = "150%"  # chart Width
    chartDataFormat = "json"  # json xml
    dataSource = {}
    dataSource['chart'] = {}
    dataSource['chart']['caption'] = "World CUP FOOTBALL POLLS"
    dataSource['chart']['subCaption'] = "Votes (" + subCaption + ")"
    dataSource['chart']['xAsixName'] = "questions"
    dataSource['chart']['yAsixName'] = "votes"
    dataSource['chart']['numberPrefix'] = ""
    dataSource['chart']['startingangle'] = "120"  # pie3d
    dataSource['chart']['slicingdistance'] = "10"  # pie3d
    dataSource['chart']['rotatevalues'] = "1"
    dataSource['chart']['plotToolText'] = "<div><b>$label</b><br/>Votes : <b>$value</b></div>"
    dataSource['chart']['theme'] = "fint"  # ‘carbon’, ‘fint’, ‘ocean’, ‘zune’
    dataSource['chart']['animation'] = "1"  # ‘carbon’, ‘fint’, ‘ocean’, ‘zune’
    dataSource['chart']['animationDuration'] = "1"  # ‘carbon’, ‘fint’, ‘ocean’, ‘zune’
    dataSource['chart']['exportEnabled'] = "1"
    # dataSource['chart']['maxZoomLimit'] = 1000
    dataSource['data'] = []
    for item in dataPlot:
        q = get_object_or_404(Question, id=item.question_id)
        data = {}
        data['label'] = item.choice_text + "\n (" + q.question_text + ")"
        data['value'] = item.votes
        dataSource['data'].append(data)
    columnChart = FusionCharts(chartType, "ex2", chartHeight, chartWidth, chartID, chartDataFormat, dataSource)
    return columnChart



def plot(request, chartID='chart_ID', chart_type='line', chart_height=500):
    data = ChartData.check_valve_data()
    print(data)

    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, "width": chart_height}
    title = {"text": 'Votes Results'}
    xAxis = {"title": {"text": 'Votes'}}
    yAxis = {"title": {"text": 'Data'}}
    series = [
        {"name": 'Votes', "data": data['votes']},
        {"name": 'Choice Options', "data": data['choice text']}
    ]

    return render(request, 'polls/index.html', {'chartID': chartID, 'chart': chart,
                                               'series': series, 'title': title,
                                               'xAxis': xAxis, 'yAxis': yAxis})





def home(request):
    template_name = 'polls/index.html'
    form = FilterResults()
    questions = Question.objects.all
    if request.method == 'POST':
        status = request.POST['filter_option']
        form = FilterResults(request.POST)
        print("in home ", status)
       
        if status == "1":
                choices_filtering = Choice.objects.all().filter(votes__gte=1).order_by('choice_text')
        elif status == "2":
            choices_filtering = Choice.objects.all().filter(votes__gte=5).order_by('choice_text')
        elif status == "3":
            choices_filtering = Choice.objects.all().filter(votes__gte=10).order_by('choice_text')
        elif status == "4":
            choices_filtering = Choice.objects.all().filter(votes__gte=15).order_by('choice_text')
        elif status == "5":
            choices_filtering = Choice.objects.all().filter(votes__gte=20).order_by('choice_text')
        elif status == "6":
            choices_filtering = Choice.objects.all().filter(votes__lte=5).order_by('choice_text')
        elif status == "7":
            choices_filtering = Choice.objects.all().filter(votes__lte=10).order_by('choice_text')
        elif status == "8":
            choices_filtering = Choice.objects.all().filter(votes__lte=15).order_by('choice_text')
        elif status == "9":
            choices_filtering = Choice.objects.all().filter(votes__lte=20).order_by('choice_text')
                

        dataPlot = choices_filtering  # Choice.objects.all().filter(votes__gte=10).order_by('choice_text')
        columnChart = chart(dataPlot, plotType="column2d", subCaption=status)  # pie3d column2d

        return render(request, template_name,
                      {'title': 'FOOTBALL Index Page', 'head': 'FOOTBALL Index Head', 'questions': questions,
                       'form': form, 'output': columnChart.render()})




