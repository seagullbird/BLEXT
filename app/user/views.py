# -*- coding: utf-8 -*-
from . import user
from flask import render_template, current_app, request, redirect, url_for, abort,make_response, flash
from flask_login import current_user, login_required
from ..models import Blog, User, Category, Tag
from .. import db
from .forms import CommentForm,SearchForm
from ..models import Comment


# 用户主页路由
@user.route('/<username>')
def index(username):
    # 查找博客主人
    host_user = User.query.filter_by(username=username).first()
    if host_user:
        # 添加分页
        page = request.args.get('page', 1, type=int)
        # 每页显示的博客数保存在配置里
        show_followed = bool(request.cookies.get('show_followed', ""))
        if show_followed:
            query = current_user.followed_blogs
            # 获得用户所有文章（按时间戳顺序）
        else:
            query = Blog.query
        pagination = query.order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
        blogs = pagination.items
        return render_template('user/index.html', blogs=blogs, pagination=pagination, host_user=host_user)
    abort(404)


# 文章分类总路由
@user.route('/<username>/categories')
def categories(username):
    host_user = User.query.filter_by(username=username).first()
    if host_user:
        return render_template('user/categories.html', categories=host_user.categories.all(), host_user=host_user)
    abort(404)


# 单个分类下的文章列表路由
@user.route('<username>/categories/<category_name>')
def category(username, category_name):
    host_user = User.query.filter_by(username=username).first()
    category = Category.query.filter_by(
        name=category_name, author_id=host_user.id).first()
    if not host_user or not category:
        abort(404)
    # 添加分页
    page = request.args.get('page', 1, type=int)
    # 如果不是本人则不能看到草稿
    if not current_user.is_authenticated or current_user.id != host_user.id:
        # 每页显示的博客数保存在配置里
        pagination = category.blogs.filter_by(draft=False).order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    else:
        # 每页显示的博客数保存在配置里
        pagination = category.blogs.order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    # 获得用户所有文章（按时间戳顺序）
    blogs = pagination.items
    return render_template('user/index.html', blogs=blogs, pagination=pagination, host_user=host_user)


# 文章标签总路由
@user.route('/<username>/tags')
def tags(username):
    host_user = User.query.filter_by(username=username).first()
    if host_user:
        return render_template('user/tags.html', tags=host_user.tags.all(), host_user=host_user)
    abort(404)


# 单个标签下的文章列表路由
@user.route('<username>/tags/<tag_name>')
def tag(username, tag_name):
    host_user = User.query.filter_by(username=username).first()
    tag = Tag.query.filter_by(name=tag_name, author_id=host_user.id).first()
    if not host_user or not tag:
        abort(404)
    # 添加分页
    page = request.args.get('page', 1, type=int)
    # 如果不是本人则不能看到草稿
    if not current_user.is_authenticated or current_user.id != host_user.id:
        # 每页显示的博客数保存在配置里
        pagination = tag.blogs.filter_by(draft=False).order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    else:
        # 每页显示的博客数保存在配置里
        pagination = tag.blogs.order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    # 获得用户所有文章（按时间戳顺序）
    blogs = pagination.items
    return render_template('user/index.html', blogs=blogs, pagination=pagination, host_user=host_user)


