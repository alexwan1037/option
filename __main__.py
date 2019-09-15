"""Build static HTML site from directory of HTML templates and plain files."""

import os
import json
import shutil
import jinja2
import click


def hello(verbose):
    """Hello case."""
    orig_path = os.path.abspath("hello") + "\\"
    try:
        with open(orig_path+'/config.json') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print("Error_JSON: failed to parse")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: Json file does not exist")
        exit(1)
    try:
        environ = jinja2.Environment(loader=jinja2.FileSystemLoader
                                     (orig_path +
                                      "/templates/"), autoescape=True)
        env_template = environ.get_template('index.html')
        rendered_tem = env_template.render(words=data[0]['context']['words'])
        new_pos = orig_path + "html\\"
    except jinja2.exceptions.TemplateError:
        print("Error_Jinja: Failed to render")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: template cannot be found does not exist")
        exit(1)
    try:
        os.mkdir(new_pos)
        out = open(new_pos + "index.html", 'w')
    except FileExistsError:
        print("Error_Output_Dir: output directory already contains files html")
        exit(1)
    if verbose:
        print("Rendered index.html -> " + new_pos + 'index.html')
    out.write(rendered_tem)


def hello_css(verbose):
    """Hello_css case."""
    orig_path = os.path.abspath("hello_css") + "\\"
    try:
        with open(orig_path + '/config.json') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print("Error_JSON: failed to parse")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: Json file does not exist")
        exit(1)
    try:
        environ = jinja2.Environment(loader=jinja2.FileSystemLoader
                                     (orig_path +
                                      "/templates/"), autoescape=True)
        env_template = environ.get_template('index.html')
        rendered_tem = env_template.render(words=data[0]['context']['words'])
        new_pos = orig_path + "html\\"
    except jinja2.exceptions.TemplateError:
        print("Error_Jinja: Failed to render")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: template cannot be found does not exist")
        exit(1)
    try:
        os.mkdir(new_pos)
        os.mkdir(new_pos + 'css\\')
        out = open(new_pos + "index.html", 'w')
    except FileExistsError:
        print("Error_Output_Dir: "
              "output directory already contains files html")
        exit(1)
    shutil.copyfile(orig_path +
                    "static\\css\\style.css",
                    new_pos + 'css\\style.css')
    if verbose:
        print("Copied " + orig_path + 'static\\ -> ' + new_pos)
        print("Rendered index.html -> " + new_pos + 'index.html')
    out.write(rendered_tem)


def json_open(orig_path):
    """Render Json and check exceptions."""
    try:
        with open(orig_path+'/config.json') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print("Error_JSON: failed to parse")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: "
              "Json file does not exist")
        exit(1)
    return data


def render_temp(orig_path, verbose, data):
    """Render first index page."""
    try:
        environ = jinja2.Environment(loader=jinja2.FileSystemLoader
                                     (orig_path + "/templates/"),
                                     autoescape=True)
        env_template = environ.get_template('index.html')
        rendered_tem = env_template.render(context=data[0]['context'])
        new_pos = orig_path + "html\\"
    except jinja2.exceptions.TemplateError:
        print("Error_Jinja: Failed to render")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: "
              "template cannot be found does not exist")
        exit(1)
    try:
        shutil.copytree(orig_path + 'static\\', new_pos)
        if verbose:
            print("Copied " + orig_path +
                  'static\\ -> ' + orig_path + 'html\\')
        out = open(new_pos + "index.html", 'w')
        if verbose:
            print("Rendered index.html -> " + orig_path + 'html\\index.html')
        out.write(rendered_tem)
        os.mkdir(new_pos+"/u/")
    except FileExistsError:
        print("Error_Output_Dir: output directory already contains files html")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: template cannot be found does not exist")
        exit(1)
    return environ


def render_user(environ, data, new_pos, verbose, i):
    """Render all u/ pages."""
    try:
        env_template = environ.get_template('user.html')
        rendered_tem = env_template.render(context=data[i]['context'])
        user = new_pos + "u\\" + data[i]["context"]["username"] + '\\'
        os.mkdir(user)
        out = open(user + "index.html", 'w')
        if verbose:
            print("Rendered index.html -> " + user + 'index.html')
        out.write(rendered_tem)
        i = i + 1
        os.mkdir(user + "/followers/")
        os.mkdir(user + "/following/")
        env_template = environ.get_template('following.html')
        rendered_tem = env_template.render(context=data[i]['context'])
        out = open(user + "/following/index.html", 'w')
        if verbose:
            print("Rendered index.html -> " + user +
                  "following\\index.html")
        out.write(rendered_tem)
        i = i + 1
        env_template = environ.get_template('followers.html')
        rendered_tem = env_template.render(context=data[i]['context'])
        out = open(user + "followers\\index.html", 'w')
        if verbose:
            print("Rendered index.html -> " + user +
                  "followers\\index.html")
        out.write(rendered_tem)
        i = i + 1
    except jinja2.exceptions.TemplateError:
        print("Error_Jinja: Failed to render")
        exit(1)
    except FileExistsError:
        print("Error_Output_Dir: output directory "
              "already contains files html")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: template cannot "
              "be found does not exist")
        exit(1)
    return i


@click.command()
@click.argument('INPUT_DIR')
@click.option('-v', '--verbose', is_flag=True, help='Print more output')
def main(verbose, input_dir):
    """Templated Static website generator."""
    if input_dir == "hello":
        hello(verbose)
        exit(0)
    if input_dir == "hello_css":
        hello_css(verbose)
        exit(0)
    orig_path = os.path.abspath(input_dir) + "\\"
    data = json_open(orig_path)
    new_pos = orig_path + "html\\"
    environ = render_temp(orig_path, verbose, data)
    i = 1
    while data[i]["template"] != "post.html":
        i = render_user(environ, data, new_pos, verbose, i)
    try:
        while i < len(data) - 1:
            env_template = environ.get_template('post.html')
            p_id = data[i]["context"]["postid"]
            os.makedirs(new_pos+"/p//"+p_id+'/')
            rendered_tem = env_template.render(context=data[i]['context'])
            out = open(new_pos + '/p//' + p_id + '//index.html', 'w')
            if verbose:
                print("Rendered index.html -> " + new_pos +
                      'p\\' + p_id + '\\index.html')
            out.write(rendered_tem)
            i = i + 1
        env_template = environ.get_template('explore.html')
        os.mkdir(new_pos + "/explore/")
        rendered_tem = env_template.render(context=data[i]['context'])
        out = open(new_pos + "/explore/index.html", 'w')
    except jinja2.exceptions.TemplateError:
        print("Error_Jinja: Failed to render")
        exit(1)
    except FileExistsError:
        print("Error_Output_Dir: output directory "
              "already contains files html")
        exit(1)
    except FileNotFoundError:
        print("Error_FileNotFound: template "
              "cannot be found does not exist")
        exit(1)
    if verbose:
        print("Rendered index.html -> "
              + new_pos +
              "explore\\index.html")
    out.write(rendered_tem)


if __name__ == "__main__":
    main()
