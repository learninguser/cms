from django.shortcuts import render, redirect
from django.views import View, generic
from blog import models
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from blog.forms import PostForm
from django.utils.text import slugify
from django.db.models import Q


class HomeView(generic.ListView):
    model = models.Post
    queryset = models.Post.objects.filter(status="P")
    context_object_name = 'posts'
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = models.Category.objects.all()
        context['categories'] = categories
        return context


class AboutUsView(generic.TemplateView):
    template_name = '404.html'


class CategoryView(View):
    def get(self, request, id):
        if models.Category.objects.filter(id=id)[0].name == 'All':
            posts = models.Post.objects.all()
            categories = models.Category.objects.all()
        else:
            posts = models.Post.objects.filter(category__id=id)
            categories = models.Category.objects.filter(id=id)
        return render(request, 'blog/index.html', context={'posts': posts, 'categories': categories})


def search(request):
    template = 'blog/index.html'
    query = request.GET.get('search')
    results = models.Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, template, context={'posts': results})

# class SearchQuery(generic.ListView):
#     model = models.Post
#     context_object_name = 'posts'
#     template_name = 'blog/index.html'
#     form_class = SearchQueryForm

#     def get_queryset(self):
#         form = self.form_class(self.request.GET)
#         print(form)
#         if form.is_valid():
#             return models.Post.objects.filter(
#         Q(title__icontains=query) | Q(content__icontains=query))
#         return models.Post.objects.all()


class PostView(generic.DetailView):
    '''
        To view a particular post
    '''
    permission_required = 'blog.view_post'
    model = models.Post
    queryset = models.Post.objects.filter(status="P")
    login_url = reverse_lazy('login')
    template_name = 'blog/blogpost.html'
    # pk_url_kwarg = 'id' # overwriting this field so that we can use id directly instead of pk

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if not request.session.get('count'):
                request.session['count'] = 1
            else:
                request.session['count'] += 1

            if request.session.get('count') > 3:
                return redirect(reverse_lazy('login'))

        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    '''
        To create a new blog post
    '''
    permission_required = 'blog.add_post'
    login_url = reverse_lazy('login')
    model = models.Post
    form_class = PostForm
    template_name = 'blog/createpost.html'

    def get_success_url(self):
        if self.object.slug:
            slug = self.object.slug
        return reverse('blog', kwargs={'slug': slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    permission_required = 'blog.change_post'
    login_url = reverse_lazy('login')
    model = models.Post
    form_class = PostForm
    template_name = 'blog/createpost.html'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        if self.object.slug:
            slug = self.object.slug
        return reverse('blog', kwargs={'slug': slug})

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get(self, request, slug):
    #     post = models.Post.objects.get(slug=slug)
    #     form = PostForm(instance=post)
    #     return render(request, "blog/createpost.html", context={"form": form, "post": post})

    def test_func(self, *args, **kwargs):
        '''
            To restrict an user to edit a post which he authored
        '''
        post = models.Post.objects.get(slug=self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False


# class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.DeleteView):
#     permission_required = 'blog.change_post'
#     login_url = reverse_lazy('login')
#     model = models.Post
#     success_url = reverse_lazy('home')

#     def get_queryset(self):
#         post = models.Post.objects.get(slug=self.kwargs.get('slug'))
#         owner = self.request.user
#         return self.model.objects.filter(author=owner)
    
#     def get_success_message(self, cleaned_data):
#         title = cleaned_data.get('title')
#         return (f"Post with {title} is deleted successfully")

#     def test_func(self, *args, **kwargs):
#         '''
#             To restrict an user to edit a post which he authored
#         '''
#         post = models.Post.objects.get(slug=self.kwargs.get('slug'))
#         if post.author == self.request.user:
#             return True
#         else:
#             return False