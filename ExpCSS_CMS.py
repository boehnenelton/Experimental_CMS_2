# RELATIONAL_GUID: 3e685944-8c75-4d43-bdab-8bc89548dba4
# VERSION: v2.4.3
# CREDITS: Elton Boehnen (github.com/boehnenelton)
# FILE: ExpCSS_CMS_v2.4.2.py
# DATE: 2026-06-03

"""
Experimental CSS CMS v2.4.2 - Unified Administrative Dashboard (HTML3)
Description: Unified management tool for MFDB data, content editing, and site deployment.
             Updated with HTML3 Layout, List Renderer, and Dynamic Tables.
"""
import os
import sys
import uuid
import collections
import subprocess
import threading
import http.server
import socketserver
import json
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename

# Add Lib to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(BASE_DIR, "Lib")
if LIB_DIR not in sys.path:
    sys.path.append(LIB_DIR)

from lib_cms_mfdb import MFDB_CMS_Manager
from lib_bejson_html3_skeletons import COLOR, BRUTAL_COLOR, CSS_CORE, CSS_BRUTAL, HTML_SKELETON, HTML_SKELETON_BRUTAL
from lib_html3_sidemenu import _sidebar_html
from lib_html3_list_renderer import HTML3_List_Renderer
from lib_html3_body import html_card, html_stats_bar, html_code_box, html_brutal_table
from lib_html3_tables import html_table
from lib_html3_widgets import html_widget, html_info_box
from lib_cms_chunker_wrapper import CMS_Chunker_Wrapper
import lib_mfdb_core as MFDBCore

# --- Flask App Initialization ---
import mimetypes
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

app = Flask(__name__, 
            static_folder=os.path.join(BASE_DIR, "templates"),
            static_url_path='/static')
app.secret_key = 'expcss-unified-v2-secret'
app.jinja_env.add_extension('jinja2.ext.do')

@app.context_processor
def inject_html3():
    # Render master CSS
    becss_css = CSS_CORE.format(**COLOR)
    return dict(
        becss_css=becss_css,
        sidebar_html=get_sidebar_html(),
        html_card=html_card,
        html_stats_bar=html_stats_bar,
        html_code_box=html_code_box,
        html_brutal_table=html_brutal_table,
        html_table=html_table,
        html_widget=html_widget,
        html_info_box=html_info_box
    )

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(BASE_DIR, "Assets"), filename)

DATA_ROOT = os.path.join(BASE_DIR, "Data")
WWW_ROOT = os.path.join(BASE_DIR, "Processing", "www")
cms = MFDB_CMS_Manager(DATA_ROOT)
chunker = CMS_Chunker_Wrapper(cms)

# Initialize databases on start
with app.app_context():
    cms.initialize_system()

# --- Preview Server State ---
_preview_srv = {
    "thread": None,
    "httpd": None,
    "port": 8080,
    "running": False
}

@app.route('/')
def dashboard():
    global_stats = MFDBCore.mfdb_core_get_stats(cms.global_manifest)
    content_stats = MFDBCore.mfdb_core_get_stats(cms.content_manifest)
    return render_template("dashboard.html", g_stats=global_stats, c_stats=content_stats)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/landing_editor', methods=['GET', 'POST'])
def landing_editor():
    if request.method == 'POST':
        cms.add_global_config("landing_mode", request.form.get('landing_mode'))
        cms.add_global_config("landing_html", request.form.get('landing_html'))
        cms.add_global_config("landing_image", request.form.get('landing_image'))
        flash('Landing page configuration updated')
        return redirect(url_for('landing_editor'))
    
    configs = cms.get_global_configs()
    assets = cms.get_assets()
    return render_template("landing_editor.html", configs=configs, assets=assets)

