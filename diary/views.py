import logging

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import InquiryForm, DiaryCreateForm, DiarySearchForm
from .models import Diary

logger = logging.getLogger(__name__)

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = "index.html"

class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('diary:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)

class DiaryListView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name="diary_list.html"
    paginate_by = 2

    def get_queryset(self):
        diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
        return diaries

class DiaryDetailView(generic.DetailView):
    # pk（モデルの主キー）ではなく、他のフィールドを使いたい場合（urlに数字ではなく記事のタイトルを入れたい場合など）
    # model = Post
    # slug_field = "title" # モデルのフィールドの名前
    # slug_url_kwarg = "title" # urls.pyでのキーワードの名前

    model = Diary
    template_name = 'diary_detail.html'
    # pk_url_kwarg = 'id' # pkをidに変更した場合に記述

class DiaryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Diary
    template_name = 'diary_create.html'
    form_class = DiaryCreateForm
    success_url = reverse_lazy('diary:diary_list')

    def form_valid(self, form):
        diary = form.save(commit=False)
        diary.user = self.request.user
        diary.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, '日記の作成に失敗しました。')
        return super().form_invalid(form)

class DiaryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Diary
    template_name = 'diary_update.html'
    form_class = DiaryCreateForm

    def get_success_url(self):
        return reverse_lazy('diary:diary_detail', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        messages.success(self.request, "日記を更新しました。")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)

class DiaryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Diary
    template_name = 'diary:diary_list'
    success_url = reverse_lazy('diary:diary_list')

    def delete(self, request, *args, **kwargs):
        message.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)

class DiarySearchView(LoginRequiredMixin, generic.ListView):
    model = Diary
    template_name="diary_search.html"
    paginate_by = 10
    form_class = DiarySearchForm
    # success_url = reverse_lazy('diary:diary_search')

    # def get_queryset(self):
    #     diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
    #     return diaries


    # def get_queryset(self):
    #     # フォームから入力されたクエリを取得
    #     query = self.request.GET.get('q')
    #     if query:
    #         # ユーザーが入力したクエリを含む日記をフィルタリングする
    #         diaries = Diary.objects.filter(user=self.request.user, content__icontains=query).order_by('-created_at')
    #     else:
    #         # クエリが指定されていない場合はすべての日記を表示する
    #         diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
    #     return diaries

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = self.form_class(self.request.GET)
    #     return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            diaries = Diary.objects.filter(user=self.request.user, content__icontains=query).order_by('-created_at')
            if diaries.exists():
                count = diaries.count()  # クエリセットの件数を取得
                messages.success(self.request, f"検索結果: {count}件見つかりました。")
            else:
                messages.warning(self.request, "検索結果が見つかりませんでした。")
        else:
            # diaries = Diary.objects.filter(user=self.request.user).order_by('-created_at')
            return Diary.objects.none()  # 検索クエリがない場合は空のクエリセットを返す
        return diaries

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['form'] = self.form_class(self.request.GET)
        context['form'] = self.form_class()
        return context

    # def get(self, request, *args, **kwargs):
    #     # メッセージを設定する例
    #     messages.success(self.request, "メッセージの内容")
    #     return super().get(request, *args, **kwargs)
