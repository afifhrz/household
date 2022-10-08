import html
from dashboard.models import admin_mst_module

from django import template
register = template.Library()
  
@register.simple_tag
def loop_module(active_page):
    list_menu = admin_mst_module.objects.filter(validstatus=1, adm_mst_id=0).order_by('ordernumber')
    list_submenu = []
    
    for id in list_menu:
        list_submenu.append(admin_mst_module.objects.filter(validstatus=1, adm_mst_id=id.id).order_by('ordernumber'))

    for_loop = zip(list_menu,list_submenu)

    result = ""
    i = 1
    for row, submenu in for_loop:
        if i == 1:
            if row.modulename == active_page:
                result += f"""<a href="{row.moduleurl}" class="nav-item nav-link active "><i class="fa {row.moduleicon} me-2"></i>{row.modulename}</a>"""
            else:
                result += f"""<a href="{row.moduleurl}" class="nav-item nav-link "><i class="fa {row.moduleicon} me-2"></i>{row.modulename}</a>"""
            i +=1
        else:
            if submenu:
                if row.modulename == active_page:
                    result += f"""  <div class="nav-item dropdown">
                                        <a href="{row.moduleurl}" class="nav-link active dropdown-toggle" data-bs-toggle="dropdown"><i class="fa {row.moduleicon} me-2"></i>{row.modulename}</a>
                                        <div class="dropdown-menu bg-transparent border-0">
                                """
                else:
                    result += f"""  <div class="nav-item dropdown">
                                        <a href="{row.moduleurl}" class="nav-link dropdown-toggle" data-bs-toggle="dropdown"><i class="fa {row.moduleicon} me-2"></i>{row.modulename}</a>
                                        <div class="dropdown-menu bg-transparent border-0">
                                """
                    
                for data_sub in submenu:
                    result +=f"""<a href="{data_sub.moduleurl}" class="dropdown-item">{data_sub.modulename}</a>"""
                
                result += """</div>        
                        </div>"""
    return result