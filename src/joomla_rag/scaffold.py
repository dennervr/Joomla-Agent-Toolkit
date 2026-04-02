import os
from pathlib import Path

def scaffold_component(name: str, path: str = "."):
    """
    Scaffold a basic Joomla 4/5 MVC component structure.
    """
    # Normalize name
    if not name.startswith('com_'):
        name = 'com_' + name
    
    # Compute display name and namespace
    display_name = name.replace('com_', '').title()
    namespace_prefix = 'Com' + display_name
    upper_name = name.replace('com_', '').upper()
    
    # Ensure path exists
    path_obj = Path(path)
    if not path_obj.exists():
        path_obj.mkdir(parents=True, exist_ok=True)
    
    # Define directories
    site_dir = path_obj / 'components' / name
    admin_dir = path_obj / 'administrator' / 'components' / name
    
    # Create directories
    site_dir.mkdir(parents=True, exist_ok=True)
    admin_dir.mkdir(parents=True, exist_ok=True)
    
    # Site files
    # name.php
    site_entry = site_dir / f'{name}.php'
    site_entry_content = f'''<?php
defined('_JEXEC') or die;

use Joomla\\CMS\\Factory;
use Joomla\\CMS\\Dispatcher\\ComponentDispatcher;

$dispatcher = new ComponentDispatcher('{namespace_prefix}');
$dispatcher->dispatch();
'''
    with open(site_entry, 'w') as f:
        f.write(site_entry_content)
    
    # src/Controller/DisplayController.php
    controller_dir = site_dir / 'src' / 'Controller'
    controller_dir.mkdir(parents=True, exist_ok=True)
    controller_file = controller_dir / 'DisplayController.php'
    controller_content = f'''<?php
namespace {namespace_prefix}\\Site\\Controller;

use Joomla\\CMS\\MVC\\Controller\\BaseController;

class DisplayController extends BaseController
{{
    public function display($cachable = false, $urlparams = false)
    {{
        $this->input->set('view', 'example');
        parent::display($cachable, $urlparams);
    }}
}}
'''
    with open(controller_file, 'w') as f:
        f.write(controller_content)
    
    # src/View/Example/HtmlView.php
    view_dir = site_dir / 'src' / 'View' / 'Example'
    view_dir.mkdir(parents=True, exist_ok=True)
    view_file = view_dir / 'HtmlView.php'
    view_content = f'''<?php
namespace {namespace_prefix}\\Site\\View\\Example;

use Joomla\\CMS\\MVC\\View\\HtmlView as BaseHtmlView;

class HtmlView extends BaseHtmlView
{{
    public function display($tpl = null)
    {{
        parent::display($tpl);
    }}
}}
'''
    with open(view_file, 'w') as f:
        f.write(view_content)
    
    # tmpl/example/default.php
    tmpl_dir = site_dir / 'tmpl' / 'example'
    tmpl_dir.mkdir(parents=True, exist_ok=True)
    tmpl_file = tmpl_dir / 'default.php'
    tmpl_content = f'<h1>Hello from {name}</h1>'
    with open(tmpl_file, 'w') as f:
        f.write(tmpl_content)
    
    # Admin files
    # name.php
    admin_entry = admin_dir / f'{name}.php'
    admin_entry_content = f'''<?php
defined('_JEXEC') or die;

use Joomla\\CMS\\Factory;
use Joomla\\CMS\\Dispatcher\\ComponentDispatcher;

$dispatcher = new ComponentDispatcher('{namespace_prefix}');
$dispatcher->dispatch();
'''
    with open(admin_entry, 'w') as f:
        f.write(admin_entry_content)
    
    # services/provider.php
    services_dir = admin_dir / 'services'
    services_dir.mkdir(parents=True, exist_ok=True)
    provider_file = services_dir / 'provider.php'
    provider_content = f'''<?php
defined('_JEXEC') or die;

use Joomla\\DI\\Container;
use Joomla\\DI\\ServiceProviderInterface;

class {namespace_prefix}ServiceProvider implements ServiceProviderInterface
{{
    public function register(Container $container)
    {{
        // Register services here
    }}
}}
'''
    with open(provider_file, 'w') as f:
        f.write(provider_content)
    
    # sql/install.mysql.utf8.sql
    sql_dir = admin_dir / 'sql'
    sql_dir.mkdir(parents=True, exist_ok=True)
    sql_file = sql_dir / 'install.mysql.utf8.sql'
    sql_content = f'''CREATE TABLE IF NOT EXISTS `#__{name}_items` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `title` varchar(255) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
'''
    with open(sql_file, 'w') as f:
        f.write(sql_content)
    
    # name.xml
    xml_file = admin_dir / f'{name}.xml'
    xml_content = f'''<?xml version="1.0" encoding="utf-8"?>
<extension type="component" version="4.0" method="upgrade">
    <name>{display_name}</name>
    <version>1.0.0</version>
    <description>COM_{upper_name}_DESCRIPTION</description>
    <administration>
        <files folder="administrator/components/{name}">
            <filename>{name}.php</filename>
            <filename>{name}.xml</filename>
            <folder>services</folder>
            <folder>sql</folder>
        </files>
    </administration>
    <site>
        <files folder="components/{name}">
            <filename>{name}.php</filename>
            <folder>src</folder>
            <folder>tmpl</folder>
        </files>
    </site>
</extension>
'''
    with open(xml_file, 'w') as f:
        f.write(xml_content)
    
    # Success message
    created_files = [
        str(site_entry),
        str(controller_file),
        str(view_file),
        str(tmpl_file),
        str(admin_entry),
        str(provider_file),
        str(sql_file),
        str(xml_file)
    ]
    print(f"Component '{name}' scaffolded successfully. Created files:")
    for file in created_files:
        print(f"  {file}")