@app.route('/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        for key, value in request.form.items():
            cms.add_global_config(key, value)
        flash('Configuration updated')
        return redirect(url_for('config'))
    
    configs = cms.get_global_configs()
    return render_template("config.html", configs=configs)

@app.route('/factory_reset')
def reset_system():
    cms.factory_reset()
    cms.initialize_system()
    flash("System has been factory reset.")
    return redirect(url_for('dashboard'))

@app.route('/repack')
def repack_system():
    cms.repack_system()
    flash("System repacked and changes committed.")
    return redirect(url_for('dashboard'))

# =============================================================================
# MEDIA LIBRARY
# =============================================================================

@app.route('/media')
def media_library():
    all_assets = cms.get_assets()
    grouped = collections.defaultdict(list)
    for a in all_assets:
        char = a['filename'][0].upper() if a['filename'][0].isalpha() else '#'
        grouped[char].append(a)
    
    sorted_groups = sorted(grouped.items())
    return render_template("media_library.html", groups=sorted_groups)

@app.route('/media/upload', methods=['POST'])
def media_upload():
    import zipfile
    files = request.files.getlist('files')
    uploaded = 0
    skipped = 0
    
    def process_data(data, original_filename, content_type, folder=""):
        nonlocal uploaded, skipped
        if not content_type.startswith('image/'):
            # Basic extension check as fallback
            if not original_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')):
                skipped += 1
                return False
        
        f_hash = cms.get_file_hash(data)
        if cms.get_asset_by_hash(f_hash):
            skipped += 1
            return False
            
        filename = secure_filename(original_filename)
        if os.path.exists(os.path.join(cms.assets_dir, filename)):
            base, ext = os.path.splitext(filename)
            filename = f"{base}_{uuid.uuid4().hex[:4]}{ext}"
            
        with open(os.path.join(cms.assets_dir, filename), "wb") as wf:
            wf.write(data)
        cms.add_asset(filename, original_filename, f_hash, len(data), content_type, folder)
        uploaded += 1
        return True

    for f in files:
        if f:
            if f.filename.endswith('.zip'):
                with zipfile.ZipFile(f, 'r') as z:
                    for name in z.namelist():
                        if name.startswith('__MACOSX') or name.endswith('/'): continue
                        folder = os.path.dirname(name)
                        data = z.read(name)
                        process_data(data, os.path.basename(name), mimetypes.guess_type(name)[0] or 'application/octet-stream', folder)
            else:
                process_data(f.read(), f.filename, f.content_type)
            
    flash(f"Uploaded {uploaded}, Skipped {skipped}")
    return redirect(url_for('media_library'))

@app.route('/media/serve/<path:filename>')
def serve_media(filename):
    return send_from_directory(cms.assets_dir, filename)

@app.route('/media/delete/<filename>')
def media_delete(filename):
    if cms.delete_asset(filename):
        flash("Asset deleted")
    return redirect(url_for('media_library'))

# =============================================================================
# CONTENT & CATEGORIES
# =============================================================================

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        slug = request.form.get('slug')
        desc = request.form.get('description')
        feed = request.form.get('feed_type')
        is_update = request.form.get('is_update') == 'true'
        
        if is_update:
            cms.update_category(slug, name, desc, feed)
            flash('Category updated')
        else:
            cms.add_category(name, slug, desc, feed)
            flash('Category added successfully')
        return redirect(url_for('categories'))

    cats_doc = MFDBCore.bejson_core_load_file(os.path.join(cms.content_db_root, 'data', 'category.bejson'))
    return render_template("categories.html", cats_doc=cats_doc)

@app.route('/categories/delete/<slug>')
def category_delete(slug):
    if slug == "uncategorized":
        flash('Cannot delete the default category.')
    else:
        cms.delete_category(slug)
        flash('Category deleted')
    return redirect(url_for('categories'))

@app.route('/pages')
def pages():
    pages_doc = MFDBCore.bejson_core_load_file(os.path.join(cms.content_db_root, "data", "page.bejson"))
    return render_template("editor_list.html", pages_doc=pages_doc)

@app.route('/new')
def new_page():
    p = {
        "page_uuid": "", "title": "", "page_type": "article", 
        "category_fk": "uncategorized", "author_fk": "", 
        "featured_img": "", "html_body": "", "video_url": "", 
        "pdf_url": "", "source_files": []
    }
    return edit_page_view(p)

@app.route('/edit/<uuid>')
def edit_page(uuid):
    page_data = cms.get_full_page_data(uuid)
    if not page_data: return "Page not found", 404
    return edit_page_view(page_data)

def edit_page_view(p):
    cats = MFDBCore.mfdb_core_load_entity(cms.content_manifest, "Category")
    authors = cms.get_authors()
    assets = cms.get_assets()
    return render_template("editor_main.html", p=p, cats=cats, authors=authors, assets=assets)

@app.route('/save', methods=['POST'])
def save_page():
    uuid_val = request.form.get('page_uuid')
    title = request.form.get('title')
    cat = request.form.get('category')
    ptype = request.form.get('page_type')
    html_body = request.form.get('html_body')
    
    content_data = {"html_body": html_body}
    if ptype == 'video':
        content_data["video_url"] = request.form.get('video_url')
    elif ptype == 'pdf-viewer':
        content_data["pdf_url"] = request.form.get('pdf_url')
    elif ptype == 'source-code':
        source_files_json = request.form.get('source_files_json')
        if source_files_json:
            content_data["source_files"] = json.loads(source_files_json)
        else:
            content_data["source_files"] = []
            
    content_data["author_fk"] = request.form.get('author_fk')
    content_data["featured_img"] = request.form.get('featured_img')

    if uuid_val:
        cms.update_page(uuid_val, title, cat, ptype, content_data)
        flash("Page updated successfully")
    else:
        cms.create_page(title, cat, ptype, content_data)
        flash("New page created")
        
    return redirect(url_for('pages'))

@app.route('/pages/delete/<uuid>')
def page_delete(uuid):
    cms.delete_page(uuid)
    flash("Page deleted")
    return redirect(url_for('pages'))

# =============================================================================
# APPS & NAVIGATION
# =============================================================================

@app.route('/apps', methods=['GET', 'POST'])
def apps():
    import zipfile
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('description')
        cat = request.form.get('category')
        feat_img = request.form.get('featured_img')
        entry = request.form.get('entry_file', 'index.html')
        
        app_file = request.files.get('app_file')
        app_uuid = str(uuid.uuid4())
        app_dir = os.path.join(cms.apps_dir, app_uuid)
        os.makedirs(app_dir, exist_ok=True)

        if app_file:
            fname = secure_filename(app_file.filename)
            fpath = os.path.join(app_dir, fname)
            app_file.save(fpath)
            
            if fname.endswith('.zip'):
                with zipfile.ZipFile(fpath, 'r') as z:
                    z.extractall(app_dir)
                os.remove(fpath)
            else:
                entry = fname
                
        cms.create_app(name, desc, cat, feat_img, entry)
        flash("App imported successfully")
        return redirect(url_for('apps'))

    apps_list = cms.get_apps()
    cats = MFDBCore.mfdb_core_load_entity(cms.content_manifest, "Category")
    assets = cms.get_assets()
    return render_template("apps.html", apps=apps_list, cats=cats, assets=assets)

@app.route('/apps/delete/<uuid>')
def app_delete(uuid):
    cms.delete_app(uuid)
    flash("App deleted")
    return redirect(url_for('apps'))

@app.route('/navigation', methods=['GET', 'POST'])
def navigation():
    if request.method == 'POST':
        label = request.form.get('label')
        url = request.form.get('url')
        cms.add_nav_link(label, url)
        flash('Navigation link added')
        return redirect(url_for('navigation'))
    
    links = cms.get_nav_links()
    return render_template("navigation.html", links=links)

@app.route('/navigation/delete/<label>')
def navigation_delete(label):
    cms.delete_nav_link(label)
    return redirect(url_for('navigation'))

# =============================================================================
# AUTHORS & ADS
# =============================================================================

@app.route('/authors', methods=['GET', 'POST'])
def authors():
    if request.method == 'POST':
        name = request.form.get('name')
        bio = request.form.get('bio')
        img = request.form.get('image_url')
        uuid_val = request.form.get('author_uuid')
        
        if uuid_val:
            cms.update_author(uuid_val, name, bio, img)
            flash('Author updated')
        else:
            cms.add_author(name, bio, img)
            flash('Author added')
        return redirect(url_for('authors'))
    
    authors_list = cms.get_authors()
    assets = cms.get_assets()
    return render_template("authors.html", authors=authors_list, assets=assets)

@app.route('/authors/delete/<uuid>')
def author_delete(uuid):
    cms.delete_author(uuid)
    flash("Author deleted")
    return redirect(url_for('authors'))

@app.route('/ads', methods=['GET', 'POST'])
def ads():
    if request.method == 'POST':
        name = request.form.get('name')
        img = request.form.get('image_url')
        link = request.form.get('link_url')
        zone = request.form.get('zone')
        uuid_val = request.form.get('ad_uuid')
        active = request.form.get('active') == 'true'
        
        if uuid_val:
            cms.update_ad(uuid_val, name, img, link, zone, active)
            flash('Ad updated')
        else:
            cms.add_ad(name, img, link, zone, active)
            flash('Ad added')
        return redirect(url_for('ads'))

    ads_list = cms.get_ads()
    assets = cms.get_assets()
    return render_template("ads.html", ads=ads_list, assets=assets)

@app.route('/ads/delete/<uuid>')
def ad_delete(uuid):
    cms.delete_ad(uuid)
    flash('Ad deleted')
    return redirect(url_for('ads'))

# =============================================================================
# BUILD & PREVIEW
# =============================================================================

@app.route('/build')
def build_site():
    try:
        result = subprocess.run([sys.executable, "ExpCSS_Builder.py"], capture_output=True, text=True, cwd=BASE_DIR)
        if result.returncode == 0:
            flash("Site built successfully! Reloading Preview Server...")
            if _preview_srv["running"]:
                srv_stop()
                srv_start()
        else:
            flash(f"Build failed: {result.stderr}")
    except Exception as e:
        flash(f"Build error: {str(e)}")
    return redirect(url_for('dashboard'))

@app.route('/preview_srv')
def preview_manager():
    status = _preview_srv["running"]
    url = f"http://{request.host.split(':')[0]}:{_preview_srv['port']}"
    return render_template("preview_manager.html", running=status, url=url)

@app.route('/srv/start')
def srv_start():
    if not _preview_srv["running"]:
        def run_srv():
            import functools
            handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=WWW_ROOT)
            socketserver.TCPServer.allow_reuse_address = True
            _preview_srv["httpd"] = socketserver.TCPServer(("", _preview_srv["port"]), handler)
            _preview_srv["running"] = True
            _preview_srv["httpd"].serve_forever()
        
        _preview_srv["thread"] = threading.Thread(target=run_srv, daemon=True)
        _preview_srv["thread"].start()
        flash("Preview server started")
    return redirect(url_for('preview_manager'))

