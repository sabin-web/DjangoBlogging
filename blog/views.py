from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Post,Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm,PostModelForm
from django.urls import reverse,reverse_lazy
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import View	
from django.utils.decorators import method_decorator
from .forms import CommentForm
# Create your views here.


from django.shortcuts import render, get_object_or_404

def home(request):
	context = {
		'posts' : Post.objects.all(),
		'title' : 'Home'
	}
	return render(request, 'blog/home.html', context)

def about(request):
	return render(request, 'blog/about.html' , {'title' : 'About'})

	
def first(request):
	return render(request,'blog/first.html',{'title':'First'})



class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html' #<app>/<model>_<viewtype>.html
	context_object_name = 'posts'
	ordering = ['-date_posted']

	paginate_by = 6
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):        
		return super(PostListView, self).dispatch(request, *args, **kwargs)


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']


	paginate_by = 6

	
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')



# class PostDetailView(DetailView):
# 	model = Post
# 	def get_context_data(self,*args,**kwargs):
# 		context = super(PostDetailView,self).get_context_data(*args,**kwargs)
# 		stuff = get_object_or_404(Post,id = self.kwargs['pk'])
# 		total_likes = stuff.total_likes()
# 		context['total_likes'] = total_likes
# 		return context



# class DetailPostView(View):
# 	template_name = 'blog/post_detail.html'
# 	form_class = CommentForm

# 	def get(self, request,pk=None,*args, **kwargs):  
# 		context = {}
# 		if pk is not None:
# 			obj = get_object_or_404(Post,pk = self.kwargs['pk'])
# 			queryset = obj.comments.all()
# 			context['object'] = obj
# 			total_likes = obj.total_likes()
# 			context['total_likes'] = total_likes
# 			context['object_list'] = queryset
			
# 		return render(request,self.template_name,context)
# 	def post(self, request,pk=None, *args, **kwargs):
		
		
# 		obj = Comment(
# 			post = Post.objects.get(id=pk),
# 			body = request.POST['body'],
# 			email= request.user.email,
# 			name = request.user,
# 			active = request.user.is_active

# 			)

# 		obj.save()
			
	
			
# 		return redirect('post-detail',pk=pk)
		
class DetailPostView(View):
	template_name = 'blog/post_detail.html'
	form_class = CommentForm

	def get(self, request,pk=None,*args, **kwargs):  
		context = {}
		if pk is not None:
			obj = get_object_or_404(Post,pk = self.kwargs['pk'])
			queryset = obj.comments.all()
			context['object'] = obj
			total_likes = obj.total_likes()
			context['total_likes'] = total_likes
			context['object_list'] = queryset
			
		return render(request,self.template_name,context)
	def post(self, request,pk=None, *args, **kwargs):
		
		
		obj = Comment(
			post = Post.objects.get(id=pk),
			body = request.POST['body'],
			email= request.user.email,
			name = request.user,
			active = request.user.is_active

			)

		obj.save()
		context = {}
		context['post'] = post
		context['body'] = body
		context['email'] = email
		context['name'] = name	
		context['active'] = active
			
		

		if request.is_ajax():
			html = render_to_string('blog/comments.html',context,request=request)
			return JsonResponse({'form':html})
		return redirect('post-detail',pk=pk)


	# def get(self, request, *args, **kwargs):  
	# 	context = {}
	# 	obj = self.get_object()
	# 	if obj is not None:
	# 		form = PostModelForm(instance = obj)
	# 		context['object'] = obj
	# 		context['form'] = form
	# 	return render(request, self.template_name,context)






def LikeView(request,pk):
	post = get_object_or_404(Post,pk=pk)
	post.likes.add(request.user)
	return HttpResponseRedirect(reverse('post-detail',args=[pk]))


# class PostCreateView(LoginRequiredMixin, CreateView):
# 	model = Post	
# 	fields = ['title', 'content']

# 	def form_valid(self, form):
# 		form.instance.author = self.request.user
# 		return super().form_valid(form)

class CreatePostView(View):
    form_class = PostModelForm
    template_name = 'blog/post_form.html'

    def get(self, request, *args, **kwargs):  
        return render(request, self.template_name,{'form':self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # <process form cleaned data>
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return redirect('/')

        return render(request, self.template_name, {'form': form})

# def create_post_info(request):
# 	if request.method == 'POST':
# 		form = PostModelForm(request.POST)
# 		if form.is_valid():
# 			form.save()
# 			print('form is valid')
# 			return redirect('post-detail')
# 		else:
# 			print('from is invalid')

# 	else:
# 		form = PostModelForm()


# 	return render(request,'blog/post_form.html',{
# 		'form':form
# 		})



class UpdatePostView(View):
	form_class = PostModelForm
	template_name = 'blog/post_form.html'

	def get_object(self):
		context = {}
		id = self.kwargs.get('pk')
		obj = None
		if id is not None:
			obj = get_object_or_404(Post,id=id)
			context['object'] = obj
		return obj

	def get(self, request, *args, **kwargs):  
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = PostModelForm(instance = obj)
			context['object'] = obj
			context['form'] = form
		return render(request, self.template_name,context)

	def post(self, request, *args, **kwargs):
		
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = PostModelForm(request.POST,instance=obj)
			context['object'] = obj
			context['form'] = form
			if form.is_valid():
            # <process form cleaned data>
            
				form = form.save(commit=False)
				form.author = request.user
				form.save()
			return redirect('post-detail',pk=self.kwargs.get('pk'))

		return render(request, self.template_name, context)






def delete_post_info(request,pk):
	user_object = get_object_or_404(Post,id= pk)
	user_object.delete()
	return redirect(f'/')
