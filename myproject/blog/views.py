from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from .models import Post
from django.core.exceptions import PermissionDenied
from .forms import CommentForm

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)


        if request.method =='POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post =post
                comment.author =request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied







class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload']

    template_name ='blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied 



class PostList(ListView):
    model =Post
    ordering = '-pk'

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context=super(PostDetail, self).get_context_data()
        context['comment_form']=CommentForm
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields =['title', 'hook_text', 'content', 'head_image', 'file_upload']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')




# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')


#     return render(request, 'blog/index.html',{'posts':posts, })
def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)
    return render(
        request, 
        'blog/single_post_page.html',
         {
             'post': post
         }
    )