@app.route('/srv/stop')
def srv_stop():
    if _preview_srv["running"] and _preview_srv["httpd"]:
        _preview_srv["httpd"].shutdown()
        _preview_srv["httpd"].server_close()
        _preview_srv["running"] = False
        flash("Preview server stopped")
    return redirect(url_for('preview_manager'))


# =============================================================================
# BACKUP & CHUNKING
# =============================================================================

@app.route('/backups')
def backups():
    all_backups = chunker.list_backups()
    return render_template("backups.html", backups=all_backups)

@app.route('/backup/create', methods=['POST'])
def backup_create():
    changelog = request.form.get("changelog", "Manual Backup")
    result = chunker.backup_site(changelog=changelog)
    if result["success"]:
        flash(f"Backup created: {result['zip_path']}")
    else:
        flash(f"Backup failed: {result['error']}")
    return redirect(url_for('backups'))

@app.route('/backup/restore', methods=['POST'])
def backup_restore():
    filename = request.form.get("filename")
    result = chunker.restore_site(filename)
    if result["success"]:
        flash(result["message"])
    else:
        flash(f"Restore failed: {result['error']}")
    return redirect(url_for('backups'))

@app.route('/backup/download/<filename>')
def backup_download(filename):
    return send_from_directory(chunker.backup_dir, filename, as_attachment=True)

