from flask import render_template
from markupsafe import Markup
import markdown2
import os
from . import data_providers # Import the new data providers module

def register_routes(app):
    """
    Dynamically registers Flask routes based on the configuration.
    """
    config = app.config.get('GENERATOR_CONFIG')
    if not config or 'routes' not in config:
        return

    def view_factory(route_config):
        def generic_view():
            app_root = app.root_path

            # --- Prepare base context ---
            context = {
                'pageTitle': route_config.get('title', route_config.get('name', 'Page').capitalize()),
                'site': config.get('metadata', {}),
                'page': route_config
            }

            # --- Load Primary Markdown Content ---
            if 'content_md' in route_config:
                md_path = os.path.join(app_root, route_config['content_md'])
                try:
                    with open(md_path, 'r', encoding='utf-8') as f:
                        # Add to context with a generic name 'content'
                        context['content'] = Markup(markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"]))
                except FileNotFoundError:
                    context['content'] = ""

            # --- Load Extra Markdown Content ---
            if 'content_extra' in route_config:
                for extra in route_config['content_extra']:
                    extra_md_path = os.path.join(app_root, extra['source'])
                    try:
                        with open(extra_md_path, 'r', encoding='utf-8') as f:
                            # Add to context using the specified name
                            context[extra['name']] = Markup(markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"]))
                    except FileNotFoundError:
                        context[extra['name']] = ""

            # --- Get data from a data provider function ---
            if 'data_provider' in route_config:
                provider_name = route_config['data_provider']
                # Get the function from the data_providers module
                provider_func = getattr(data_providers, provider_name, None)
                if provider_func and callable(provider_func):
                    # Call the function and update the context with its results
                    data = provider_func(app)
                    context.update(data)

            template = route_config.get('template', 'base.html')
            return render_template(template, **context)

        return generic_view

    for route_info in config['routes']:
        path = route_info['path']
        endpoint_name = route_info.get('name', f"route_{path.replace('/', '_').strip('_')}")

        view_func = view_factory(route_info)
        app.add_url_rule(path, endpoint=endpoint_name, view_func=view_func)
