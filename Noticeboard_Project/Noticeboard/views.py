from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.core.mail import EmailMultiAlternatives
from .filters import NoticeFilter
from .models import Notice, Reply, Category, Subscription
from django.contrib.auth.models import User
from .forms import NoticeForm, ReplyForm


def home(request):
    context = {
        'notices': Notice.objects.all()
    }
    return render(request, 'flatpages/home.html', context)


def about(request):
    context = {
        'notices': Notice.objects.all()
    }
    return render(request, 'flatpages/about.html', context)


@login_required
def my_notices(request):
    context = {
        'notices': Notice.objects.order_by('-date_posted').filter(author=request.user)
    }
    return render(request, 'flatpages/my_notices.html', context)


class NoticeListView(ListView):
    model = Notice
    template_name = 'flatpages/home.html'
    context_object_name = 'notices'
    ordering = ['-date_posted']
    paginate_by = 5


class UserNoticeListView(ListView):
    model = Notice
    template_name = 'Noticeboard/users_notices.html'
    context_object_name = 'notices'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Notice.objects.filter(author=user).order_by('-date_posted')


class NoticeDetailView(DetailView):
    model = Notice
    paginate_by = 5


class NoticeCreateView(LoginRequiredMixin, CreateView):
    model = Notice
    form_class = NoticeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NoticeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Notice
    form_class = NoticeForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        notice = self.get_object()
        if self.request.user == notice.author:
            return True
        return False


class NoticeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Notice
    success_url = '/'

    def test_func(self):
        notice = self.get_object()
        if self.request.user == notice.author:
            return True
        return False


class CategoryListView(NoticeListView):
    model = Notice
    template_name = 'categories.html'
    context_object_name = 'category_notices'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NoticeFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = datetime.utcnow()
        context['next_info'] = None
        context['filterset'] = self.filterset
        return context


class OneCategoryListView(NoticeListView):
    model = Notice
    template_name = 'category_list.html'
    context_object_name = 'category'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Notice.objects.filter(category=self.category).order_by('-date_posted')
        return queryset


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    success_url = '/notice/{notice_id}'

    def form_valid(self, form):
        form.instance.commentator = self.request.user
        form.instance.notice_id = self.kwargs['pk']
        return super().form_valid(form)


class ReplyDetailView(DetailView):
    model = Reply


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    form_class = ReplyForm
    success_url = '/notice/{notice_id}'

    def form_valid(self, form):
        form.instance.commentator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        notice = self.get_object()
        if self.request.user == notice.commentator:
            return True
        return False


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    success_url = '/notice/{notice_id}'

    def test_func(self):
        notice = self.get_object()
        if self.request.user == notice.commentator or self.request.user == notice.notice.author:
            return True
        return False


def accept(request, pk):
    user = request.user
    accepted_user = Reply.objects.get(id=pk)
    accepted_user.accept.add(user)
    message = "You have accepted the reply!"
    users = dict(User.objects.values_list('username', "email"))
    for key in users:
        if key == str(accepted_user):
            email = users[key]
            subject = 'Accepted!'
            text = f'Your reply has just been accepted! Check it out on our website - My Noticeboard!'
            html = (
                f'{accepted_user}, your reply has just been accepted! '
                f'Check it out on our website - <a href="http://127.0.0.1:8000/">My Noticeboard</a>!'
            )
            msg = EmailMultiAlternatives(subject=subject, body=text, from_email=None, to=[email])
            msg.attach_alternative(html, 'text/html')
            msg.send()
            break
    return render(request, 'accepted.html', {'accepted': accepted_user, 'message': message})


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe': Subscription.objects.filter(user=request.user, category=category,).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(Subscription.objects.filter(user=request.user,category=OuterRef('pk'),))).order_by('name')
    return render(request, 'subscriptions.html', {'categories': categories_with_subscriptions},)