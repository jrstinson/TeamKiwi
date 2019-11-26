"""
    Routes
    ~~~~~~
"""
import pdfkit, os, uuid
from flask import Blueprint, Response, app, current_app
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import g
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from wiki.core import Processor
from wiki.web.forms import EditorForm, UploadForm
from wiki.web.forms import LoginForm
from wiki.web.forms import SearchForm
from wiki.web.forms import RegistrationForm
from wiki.web.forms import URLForm
from wiki.web import current_wiki
from wiki.web import current_users
from wiki.web.user import protect
from wiki.web.user import protect, UserManager
from werkzeug.utils import secure_filename


bp = Blueprint('wiki', __name__)
file_location = 'textfiles'
allowed_file_extensions = ["MD", "TXT", "HTML", "RTF", "XML"]


@bp.route('/')
@protect
def home():
    page = current_wiki.get('home')
    if page:
        return display('home')
    return render_template('home.html')


@bp.route('/index/')
@protect
def index():
    pages = current_wiki.index()
    return render_template('index.html', pages=pages)


@bp.route('/<path:url>/')
@protect
def display(url):
    page = current_wiki.get_or_404(url)
    if page.owner:
        owning_user = current_users.get_user(page.owner)
        if page.owner == current_user.get_id():
            return render_template('page.html', page=page, ou=owning_user)
        else:
            return render_template('page.html', page=page, flag='readonly', ou=owning_user)
    return render_template('page.html', page=page)


@bp.route('/create/', methods=['GET', 'POST'])
@protect
def create():
    form = URLForm()
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.edit', url=form.clean_url(form.url.data)))
    return render_template('create.html', form=form)


@bp.route('/edit/<path:url>/', methods=['GET', 'POST'])
@protect
def edit(url):
    page = current_wiki.get(url)
    if page:
        if page.owner:
            if page.owner == current_user.get_id():
                form = EditorForm(obj=page)
                if form.validate_on_submit():
                    if not page:
                        page = current_wiki.get_bare(url)
                    if form.image.data:
                        directory = "wiki/web/static/picture/{}".format(url)
                        if not os.path.exists(directory):
                            os.makedirs(directory)
                        f = request.files['image']
                        sfname = "{}/{}".format(directory, str(secure_filename(f.filename)))
                        f.save(sfname)
                        form.body.data = form.body.data + "\n![{}](/static/picture/{}/{})".format(f.filename, url,
                                                                                                  f.filename)
                    form.populate_obj(page)
                    page.save()
                    flash('"%s" was saved.' % page.title, 'success')
                    return redirect(url_for('wiki.display', url=url))
                return render_template('editor.html', form=form, page=page)
            else:
                if page.owner == "admin":
                    flash('This page is locked to editing by the site administrators.')
                else:
                    flash('You must own this page to move it', 'success')
                return redirect(url_for('wiki.display', url=url))
        else:
            form = EditorForm(obj=page)
            if form.validate_on_submit():
                if not page:
                    page = current_wiki.get_bare(url)
                if form.image.data:
                    directory = "wiki/web/static/picture/{}".format(url)
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    f = request.files['image']
                    sfname = "{}/{}".format(directory, str(secure_filename(f.filename)))
                    f.save(sfname)
                    form.body.data = form.body.data + "\n![{}](/static/picture/{}/{})".format(f.filename, url,
                                                                                              f.filename)
                form.populate_obj(page)
                page.save()
                flash('"%s" was saved.' % page.title, 'success')
                return redirect(url_for('wiki.display', url=url))
    else:
        form = EditorForm(obj=page)
        if form.validate_on_submit():
            if not page:
                page = current_wiki.get_bare(url)
            if form.image.data:
                directory = "wiki/web/static/picture/{}".format(url)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                f = request.files['image']
                sfname = "{}/{}".format(directory, str(secure_filename(f.filename)))
                f.save(sfname)
                form.body.data = form.body.data + "\n![{}](/static/picture/{}/{})".format(f.filename, url, f.filename)
            form.populate_obj(page)
            page.save()
            flash('"%s" was saved.' % page.title, 'success')
            return redirect(url_for('wiki.display', url=url))
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        if not page:
            page = current_wiki.get_bare(url)
        if form.image.data:
            directory = "wiki/web/static/picture/{}".format(url)
            if not os.path.exists(directory):
                os.makedirs(directory)
            f = request.files['image']
            sfname = "{}/{}".format(directory,str(secure_filename(f.filename)))
            f.save(sfname)
            form.body.data = form.body.data + "\n![{}](/static/picture/{}/{})".format(f.filename,url,f.filename)
        form.populate_obj(page)
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=url))
    return render_template('editor.html', form=form, page=page)


