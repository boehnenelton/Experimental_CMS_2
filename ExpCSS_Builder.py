# RELATIONAL_GUID: 3e685944-8c75-4d43-bdab-8bc89548dba4
# VERSION: v3.0.0
# CREDITS: Elton Boehnen (github.com/boehnenelton)
# DATE: 2026-06-06
# FILE: ExpCSS_Builder.py

"""
Experimental CSS Builder v2.0.3 - Static Site Generator
Description: Builds the static website using the BEJSON HTML Template Scaffolding.
             Rewired for block-based injection (Header, Sidebar, Body, Footer).
"""
import os
import sys
import shutil
import random
import re
from jinja2 import Template

# Add Lib_EXPCMS to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(BASE_DIR, "Lib_EXPCMS")
if LIB_DIR not in sys.path:
    sys.path.append(LIB_DIR)

from lib_expcms_mfdb import MFDB_CMS_Manager
from lib_html3_app_layout import HTML3_App_Layout
from lib_html3_list_renderer import HTML3_List_Renderer
import lib_mfdb_core as MFDBCore

class ExpCSS_Builder:
    def __init__(self, data_root: str, skel_dir: str, output_dir: str):
        self.cms = MFDB_CMS_Manager(data_root)
        self.skel_dir = skel_dir
        self.output_dir = output_dir
        self.templates_root = os.path.join(BASE_DIR, "templates")
        self.components_root = os.path.join(BASE_DIR, "Components")
        
        # Load Global Skeletons
        with open(os.path.join(skel_dir, "Global_Skeleton.html"), "r") as f:
            self.global_skel = f.read()
            
        self.random = random
        self.site_urls = []

    def _read_template(self, subpath):
        # 1. Try permanent Components library first
        if subpath.startswith("components/"):
            comp_path = os.path.join(self.components_root, subpath.replace("components/", ""))
            if os.path.exists(comp_path):
                with open(comp_path, "r") as f:
                    return f.read()
        
        # 2. Fallback to staging_templates
        path = os.path.join(self.templates_root, subpath)
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()
        return f"<!-- Template Not Found: {subpath} -->"

    def build_site(self):
        print(f"🚀 Starting ExpCSS v2.0 Build to: {self.output_dir}")
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir)
        
        # 1. Physical Assets (CSS/Apps)
        self._copy_apps()
        self._copy_assets()
        self._sync_css()

        self.site_urls = []
        # 2. Prepare Global Data
        site_config = self.cms.get_global_configs()
        self.base_url = site_config.get("base_url", "https://boehnenelton2024.pages.dev").rstrip('/')
        nav_links = self.cms.get_nav_links()
        categories = MFDBCore.mfdb_core_load_entity(self.cms.content_manifest, "Category")
        social_links = MFDBCore.mfdb_core_load_entity(self.cms.global_manifest, "SocialLink")
        
        # 3. Component Preparation
        # Header: Telemetry HUD
        header_raw = self._read_template("components/headers/Template-Header-Telemetry-HUD.html")
        header_html = Template(header_raw).render({"site_title": site_config.get("site_title", "boehnenelton2024")})

        # Footer: Status Feed + Contact Info
        footer_raw = self._read_template("components/footers/Template-Footer-Status-Feed.html")
        footer_html = Template(footer_raw).render()
        
        contact_footer = """
        <div class="c-footer-links" style="background: var(--surface); border-top: 1px solid var(--border); padding: 3rem 1rem; margin-top: 4rem;">
            <div class="container mx-auto grid grid-cols-1 md:grid-cols-3 gap-12">
                <div>
                    <h4 style="color: var(--accent); font-weight: 800; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">CONTACT</h4>
                    <p style="font-size: 0.9rem; color: #888; line-height: 1.8;">Email: info@boehnenelton.dev<br>Location: Distributed Node</p>
                </div>
                <div>
                    <h4 style="color: var(--accent); font-weight: 800; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">RESOURCES</h4>
                    <ul style="list-style: none; padding: 0; font-size: 0.9rem; color: #888; line-height: 2;">
                        <li><a href="#" style="color: inherit; text-decoration: none;">Documentation</a></li>
                        <li><a href="#" style="color: inherit; text-decoration: none;">API Status</a></li>
                    </ul>
                </div>
                <div>
                    <h4 style="color: var(--accent); font-weight: 800; margin-bottom: 1.5rem; text-transform: uppercase; letter-spacing: 1px;">LEGAL</h4>
                    <ul style="list-style: none; padding: 0; font-size: 0.9rem; color: #888; line-height: 2;">
                        <li><a href="#" style="color: inherit; text-decoration: none;">Privacy Policy</a></li>
                        <li><a href="#" style="color: inherit; text-decoration: none;">Terms of Service</a></li>
                    </ul>
                </div>
            </div>
        </div>
        """
        footer_html += contact_footer

        self.global_context = {
            "site_title": site_config.get("site_title", "ExpCSS"),
            "site_tagline": site_config.get("site_tagline", "Experimental CSS Scaffolding"),
            "nav_links": nav_links,
            "categories": categories,
            "social_links": social_links,
            "header_block": header_html,
            "footer_block": footer_html
        }

        # 4. Build Homepage
        context = self.global_context
        landing_mode = site_config.get("landing_mode", "feed")
        if landing_mode == "html":
            home_content = site_config.get("landing_html", "<h1>Welcome</h1>")
        elif landing_mode == "image":
            img = site_config.get("landing_image", "")
            home_content = f'<div class="c-hero-image" style="text-align:center; padding: 4rem 0;"><img src="assets/{img}" style="max-width:100%; border-radius:12px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1);"></div>'
        else:
            home_skel = self._read_template("components/body/Template-Standard-Hero-Section-body-component.html")
            home_content = Template(home_skel).render({
                "site_title": context["site_title"],
                "hero_sub": context["site_tagline"]
            })
        
        html = self._render_page(home_content, context)
        with open(os.path.join(self.output_dir, "index.html"), "w") as f:
            f.write(html)

        # 5. Build Categories + Pages
        for cat in categories:
            self._build_category(cat, context)

        # 6. Generate Sitemap
        self._generate_sitemap()
        print(f"✅ Build complete. {len(self.site_urls)} pages generated.")

    def _sync_css(self):
        src_css = os.path.join(self.templates_root, "css")
        if not os.path.isdir(src_css):
            return
        css_dest = os.path.join(self.output_dir, "css")
        os.makedirs(css_dest, exist_ok=True)
        for f in os.listdir(src_css):
            if f.endswith(".css"):
                shutil.copy2(os.path.join(src_css, f), os.path.join(css_dest, f))

    def _copy_apps(self):
        apps_dest = os.path.join(self.output_dir, "apps")
        if os.path.exists(self.cms.apps_dir):
            shutil.copytree(self.cms.apps_dir, apps_dest)

    def _copy_assets(self):
        assets_dest = os.path.join(self.output_dir, "assets")
        os.makedirs(assets_dest, exist_ok=True)
        
        assets = self.cms.get_assets()
        for a in assets:
            folder = a.get("folder", "")
            target_dir = os.path.join(assets_dest, folder) if folder else assets_dest
            os.makedirs(target_dir, exist_ok=True)
            
            src = os.path.join(self.cms.assets_dir, a["filename"])
            dest = os.path.join(target_dir, a["filename"])
            if os.path.exists(src):
                shutil.copy2(src, dest)

    def _generate_sidebar(self, context, rel_prefix=""):
        renderer = HTML3_List_Renderer()
        # Create temporary BEJSON for navigation
        nav_values = []
        for i, cat in enumerate(context["categories"]):
            nav_values.append([f"cat_{i}", cat["category_name"], cat.get("description", ""), None, f"{rel_prefix}{cat['category_slug']}/index.html"])
        
        # Add a placeholder for contact/info
        nav_values.append(["inf1", "Contact Us", "Get in touch", None, f"{rel_prefix}contact.html"])

        nav_doc = {
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
            "Values": nav_values
        }
        
        import json
        temp_nav_path = os.path.join(self.output_dir, "temp_nav.bejson")
        with open(temp_nav_path, 'w') as f:
            json.dump(nav_doc, f)
            
        # Using TREE mode for sidebar as per "tree nav" request
        html = renderer.render(temp_nav_path, mode="TREE", title="EXPLORE SITE")
        os.remove(temp_nav_path)
        return html

    def _render_page(self, main_content, context, rel_prefix="", related_block=""):
        # Inject Sidebar
        sidebar_html = self._generate_sidebar(context, rel_prefix)
        
        page_context = {
            **context, 
            "main_content": main_content, 
            "sidebar_block": sidebar_html,
            "rel_prefix": rel_prefix,
            "related_block": related_block,
            "related_content": bool(related_block)
        }
        return Template(self.global_skel).render(page_context)

    def _build_homepage(self, context):
        home_skel = self._read_template("components/body/Template-Standard-Hero-Section-body-component.html")
        # Customizing the Hero for the site
        home_content = Template(home_skel).render({
            "site_title": context["site_title"],
            "hero_sub": context["site_tagline"]
        })
        
        html = self._render_page(home_content, context)
        with open(os.path.join(self.output_dir, "index.html"), "w") as f:
            f.write(html)

    def _build_category(self, cat, context):
        cat_dir = os.path.join(self.output_dir, cat["category_slug"])
        os.makedirs(cat_dir, exist_ok=True)
        self.site_urls.append(f"{cat['category_slug']}/index.html")
        
        with open(os.path.join(self.skel_dir, "Category_Feed_Skeleton.html"), "r") as f:
            feed_skel = f.read()
            
        pages = self.cms.get_pages_in_category(cat["category_slug"])
        apps = self.cms.get_apps_in_category(cat["category_slug"])
        
        feed_type = cat.get("feed_type", "blog")
        
        item_html = ""
        for p in pages:
            p_data = self.cms.get_full_page_data(p["page_uuid"])
            desc = self._get_content_preview(p_data.get("html_body", "") if p_data else "")
            img_url = f"../assets/{p.get('featured_img')}" if p.get('featured_img') else ""
            
            if feed_type == 'news':
                item_html += f'''
                <div class="news-item">
                    <div class="news-thumb">{"<img src='"+img_url+"'>" if p.get('featured_img') else "<span>IMG</span>"}</div>
                    <div class="news-content">
                        <div class="news-category">{cat["category_name"]}</div>
                        <h2 class="news-title"><a href="{p["slug"]}/index.html">{p["title"]}</a></h2>
                        <p class="news-excerpt">{desc}</p>
                        <div class="news-meta"><span>{p.get("created_at")}</span></div>
                    </div>
                </div>'''
            elif feed_type == 'products':
                item_html += f'''
                <div class="product-card">
                    <div class="product-img">{"<img src='"+img_url+"'>" if p.get('featured_img') else "<span>PRODUCT</span>"}</div>
                    <div class="product-details">
                        <div class="product-title"><a href="{p["slug"]}/index.html">{p["title"]}</a></div>
                        <div class="product-price-row"><button class="product-add">VIEW</button></div>
                    </div>
                </div>'''
            elif feed_type == 'masonry':
                item_html += f'''
                <div class="masonry-item">
                    {"<img src='"+img_url+"'>" if p.get('featured_img') else "<div style='height:200px;background:#222;'></div>"}
                    <div class="masonry-overlay"><div class="masonry-title"><a href="{p["slug"]}/index.html">{p["title"]}</a></div></div>
                </div>'''
            else: # Blog
                item_html += f'''
                <div class="blog-card">
                    <div class="blog-thumb">{"<img src='"+img_url+"'>" if p.get('featured_img') else "IMG"}</div>
                    <div class="blog-card-body">
                        <p class="blog-card-title"><a href="{p["slug"]}/index.html">{p["title"]}</a></p>
                        <p class="blog-card-excerpt">{desc}</p>
                        <span class="blog-card-meta">{p.get("created_at")}</span>
                    </div>
                </div>'''
            
        feed_content = Template(feed_skel).render({
            "category_name": cat["category_name"],
            "category_description": cat["description"],
            "feed_type": feed_type,
            "content_items": item_html
        })
        
        html = self._render_page(feed_content, context, rel_prefix="../")
        with open(os.path.join(cat_dir, "index.html"), "w") as f:
            f.write(html)
            
        for p in pages:
            self._build_page(p, cat, context)

    def _build_page(self, page, cat, context):
        page_uuid = page["page_uuid"]
        page_data = self.cms.get_full_page_data(page_uuid)
        page_dir = os.path.join(self.output_dir, cat["category_slug"], page["slug"])
        os.makedirs(page_dir, exist_ok=True)
        self.site_urls.append(f"{cat['category_slug']}/{page['slug']}/index.html")
        
        with open(os.path.join(self.skel_dir, "Article_Skeleton.html"), "r") as f:
            page_skel = f.read()
            
        page_content = Template(page_skel).render({
            **page_data,
            "category_name": cat["category_name"],
            "rel_prefix": "../../"
        })
        
        html = self._render_page(page_content, context, rel_prefix="../../")
        with open(os.path.join(page_dir, "index.html"), "w") as f:
            f.write(html)

    def _get_content_preview(self, html, length=150):
        clean = re.sub('<[^<]+?>', '', html)
        return (clean[:length] + '...') if len(clean) > length else clean

    def _generate_sitemap(self):
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        xml += f'  <url><loc>{self.base_url}/index.html</loc><priority>1.0</priority></url>\n'
        for url in self.site_urls:
            xml += f'  <url><loc>{self.base_url}/{url}</loc><priority>0.8</priority></url>\n'
        xml += '</urlset>'
        with open(os.path.join(self.output_dir, "sitemap.xml"), "w") as f:
            f.write(xml)

if __name__ == "__main__":
    builder = ExpCSS_Builder(
        data_root=os.path.join(BASE_DIR, "Data"),
        skel_dir=os.path.join(BASE_DIR, "HTML_Skeletons"),
        output_dir=os.path.join(BASE_DIR, "Processing", "www")
    )
    builder.build_site()
