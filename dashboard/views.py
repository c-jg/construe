from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import ListView, CreateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Report

from membership.views import get_user_membership

# Create your views here.

@login_required
def account_settings_view(request):
    context = {"account_act": "vMenu--active", "dash_style":"opacity:1;border-bottom: 1px solid #fff;"}
    return render(request, "acc_settings.html", context)

def terms_view(request):
    context = {"terms_act": "vMenu--active", "dash_style":"opacity:1;border-bottom: 1px solid #fff;"}
    return render(request, "terms.html", context)

@login_required
def privacy_policy_view(request):
    context = {"privacy_act": "vMenu--active", "dash_style":"opacity:1;border-bottom: 1px solid #fff;"}
    return render(request, "privacy_policy.html", context)

def success_view(request):
    return render(request, 'success.html', {})
    
def cancel_view(request):
    return render(request, 'cancel.html', {})

class ReportCreateView(LoginRequiredMixin, CreateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)      
        return context

    model = Report
    fields = ['url', 'report_name']
    #success_url = '/saved/'    
    def get_success_url(self):
        return reverse('report_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        rep = form.save(commit=False)
        
        input_url = self.request.POST['url'].split("/watch?v=")[1]
        new_url = input_url[:11]
        rep.url = new_url
        # -------------
        import googleapiclient.discovery
        import os, csv, json, nltk, collections, pickle
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        from ibm_watson import NaturalLanguageUnderstandingV1
        from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, EmotionOptions
        from ibm_watson.natural_language_understanding_v1 import EntitiesOptions, KeywordsOptions

        nltk.download('vader_lexicon')

        ibmApiKey = os.environ['IBM_API_KEY']
        url = 'https://gateway.watsonplatform.net/natural-language-understanding/api'

        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey=ibmApiKey,
            url=url
        )

        #os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

        comments = []
        data = []
        keys = []
        only_com = []
        video_details = []

        api_service_name = 'youtube'
        api_version = "v3"
        ytApiKey = os.environ['YT_API_KEY']

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey = ytApiKey)

        vid_id = new_url
        # get details
        req_details = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=vid_id
        )

        details = req_details.execute()
        det = details["items"][0]
        videoTitle = det["snippet"]["title"]        
        viewCount = det["statistics"]["viewCount"]
        commentCount = det["statistics"]["commentCount"]
        #description = det["snippet"]["description"]
        #vidLikes = det["statistics"]["likeCount"]
        #vidDislikes = det["statistics"]["dislikeCount"]
        
        video_details.append(videoTitle)    
        video_details.append(viewCount)
        video_details.append(commentCount)

        # get all comments        
        def get_comment_threads(token=""):     
            results = youtube.commentThreads().list(
                part="snippet,replies",
                textFormat="plainText",
                pageToken=token,
                maxResults=100,
                videoId=vid_id
            ).execute()

            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]
                text = comment["snippet"]["textDisplay"]
                comReplies = item["snippet"]["totalReplyCount"]
                comLikes = comment["snippet"]["likeCount"]
                top = comReplies + comLikes
                comments.append([text, comLikes, comReplies, top])
                only_com.append(text)

                if 'replies' in item.keys():
                    for rep in item["replies"]["comments"]:
                        reply = rep["snippet"]["textDisplay"]
                        rep_likes = rep["snippet"]["likeCount"]
                        comments.append([reply, rep_likes, "N/A", "N/A"])
                        only_com.append(reply)

            if "nextPageToken" in results:
                return get_comment_threads(results["nextPageToken"])
            else:
                return comments
        get_comment_threads()
        all_ = ". ".join(only_com)

        # IBM
        response = natural_language_understanding.analyze(
            text=str(all_),
            language='en',
            features=Features(concepts=ConceptsOptions(limit=5),
                            entities=EntitiesOptions(sentiment=True, limit=5),
                            keywords=KeywordsOptions(limit=200)
            )).get_result()

        # Sort Keywords

        for key in response["keywords"]:
            text = key["text"]
            count = key["count"]
            rel = key["relevance"]
            keys.append([text, count, rel])

        def sortSecond(val): 
            return val[1]
        keys.sort(key = sortSecond)

        # Score sentiment
        sent_array = []

        prod_sent = []

        vn = []
        n = []
        sn = []
        neu = [] #0
        sp = []
        p = []
        vp = []

        sia = SentimentIntensityAnalyzer()
        for i in range(len(comments)):
            comment = comments[i][0]
            sent = sia.polarity_scores(comment)
            score = sent["compound"]
            #data.append([comment, score])
            sent_array.append(score)

        for i in sent_array:
            if i <= -.75:
                vn.append(i)
            elif -.75 < i <= -.5:
                n.append(i)
            elif -.5 < i <= -.25:
                sn.append(i)
            elif -.25 < i <= .25:
                neu.append(i)
            elif .25 < i <= .5:
                sp.append(i)
            elif .5 < i <= .75:
                p.append(i)
            else:
                vp.append(i)

        prod_sent.append(len(vn))
        prod_sent.append(len(n))
        prod_sent.append(len(sn))
        prod_sent.append(len(neu))
        prod_sent.append(len(sp))
        prod_sent.append(len(p))
        prod_sent.append(len(vp))

        # Spam
        from django.contrib.staticfiles import finders
        locRes = finders.find('pickles/sp_model')
        with open(locRes, 'rb') as p:
            sm = pickle.load(p)
        

        spam = 0
        ham = 0
        for i in range(len(comments)):
            comment = comments[i][0]
            sm.predict([comment])
            if sm.predict([comment]) == [1]:
                spam += 1
            else:
                ham += 1

        if (spam) == 0:
            perc = 0
        else:
            perc = round((spam/(spam + ham)), 4)

                
        # IBM concepts
        conc = []
        _concepts = []
        concept_rel = []
        for concept in response["concepts"]:
            text = concept["text"]
            relevance = concept["relevance"]            
            conc.append([text, relevance])

        # Sort concepts
        conc.sort(key = sortSecond)
        for i in range(len(conc)):
            _concepts.append(conc[i][0])
            concept_rel.append(conc[i][1])

        # IBM Keyphrases
        words = []
        total_k = 0
        
        _keyW = []
        _keyCount = []

        for elem in keys:
            if elem not in words:
                words.append(elem)
                if len(words) >= 10:
                    break
        for i in range(len(words)):
            _keyW.append(words[i][0])
            _keyCount.append(words[i][1])
            total_k += words[i][1]
            
        for i in range(len(words)):
            cnt = words[i][1]
            percent = round((cnt/total_k), 4)

        # Entities (Count, Sentiment) - IBM
        total_e = 0
        ents = []
        # ---- PRODUCTION
        _entities = []
        _eCount = []
        _eSent = []
        _ePerc = []

        all_ent = []
        # ---- PRODUCTION

        for ent in response["entities"]:
            text = ent["text"]
            sent = ent["sentiment"]["label"]
            sent_score = ent["sentiment"]["score"]
            rel = ent["relevance"]
            eCount = ent["count"]
            total_e += eCount
            ents.append([text, sent, rel, eCount, sent_score])
            _eSent.append(sent_score)
            all_ent.append([text, eCount])

        # Sort Entities
        all_ent.sort(key = sortSecond)
        for i in range(len(all_ent)):
            _entities.append(all_ent[i][0])
            _eCount.append(all_ent[i][1])

        
        # -------------
        
        
        rep.keywords = _keyW
        rep.keyword_count = _keyCount

        rep.spam = perc
        rep.entities = _entities
        rep.entity_count = _eCount
        rep.title = video_details[0]
        rep.views = video_details[1]
        rep.comments = video_details[2]
        rep.concepts = _concepts
        rep.concept_relevance = concept_rel
        rep.sentiment = prod_sent

        form.instance.author = self.request.user
        return super().form_valid(form)

# Dashboard list of saved reports
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'saved.html'
    context_object_name = "reports"
    ordering = ['-created']
    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user)


# load data from database and display on charts here
from django.http import Http404  
class ReportDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Report

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['keyword_data'] = zip(self.get_object().keywords, self.get_object().keyword_count)
        context['entity_data'] = zip(self.get_object().entities, self.get_object().entity_count)
        context['not_spam'] = 1 - self.get_object().spam
        context['concept_data'] = zip(self.get_object().concepts, self.get_object().concept_relevance)
        return context

    def test_func(self):
        report = self.get_object()
        if self.request.user == report.author:
            return True
        raise Http404