@bp.route('/picture/<path:url>/<path:image_name>')
def picture(url,image_name):
    img_url = "/static/picture/{}/{}".format(url,image_name)
    return render_template('picture.html',img_url = img_url,img_name=image_name)


file_location = 'textfiles'
allowed_file_extensions = ["MD", "TXT", "HTML", "RTF", "XML"]



def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in allowed_file_extensions:
        return True
    else:
        return False


@bp.route('/upload/', methods=['GET', 'POST'])
@protect
def upload():

    form = UploadForm()
    if request.method == "POST":

        if request.files:
            file = request.files["file"]

            if file.filename == "":
                print ("No filename")
                return redirect(request.url)
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(filename)
                #return redirect(request.url)

                mdname = 'content\\'+form.url.data+'.md'

                f = open(filename)
                if 'title:' not in f.read():
                    f1 = open(mdname, "w")
                    f1.write('title: Default Title\ntags:\n\n')
                    f1.close()
                    f.close()
                with open(filename) as f:
                    with open(mdname, "a+") as f1:
                        for line in f:
                            f1.write(line)

                os.remove(filename)

            else:
                print("That file extension is not allowed. Please select a valid file extension (.md, .txt, .rtf, .html, .xml")
                flash("That file extension is not allowed. Please select a valid file extension (.md, .txt, .rtf, .html, .xml)")
                return redirect(request.url)

        if form.validate_on_submit():
            return redirect(url_for(
                'wiki.edit', url=form.clean_url(form.url.data)))

    return render_template('upload.html', form=form)


@bp.route('/export/<path:url>/', methods=['GET', 'POST'])
@protect
def export(url):
    page = current_wiki.get(url)
    md = current_wiki.get_md(url)
    filename = url+'.md'
    return Response(
        md,
        mimetype="application/md",
        headers={
            "Content-disposition": "attachment; filename=" + filename,
            "Content-type": "application/force-download"
        }
    )


@bp.route('/saveas/<path:url>/', methods=['POST', 'GET'])
@protect
def saveas(url):
    old_page = current_wiki.get_or_404(url)
    form = URLForm(obj=old_page)
    if form.validate_on_submit():
        return redirect(url_for(
            'wiki.copy', oldurl=form.clean_url(url), newurl=form.clean_url(form.url.data)
        ))
    return render_template('saveas.html', form=form)


@bp.route('/copy/<path:oldurl>/<path:newurl>', methods=['POST', 'GET'])
@protect
def copy(oldurl, newurl):
    old_page = current_wiki.get(oldurl)
    new_page = current_wiki.get(newurl)
    form = EditorForm(obj=old_page)
    if form.validate_on_submit():
        if not new_page:
            new_page = current_wiki.get_bare(newurl)
        form.populate_obj(new_page)
        new_page.save()
        flash('"%s" was saved.' % new_page.title, 'success')
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('copyeditor.html', form=form, page=old_page, url=newurl)


@bp.route('/profile/<path:user_id>', methods=['POST', 'GET'])
def profile(user_id):
    page = current_wiki.get(user_id)
    if page:
        if page.owner:
            if current_user.get_id() == page.owner:
                return redirect(url_for('wiki.display', url=user_id))
            else:
                flash("Sorry, you can't access another user's profile.", 'success')
                return render_template('home.html')
        else:
            return redirect(url_for('wiki.display', url=user_id))
    form = EditorForm(obj=page)
    if form.validate_on_submit():
        page = current_wiki.get_bare(user_id)
        form.populate_obj(page)
        page.owner = current_user.get_id()
        page.save()
        flash('"%s" was saved.' % page.title, 'success')
        return redirect(url_for('wiki.display', url=user_id))
    return render_template('editor.html', form=form, page=page, uid=user_id)