# --- HTML3 Integration ---
def get_sidebar_html():
    renderer = HTML3_List_Renderer()
    nav_data = {
        "Format": "BEJSON",
        "Format_Version": "104",
        "Format_Creator": "Elton Boehnen",
        "Records_Type": ["NavItem"],
        "Fields": [
            {"name": "id", "type": "string"},
            {"name": "title", "type": "string"},
            {"name": "description", "type": "string"},
            {"name": "parent_id_fk", "type": "string"},
            {"name": "url", "type": "string"}
        ],
        "Values": [
            ["d1", "Dashboard", "", None, "/"],
            ["c1", "Categories", "", None, "/categories"],
            ["p1", "Pages", "", None, "/pages"],
            ["a1", "Standalone Apps", "", None, "/apps"],
            ["m1", "Media Library", "", None, "/media"],
            ["au1", "Authors", "", None, "/authors"],
            ["n1", "Nav Links", "", None, "/navigation"],
            ["ad1", "Ad Rotator", "", None, "/ads"],
            ["pr1", "Preview Manager", "", None, "/preview_srv"],
            ["bk1", "Site Backups", "", None, "/backups"],
            ["bld1", "Build Site", "", None, "/build"],
            ["rp1", "Repack System", "", None, "/repack"],
            ["cfg1", "Global Config", "", None, "/config"]
        ]
    }
    temp_path = os.path.join(BASE_DIR, "Data", "admin_nav.bejson")
    with open(temp_path, 'w') as f:
        json.dump(nav_data, f)
    
    return renderer.render(temp_path, mode="SIDEBAR", title="System Orbit")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