# 用户草稿路由
@login_required
@user.route('/<username>/drafts')
def drafts(username):
    host_user = User.query.filter_by(username=username).first()
    # 判断是否本人
    if host_user and current_user._get_current_object() == host_user:
        # 添加分页
        page = request.args.get('page', 1, type=int)
        # 每页显示的博客数保存在配置里
        pagination = Blog.query.filter_by(author_id=host_user.id, draft=True).order_by(Blog.timestamp.desc()).paginate(
            page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
        # 获得用户所有文章（按时间戳顺序）
        blogs = pagination.items
        # 返回入口
        draft_enter = 'Home'
        return render_template('user/index.html', blogs=blogs, pagination=pagination, host_user=host_user, draft_enter=draft_enter)
    abort(404)


# 用户文章路由
@user.route('/<username>/<int:blog_id>',methods=['GET','POST'])
def blog_page(username, blog_id):
    # 利用blog_id从数据库读到blog对象并返回给模版
    host_user = User.query.filter_by(username=username).first()
    blog = Blog.query.filter_by(id=blog_id).first()
    # 如果访问的用户和文章存在：
    if host_user and blog:
        # 如果当前用户已登录并且 id 和被访问用户相同（是本人）或者当前文章不是草稿：
        if (current_user.is_authenticated and host_user.id == current_user.id) or not blog.draft:
            form = CommentForm()
            if form.validate_on_submit():
                comment = Comment(body=form.body.data,
                                  blog_id=blog.id,
                                  author_id=host_user.id)
                db.session.add(comment)
                flash('Your comment has been published.')
                return redirect(url_for('.post', id=blog.id, page=-1, username=username))
            post = Blog.query.get_or_404(blog_id)
            page = request.args.get('page', 1, type=int)
            if page == -1:
                page = (post.comments.count() - 1) // \
                       current_app.config['BLEXT_COMMENTS_PER_PAGE'] + 1
            pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
                page, per_page=current_app.config['BLEXT_COMMENTS_PER_PAGE'],
                error_out=False)
            comments = pagination.items
            return render_template('/user/blog_page.html', blog=blog, host_user=host_user,form=form,comments=comments,pagination=pagination)
    abort(404)


# 删除用户文章（需要登录才能访问）
@login_required
@user.route('/delete/<blog_id>')
def delete_blog(blog_id):
    # 通过博客id查询到博客对象
    blog = Blog.query.filter_by(id=blog_id).first()
    # 判断是否博主本人操作
    if blog and current_user.id == blog.author_id:
        blog.delete_category()
        blog.delete_tags()
        db.session.delete(blog)
        return redirect(url_for('user.index', username=current_user.username))
    abort(404)


# 用户 About Me 页面
@user.route('/<username>/about_me')
def about_me(username):
    host_user = User.query.filter_by(username=username).first()
    if host_user:
        return render_template('user/about_me.html', about_me=host_user.about_me, host_user=host_user)
    abort(404)


@user.route('/<username>/search',methods=['GET','POST'])
def searchUser(username):
    print("in searchUser")
    if request.args.get('query', ""):
        search_username = request.args.get('query',"")
        host_user = User.query.filter_by(username=username).first_or_404()
        users = User.query.filter_by(username=search_username)
        print("here")
        if users:
            return render_template('user/search.html', users=users, host_user=host_user)
        else:
            return redirect(url_for(".index",username=username))
    else:
        return redirect(url_for(".index", username=username))

@login_required
@user.route('/<username>/all')
def show_all(username):
    resp = make_response(redirect(url_for('.index',username=username)))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@login_required
@user.route('/<username>/followed')
def show_followed(username):
    resp = make_response(redirect(url_for('.index', username=username)))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@user.route('/<username>/post/<int:id>', methods=['GET', 'POST'])
def post(username,id):
    host_user = User.query.filter_by(username=username).first()
    blog = Blog.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          blog_id=blog.id,
                          author_id=host_user.id)
        db.session.add(comment)
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=blog.id, page=-1,username=username))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (blog.comments.count() - 1) // \
            current_app.config['BLEXT_COMMENTS_PER_PAGE'] + 1
    pagination = blog.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=current_app.config['BLEXT_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    print("here",comments)
    return render_template('user/blog_page.html', blog=blog, form=form,
                           comments=comments, pagination=pagination,host_user=host_user,user=host_user)


@user.route('/<username>/follow')
@login_required
#@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', host_username=current_user.username,username=username))


@user.route('/unfollow/<username>')
@login_required
#@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', host_username=current_user.username,username=username))


@user.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@user.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@user.route('/<host_username>/<username>')
def user(host_username,username):
    print("in user",host_username,username)
    host_user = User.query.filter_by(username=host_username).first_or_404()
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    query = Blog.query
    pagination = query.order_by(Blog.timestamp.desc()).paginate(
        page, per_page=current_app.config['BLEXT_BLOGS_PER_PAGE'], error_out=False)
    blogs = pagination.items
    return render_template('user/user.html',host_user=host_user,user=user,blogs=blogs,pagination=pagination)






