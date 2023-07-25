import logging

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.template.response import TemplateResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Category, Words
from .forms import InquiryForm, QuizForm

logger = logging.getLogger(__name__)

class IndexView(generic.TemplateView):
    template_name = 'quiz/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'quiz/index.html'


class WordsListView(generic.ListView):
    template_name = 'quiz/words_list.html'
    context_object_name = 'category_obj'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category =  self.kwargs.get('category')
        context['category'] = category

        return context

    def get_queryset(self):
        category = self.kwargs.get('category')

        if category == '全ての英単語一覧':
            queryset = Words.objects.all()
        else:
            queryset = Category.objects.get(category=category).words_set.all()

        return queryset

class InquiryView(generic.FormView):
    template_name = 'quiz/inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('quiz:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class FlashCardView(LoginRequiredMixin, generic.ListView):
    template_name = 'quiz/flashcard.html'
    context_object_name = 'flashcard_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')

        return context

    def get_queryset(self):
        category = self.kwargs.get('category')
        queryset = Category.objects.get(category=category).words_set.all()

        return queryset

@login_required
def words_mean(request, category, pk):
    category = get_object_or_404(Category, category=category)
    words = get_object_or_404(Words, pk=pk, category=category)

    context = {
        'category': category,
        'words': words,
    }

    return render(request, 'quiz/words_mean.html', context)

def result_message(answer, japanese):
    if str(answer) == str(japanese):
        message = '正解'
    else:
        message = '不正解'

    return message

@login_required
def start_quiz(request, category):
    form = QuizForm(request.POST or None)
    category = Category.objects.get(category=category)
    words = Words.objects.filter(category=category.pk).first()

    if request.method == 'POST' and form.is_valid():
        answer = request.POST['answer']
        japanese = words.japanese
        
        message = result_message(answer, japanese)

        context = {
            'message': message,
            'words': words,
            'form': form
        }
               
        return redirect('quiz:result', category=category.category, message=message, pk=words.pk)
    else:
        context = {
            'category' : category,
            'words': words,
            'form': form
        }

        return render(request, 'quiz/quiz.html', context)

class QuizView(LoginRequiredMixin, generic.FormView):
    template_name = 'quiz/quiz.html'
    form_class = QuizForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, category=self.kwargs.get('category'))
        context['words'] = Words.objects.filter(category=category.pk).get(pk=self.kwargs.get('pk'))

        return context

    def form_valid(self, form):
        answer = form.cleaned_data['answer']
        words = Words.objects.get(pk=self.kwargs.get('pk'))
        japanese = words.japanese
        category = get_object_or_404(Category, category=self.kwargs.get('category'))

        message = result_message(answer, japanese)

        return redirect('quiz:result', category=category, message=message, pk=words.pk)

class ResultView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'quiz/result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = self.kwargs.get('message')
        context['words'] = Words.objects.get(pk=self.kwargs.get('pk'))

        return context

        
        


# class QuizView(generic.FormView):
#     template_name = 'quiz/quiz.html'
#     form_class = QuizForm
#     # context_object_name = 'quiz_obj'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = get_object_or_404(Category, category=self.kwargs.get('category'))
#         context['category'] = category
#         context['first'] = Words.objects.filter(category=category.pk).first()
#         return context

    
