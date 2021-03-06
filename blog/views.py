from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostModelForm, PostForm, CommentModelForm

from blog.models import Post, Comment


# Views 내에 선언된 함수 -> HttpRequest 객체를 인자로 Django가 전달해준다
def post_list(request):
    # my_name = 'Django Web Framework'
    # http_method = request.method
    # return HttpResponse('''
    #     <h2>Welcome {name}</h2>
    #     <p>Http Method : {method}</p>
    #     <p>Http headers : {header}</p>
    #     <p>Http Path : {my_path}</p>
    # '''.format(name=my_name, method=http_method, header=request.headers['user-agent'], my_path=request.path))

    # return render(request, 'blog/post_list.html')
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'post_list': posts})


# 글 상세 정보
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# 글 등록 (form 사용)
@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data)
            clean_data_dict = form.cleaned_data
            post = Post.objects.create(
                author=request.user,
                title=clean_data_dict['title'],
                text=clean_data_dict['text'],
                published_date=timezone.now()
            )
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'postform': form})


# 글 수정 (ModelForm 사용)
@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'postform': form})


# 글 삭제
@login_required
def post_remove(request, pk):
    post = Post.objects.get(pk=pk)
    post.delete()
    return redirect('post_list_home')


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # 댓글이 속한 post 객체를 comment.post에 명시적으로 넘겨줘야함
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentModelForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)


# 글 등록 (ModelForm 사용)
# def post_new_modelform(request):
#     if request.method == 'POST':
#         # 데이터 등록 요청
#         post_form = PostModelForm(request.POST)
#         if post_form.is_valid():
#             # form 객체의 save() 호출함으로써 Model 객체 생성
#             post = post_form.save(commit=False)
#             # 로그인 되어있는 username을 author 필드에 저장
#             post.author = request.user
#             # 현재날짜시간을 게시일자로 저장
#             post.published_date = timezone.now()
#             # post 객체 저장 -> insert 처리
#             post.save()
#             # 등록 후 상세 페이지로 리다이렉션 처리
#             return redirect('post_detail', pk=post.pk)
#     else:
#         # 등록을 위한 Form 출력
#         post_form = PostModelForm()
#     return render(request, 'blog/post_edit.html', {'postform': post_form})