@bp.route('/preview/', methods=['POST'])
@protect
def preview():
    data = {}
    processor = Processor(request.form['body'])
    data['html'], data['body'], data['meta'] = processor.process()
    return data['html']


@bp.route('/move/<path:url>/', methods=['GET', 'POST'])
@protect
def move(url):
    page = current_wiki.get_or_404(url)
    if page.owner:
        if current_user.get_id() == page.owner:
            form = URLForm(obj=page)
            if form.validate_on_submit():
                newurl = form.url.data
                current_wiki.move(url, newurl)
                return redirect(url_for('wiki.display', url=newurl))
        else:
            if page.owner == "admin":
                flash('This page is locked to editing by the site administrators.')
            else:
                flash('You must own this page to move it', 'success')
            return redirect(url_for('wiki.display', url=url))
    form = URLForm(obj=page)
    if form.validate_on_submit():
        newurl = form.url.data
        current_wiki.move(url, newurl)
        return redirect(url_for('wiki.display', url=newurl))
    return render_template('move.html', form=form, page=page)


@bp.route('/delete/<path:url>/')
@protect
def delete(url):
    page = current_wiki.get_or_404(url)
    if page.owner:
        if current_user.get_id() == page.owner:
            current_wiki.delete(url)
            flash('Page "%s" was deleted.' % page.title, 'success')
            return redirect(url_for('wiki.home'))
        else:
            if page.owner == "admin":
                flash('This page is locked to editing by the site administrators.')
            else:
                flash('You must own this page to move it', 'success')
            return redirect(url_for('wiki.display', url=url))
    current_wiki.delete(url)
    flash('Page "%s" was deleted.' % page.title, 'success')
    return redirect(url_for('wiki.home'))


@bp.route('/tags/')
@protect
def tags():
    tags = current_wiki.get_tags()
    return render_template('tags.html', tags=tags)


@bp.route('/tag/<string:name>/')
@protect
def tag(name):
    tagged = current_wiki.index_by_tag(name)
    return render_template('tag.html', pages=tagged, tag=name)


@bp.route('/search/', methods=['GET', 'POST'])
@protect
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = current_wiki.search(form.term.data, form.ignore_case.data)
        return render_template('search.html', form=form,
                               results=results, search=form.term.data)
    return render_template('search.html', form=form, search=None)


@bp.route('/user/login/', methods=['GET', 'POST'])
def user_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = current_users.get_user(form.name.data)
        login_user(user)
        user.set('authenticated', True)
        flash('Login successful.', 'success')
        return redirect(request.args.get("next") or url_for('wiki.home'))
    return render_template('login.html', form=form)


@bp.route('/user/logout/')
@login_required
def user_logout():
    current_user.set('authenticated', False)
    logout_user()
    flash('Logout successful.', 'success')
    return redirect(url_for('wiki.index'))


@bp.route('/user/')
def user_index():
    pass


@bp.route('/user/<int:user_id>/')
def user_admin(user_id):
    pass


@bp.route('/user/delete/<int:user_id>/')
def user_delete(user_id):
    pass

"""
Written by: Nick Peace

"""


@bp.route('/register/', methods=['GET','POST'])
def user_create():
    try:
        form = RegistrationForm()

        if request.method == "POST" and form.validate_on_submit():
            username = form.user.data
            password = form.password.data
            fullName = form.fullName.data
            email = form.email.data
            bio = form.bio.data
            favoriteLanguages = form.favoriteLanguages.data

            if current_users.get_user(username):
                flash("That username is already taken! please try again")
                return render_template('register.html', form=form)

            user = current_users.add_user(username,password,email,fullName,bio,favoriteLanguages)
            login_user(user)
            user.set('authenticated', True)
            flash('Thanks for registering! Welcome to Kiwi.', 'success')
            return redirect(request.args.get("next") or url_for('wiki.index'))

        return render_template('register.html',form=form)

    except Exception as e:
        return(str(e))


"""
    Error Handlers
    ~~~~~~~~~~~~~~
"""


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

